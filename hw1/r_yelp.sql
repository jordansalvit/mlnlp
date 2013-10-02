-- MySQL dump 10.13  Distrib 5.5.30, for Linux (x86_64)
--
-- Host: jsalvitdbinstance.cku3opv9prdt.us-east-1.rds.amazonaws.com    Database: r_yelp
-- ------------------------------------------------------
-- Server version	5.5.27-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Business_Categories`
--

DROP TABLE IF EXISTS `Business_Categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Business_Categories` (
  `businessid` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Business_Neighborhoods`
--

DROP TABLE IF EXISTS `Business_Neighborhoods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Business_Neighborhoods` (
  `businessid` varchar(255) NOT NULL,
  `neighborhood` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Businesses`
--

DROP TABLE IF EXISTS `Businesses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Businesses` (
  `businessid` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `neighborhoods` varchar(255) DEFAULT NULL,
  `full_address` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `latitude` decimal(18,6) DEFAULT NULL,
  `longitude` decimal(18,6) DEFAULT NULL,
  `stars` decimal(6,2) DEFAULT NULL,
  `review_count` decimal(18,0) DEFAULT NULL,
  `photo_url` varchar(255) DEFAULT NULL,
  `categories` varchar(255) DEFAULT NULL,
  `open` varchar(255) DEFAULT NULL,
  `schools` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`businessid`),
  KEY `b_businessid` (`businessid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Reviews`
--

DROP TABLE IF EXISTS `Reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Reviews` (
  `businessid` varchar(255) NOT NULL,
  `userid` varchar(255) NOT NULL,
  `stars` decimal(18,4) DEFAULT NULL,
  `review` text,
  `review_date` date DEFAULT NULL,
  `useful` int(11) DEFAULT NULL,
  `funny` int(11) DEFAULT NULL,
  `cool` int(11) DEFAULT NULL,
  `Extrovert` decimal(18,6) DEFAULT NULL,
  `Introvert` decimal(18,6) DEFAULT NULL,
  `Sensing` decimal(18,6) DEFAULT NULL,
  `Intuitive` decimal(18,6) DEFAULT NULL,
  `Thinking` decimal(18,6) DEFAULT NULL,
  `Feeling` decimal(18,6) DEFAULT NULL,
  `Judging` decimal(18,6) DEFAULT NULL,
  `Perceiving` decimal(18,6) DEFAULT NULL,
  `MBTI` varchar(4) DEFAULT NULL,
  KEY `r_businessid` (`businessid`),
  KEY `r_userid` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Reviews_liwc`
--

DROP TABLE IF EXISTS `Reviews_liwc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Reviews_liwc` (
  `Filename` varchar(255) DEFAULT NULL,
  `businessid` varchar(55) DEFAULT NULL,
  `userid` varchar(55) DEFAULT NULL,
  `WC` decimal(18,6) DEFAULT NULL,
  `WPS` decimal(18,6) DEFAULT NULL,
  `Qmarks` decimal(18,6) DEFAULT NULL,
  `Sixltr` decimal(18,6) DEFAULT NULL,
  `Dic` decimal(18,6) DEFAULT NULL,
  `funct` decimal(18,6) DEFAULT NULL,
  `pronoun` decimal(18,6) DEFAULT NULL,
  `ppron` decimal(18,6) DEFAULT NULL,
  `i` decimal(18,6) DEFAULT NULL,
  `we` decimal(18,6) DEFAULT NULL,
  `you` decimal(18,6) DEFAULT NULL,
  `shehe` decimal(18,6) DEFAULT NULL,
  `they` decimal(18,6) DEFAULT NULL,
  `ipron` decimal(18,6) DEFAULT NULL,
  `article` decimal(18,6) DEFAULT NULL,
  `verb` decimal(18,6) DEFAULT NULL,
  `auxverb` decimal(18,6) DEFAULT NULL,
  `past` decimal(18,6) DEFAULT NULL,
  `present` decimal(18,6) DEFAULT NULL,
  `future` decimal(18,6) DEFAULT NULL,
  `adverb` decimal(18,6) DEFAULT NULL,
  `preps` decimal(18,6) DEFAULT NULL,
  `conj` decimal(18,6) DEFAULT NULL,
  `negate` decimal(18,6) DEFAULT NULL,
  `quant` decimal(18,6) DEFAULT NULL,
  `number` decimal(18,6) DEFAULT NULL,
  `swear` decimal(18,6) DEFAULT NULL,
  `social` decimal(18,6) DEFAULT NULL,
  `family` decimal(18,6) DEFAULT NULL,
  `friend` decimal(18,6) DEFAULT NULL,
  `humans` decimal(18,6) DEFAULT NULL,
  `affect` decimal(18,6) DEFAULT NULL,
  `posemo` decimal(18,6) DEFAULT NULL,
  `negemo` decimal(18,6) DEFAULT NULL,
  `anx` decimal(18,6) DEFAULT NULL,
  `anger` decimal(18,6) DEFAULT NULL,
  `sad` decimal(18,6) DEFAULT NULL,
  `cogmech` decimal(18,6) DEFAULT NULL,
  `insight` decimal(18,6) DEFAULT NULL,
  `cause` decimal(18,6) DEFAULT NULL,
  `discrep` decimal(18,6) DEFAULT NULL,
  `tentat` decimal(18,6) DEFAULT NULL,
  `certain` decimal(18,6) DEFAULT NULL,
  `inhib` decimal(18,6) DEFAULT NULL,
  `incl` decimal(18,6) DEFAULT NULL,
  `excl` decimal(18,6) DEFAULT NULL,
  `percept` decimal(18,6) DEFAULT NULL,
  `see` decimal(18,6) DEFAULT NULL,
  `hear` decimal(18,6) DEFAULT NULL,
  `feel` decimal(18,6) DEFAULT NULL,
  `bio` decimal(18,6) DEFAULT NULL,
  `body` decimal(18,6) DEFAULT NULL,
  `health` decimal(18,6) DEFAULT NULL,
  `sexual` decimal(18,6) DEFAULT NULL,
  `ingest` decimal(18,6) DEFAULT NULL,
  `relativ` decimal(18,6) DEFAULT NULL,
  `motion` decimal(18,6) DEFAULT NULL,
  `space` decimal(18,6) DEFAULT NULL,
  `time` decimal(18,6) DEFAULT NULL,
  `work` decimal(18,6) DEFAULT NULL,
  `achieve` decimal(18,6) DEFAULT NULL,
  `leisure` decimal(18,6) DEFAULT NULL,
  `home` decimal(18,6) DEFAULT NULL,
  `money` decimal(18,6) DEFAULT NULL,
  `relig` decimal(18,6) DEFAULT NULL,
  `death` decimal(18,6) DEFAULT NULL,
  `assent` decimal(18,6) DEFAULT NULL,
  `nonfl` decimal(18,6) DEFAULT NULL,
  `filler` decimal(18,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `userid` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `review_count` decimal(18,0) DEFAULT NULL,
  `average_stars` decimal(18,2) DEFAULT NULL,
  `useful` decimal(18,0) DEFAULT NULL,
  `funny` decimal(18,0) DEFAULT NULL,
  `cool` decimal(18,0) DEFAULT NULL,
  `Extrovert` decimal(18,6) DEFAULT NULL,
  `Introvert` decimal(18,6) DEFAULT NULL,
  `Sensing` decimal(18,6) DEFAULT NULL,
  `Intuitive` decimal(18,6) DEFAULT NULL,
  `Thinking` decimal(18,6) DEFAULT NULL,
  `Feeling` decimal(18,6) DEFAULT NULL,
  `Judging` decimal(18,6) DEFAULT NULL,
  `Perceiving` decimal(18,6) DEFAULT NULL,
  `MBTI` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`userid`),
  KEY `u_userid` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users_liwc`
--

DROP TABLE IF EXISTS `Users_liwc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users_liwc` (
  `Filename` varchar(255) DEFAULT NULL,
  `userid` varchar(45) DEFAULT NULL,
  `WC` decimal(18,6) DEFAULT NULL,
  `WPS` decimal(18,6) DEFAULT NULL,
  `Qmarks` decimal(18,6) DEFAULT NULL,
  `Sixltr` decimal(18,6) DEFAULT NULL,
  `Dic` decimal(18,6) DEFAULT NULL,
  `funct` decimal(18,6) DEFAULT NULL,
  `pronoun` decimal(18,6) DEFAULT NULL,
  `ppron` decimal(18,6) DEFAULT NULL,
  `i` decimal(18,6) DEFAULT NULL,
  `we` decimal(18,6) DEFAULT NULL,
  `you` decimal(18,6) DEFAULT NULL,
  `shehe` decimal(18,6) DEFAULT NULL,
  `they` decimal(18,6) DEFAULT NULL,
  `ipron` decimal(18,6) DEFAULT NULL,
  `article` decimal(18,6) DEFAULT NULL,
  `verb` decimal(18,6) DEFAULT NULL,
  `auxverb` decimal(18,6) DEFAULT NULL,
  `past` decimal(18,6) DEFAULT NULL,
  `present` decimal(18,6) DEFAULT NULL,
  `future` decimal(18,6) DEFAULT NULL,
  `adverb` decimal(18,6) DEFAULT NULL,
  `preps` decimal(18,6) DEFAULT NULL,
  `conj` decimal(18,6) DEFAULT NULL,
  `negate` decimal(18,6) DEFAULT NULL,
  `quant` decimal(18,6) DEFAULT NULL,
  `number` decimal(18,6) DEFAULT NULL,
  `swear` decimal(18,6) DEFAULT NULL,
  `social` decimal(18,6) DEFAULT NULL,
  `family` decimal(18,6) DEFAULT NULL,
  `friend` decimal(18,6) DEFAULT NULL,
  `humans` decimal(18,6) DEFAULT NULL,
  `affect` decimal(18,6) DEFAULT NULL,
  `posemo` decimal(18,6) DEFAULT NULL,
  `negemo` decimal(18,6) DEFAULT NULL,
  `anx` decimal(18,6) DEFAULT NULL,
  `anger` decimal(18,6) DEFAULT NULL,
  `sad` decimal(18,6) DEFAULT NULL,
  `cogmech` decimal(18,6) DEFAULT NULL,
  `insight` decimal(18,6) DEFAULT NULL,
  `cause` decimal(18,6) DEFAULT NULL,
  `discrep` decimal(18,6) DEFAULT NULL,
  `tentat` decimal(18,6) DEFAULT NULL,
  `certain` decimal(18,6) DEFAULT NULL,
  `inhib` decimal(18,6) DEFAULT NULL,
  `incl` decimal(18,6) DEFAULT NULL,
  `excl` decimal(18,6) DEFAULT NULL,
  `percept` decimal(18,6) DEFAULT NULL,
  `see` decimal(18,6) DEFAULT NULL,
  `hear` decimal(18,6) DEFAULT NULL,
  `feel` decimal(18,6) DEFAULT NULL,
  `bio` decimal(18,6) DEFAULT NULL,
  `body` decimal(18,6) DEFAULT NULL,
  `health` decimal(18,6) DEFAULT NULL,
  `sexual` decimal(18,6) DEFAULT NULL,
  `ingest` decimal(18,6) DEFAULT NULL,
  `relativ` decimal(18,6) DEFAULT NULL,
  `motion` decimal(18,6) DEFAULT NULL,
  `space` decimal(18,6) DEFAULT NULL,
  `time` decimal(18,6) DEFAULT NULL,
  `work` decimal(18,6) DEFAULT NULL,
  `achieve` decimal(18,6) DEFAULT NULL,
  `leisure` decimal(18,6) DEFAULT NULL,
  `home` decimal(18,6) DEFAULT NULL,
  `money` decimal(18,6) DEFAULT NULL,
  `relig` decimal(18,6) DEFAULT NULL,
  `death` decimal(18,6) DEFAULT NULL,
  `assent` decimal(18,6) DEFAULT NULL,
  `nonfl` decimal(18,6) DEFAULT NULL,
  `filler` decimal(18,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-10-02 18:29:43
