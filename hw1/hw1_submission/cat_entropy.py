# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 20:18:42 2013

@author: allan
"""

"""
This module contains sklearn style feature transformations for 
feature vectors from text documents, based on the TfidfTransformer.
"""

import itertools

import numpy as np
import scipy.sparse as sp

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import normalize

__all__ = ['CatEntTransformer', 'InvCatEntTransformer']

def _document_frequency(X):
    """Count the number of non-zero values for each feature in csc_matrix X."""
    return np.diff(X.indptr)    

class CatEntTransformer(BaseEstimator, TransformerMixin):
    """Transform a count matrix to a category entropy weighted representation
    
    The category entropy for each term is given by the entropy of the conditional
    probability distribution of p(category | term).
    
    The goal of this weight is to give a high weight to words that are common
    across categories and a low weight to those that only appear in certain categories.
    
    These weights should be used when it is suspected that the observed categories
    are confounding variables for some other classification task.
    
    Parameters
    ----------
    cats : array
    Category labels for each feature vector in input to transformer.
    Should have the same length as the number of examples.    
    
    norm  : 'l1', 'l2' or None, optional
    Norm used to normalize term vectors. None for no normalization.
    
    smooth : boolean, optional
    Smooth weights by adding one to document frequencies, as if an
    extra document was seen containing every term in the collection
    exactly once. Also the extra document belongs to each category.
    Prevents zero divisions.
    """
    
    def __init__(self, cats, norm='l2', smooth=True):
        self.cats = cats
        self.norm = norm
        self.smooth = smooth
        
    def fit(self, X, y=None):
        """Learn the catent vector (global term weights)
        
        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
        a matrix of term/token counts        
        """
        if not sp.isspmatrix_csc(X):
            X = sp.csc_matrix(X)
        
        n_samples, n_features = X.shape
        df = _document_frequency(X)
        cats = self.cats
        cat_vals, cat_indicies = np.unique(cats, return_inverse=True)
        cat_count = np.zeros((cat_vals.size, n_features))
               
        # preform smoothing if required
        df += int(self.smooth)
        n_samples += int(self.smooth)
        cat_count += int(self.smooth)
        
        # count appearance of each term for each category
        cx = X.tocoo()
        for i,j in itertools.izip(cx.row, cx.col):
#            print i, cats[i], cat_indicies[i]
            cat_count[cat_indicies[i], j] += 1
            
        # compute entropy of p(c|t) as
        # log(df(t)) - 1/df(t) * sum_c (count(c,t) * log(count(c,t)))
        catent = np.log(df) - 1/df * np.sum(cat_count * np.log(cat_count), axis=0)
#        catent = 1.0 / (catent + 1)
        self._catent_diag = sp.spdiags(catent, diags=0, m=n_features, n=n_features)
        
        return self
        
    def transform(self, X, copy=True):
        """Transform a count matrix to a catent weighted representation

        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
        a matrix of term/token counts
        
        Returns
        -------
        vectors : sparse matrix, [n_samples, n_features]
        """        
        if hasattr(X, 'dtype') and np.issubdtype(X.dtype, np.float):
            # preserve float family dtype
            X = sp.csr_matrix(X, copy=copy)
        else:
            # convert counts or binary occurrences to floats
            X = sp.csr_matrix(X, dtype=np.float64, copy=copy)

        n_samples, n_features = X.shape

        if not hasattr(self, "_catent_diag"):
            raise ValueError("catent weight vector not fitted")
        expected_n_features = self._catent_diag.shape[0]
        if n_features != expected_n_features:
            raise ValueError("Input has n_features=%d while the model"
                             " has been trained with n_features=%d" % (
                                 n_features, expected_n_features))
        # *= doesn't work
        X = X * self._catent_diag

        if self.norm:
            X = normalize(X, norm=self.norm, copy=False)

        return X
                
class InvCatEntTransformer(CatEntTransformer, TransformerMixin):
    def __init__(self, cats, norm='l2', smooth=True):    
        super(InvCatEntTransformer, self).__init__(cats, norm, smooth)
    
    def fit(self, X, y=None):
        """Learn the inverse catent vector (global term weights)
        
        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
        a matrix of term/token counts        
        """        
        _, n_features = X.shape        
        super(InvCatEntTransformer, self).fit(X)
        
        # invert catent weight vector and add 1 to avoid division by zero
        catent = 1.0 / (np.diag(self._catent_diag.todense()) + 1)
        self._catent_diag = sp.spdiags(catent, diags=0, m=n_features, n=n_features)
        
        return self
        
    def transform(self, X, copy=True):
        """Transform a count matrix to a catent weighted representation

        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
        a matrix of term/token counts
        
        Returns
        -------
        vectors : sparse matrix, [n_samples, n_features]
        """   
        return super(InvCatEntTransformer, self).transform(X)