-- MySQL dump 10.15  Distrib 10.0.13-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: videoag
-- ------------------------------------------------------
-- Server version	10.0.13-MariaDB-log

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
-- Table structure for table `auth`
--

DROP TABLE IF EXISTS `auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `token` char(128) NOT NULL,
  `user` tinytext NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `valid` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
INSERT INTO `auth` VALUES (1,'aab8d0dc34b59ee9e804f1261a2da9a82feafb64054cd40c4a62fa0767aed228096e558b13452623579208ed33904c6762c4ad625c4e7b25c2b2688e2e5ebb0c','moritz','2014-09-03 19:49:29',1);
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `endings`
--

DROP TABLE IF EXISTS `endings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `endings` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `ending` tinytext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ending` (`ending`(255))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endings`
--

LOCK TABLES `endings` WRITE;
/*!40000 ALTER TABLE `endings` DISABLE KEYS */;
INSERT INTO `endings` VALUES (1,'mts');
/*!40000 ALTER TABLE `endings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fileevent`
--

DROP TABLE IF EXISTS `fileevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fileevent` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `file` mediumint(8) unsigned NOT NULL,
  `lecture` mediumint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `filelecture` (`file`,`lecture`),
  KEY `fileevent` (`file`),
  KEY `lecture` (`lecture`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fileevent`
--

LOCK TABLES `fileevent` WRITE;
/*!40000 ALTER TABLE `fileevent` DISABLE KEYS */;
/*!40000 ALTER TABLE `fileevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filepaths`
--

DROP TABLE IF EXISTS `filepaths`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filepaths` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `fileid` mediumint(8) unsigned NOT NULL,
  `path` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filepaths`
--

LOCK TABLES `filepaths` WRITE;
/*!40000 ALTER TABLE `filepaths` DISABLE KEYS */;
/*!40000 ALTER TABLE `filepaths` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `files` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `uuhash` tinytext NOT NULL,
  `origname` tinytext NOT NULL,
  `path` text,
  `size` bigint(20) unsigned NOT NULL,
  `mtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `md5` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuhash` (`uuhash`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filesubtest`
--

DROP TABLE IF EXISTS `filesubtest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filesubtest` (
  `id` mediumint(9) unsigned NOT NULL AUTO_INCREMENT,
  `file` mediumint(9) unsigned NOT NULL,
  `subtest` smallint(9) unsigned NOT NULL,
  `data` tinytext,
  `good` tinyint(1) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `file` (`file`),
  KEY `good` (`good`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filesubtest`
--

LOCK TABLES `filesubtest` WRITE;
/*!40000 ALTER TABLE `filesubtest` DISABLE KEYS */;
/*!40000 ALTER TABLE `filesubtest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `level` tinyint(3) unsigned NOT NULL,
  `logid` mediumint(8) unsigned NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `msg` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `logid` (`logid`),
  KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logids`
--

DROP TABLE IF EXISTS `logids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logids` (
  `logid` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`logid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logids`
--

LOCK TABLES `logids` WRITE;
/*!40000 ALTER TABLE `logids` DISABLE KEYS */;
/*!40000 ALTER TABLE `logids` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subtest`
--

DROP TABLE IF EXISTS `subtest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subtest` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `test` smallint(6) unsigned NOT NULL,
  `name` tinytext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `test` (`test`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subtest`
--

LOCK TABLES `subtest` WRITE;
/*!40000 ALTER TABLE `subtest` DISABLE KEYS */;
INSERT INTO `subtest` VALUES (1,1,'md5'),(2,2,'mp2t');
/*!40000 ALTER TABLE `subtest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testending`
--

DROP TABLE IF EXISTS `testending`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `testending` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `test` smallint(5) unsigned NOT NULL,
  `ending` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `test` (`test`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testending`
--

LOCK TABLES `testending` WRITE;
/*!40000 ALTER TABLE `testending` DISABLE KEYS */;
INSERT INTO `testending` VALUES (1,1,1),(2,2,1);
/*!40000 ALTER TABLE `testending` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tests`
--

DROP TABLE IF EXISTS `tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tests` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests`
--

LOCK TABLES `tests` WRITE;
/*!40000 ALTER TABLE `tests` DISABLE KEYS */;
INSERT INTO `tests` VALUES (1,'md5'),(2,'mp2t');
/*!40000 ALTER TABLE `tests` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-09-18 15:36:20
