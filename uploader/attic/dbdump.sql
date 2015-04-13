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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
INSERT INTO `auth` VALUES (3,'3224e79d455a886a6a0fc210914004f5fe3f098f802e02d0f4a1963855d274ca5dda1752c991abbb2812eabec504ed6807572fb15cfb8e97e4c84530bd449e9f','moritz','2014-08-28 22:13:32',1);
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
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
  KEY `lecture` (`lecture`),
  KEY `file` (`file`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fileevent`
--

LOCK TABLES `fileevent` WRITE;
/*!40000 ALTER TABLE `fileevent` DISABLE KEYS */;
INSERT INTO `fileevent` VALUES (1,1,1337),(2,1,4711),(3,2,1337),(4,2,4711),(5,3,1337),(6,3,4711),(7,4,1337),(8,4,4711),(9,5,1337),(10,5,4711),(11,6,1337),(12,6,4711),(13,7,1337),(14,7,4711);
/*!40000 ALTER TABLE `fileevent` ENABLE KEYS */;
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
  `md5` binary(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuhash` (`uuhash`(255))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (1,'ygg49HF4wMYy6Ty8itZ1KbD1//8=','client.py','data/1',2639,'2014-08-30 13:24:01','ca0838f47178c0c6'),(2,'RZ8W96tu3ZXTU1Yz0K5ODV75//8=','comlib.py','data/2',1697,'2014-08-30 13:24:14','459f16f7ab6edd95'),(3,'mwZpsETo+obMGud8CbGYXVnr//8=','dblib.py','data/3',5286,'2014-08-30 13:22:31','9b0669b044e8fa86'),(4,'qewYo9IiT0kELsqujkzPE2L5//8=','filelib.py','data/4',1693,'2014-08-29 23:08:50','a9ec18a3d2224f49'),(5,'vcrznJDg6YFpIOAZLl+rdMT3//8=','identify.py','data/5',2107,'2014-08-29 23:08:50','bdcaf39c90e0e981'),(6,'6cBJiVDD2AFE2gn2dBTI12v4//8=','server.py','data/6',1940,'2014-08-30 12:59:59','e9c0498950c3d801'),(7,'ZipzUTtsHv8h3M5ITuxsTab3//8=','serverhandler.py','data/7',2137,'2014-08-29 23:08:50','662a73513b6c1eff'),(8,'5/Khou/ZcYEzB4MGljeRSEf8//8=','tools.py','data/8',952,'2014-08-30 13:20:57','e7f2a1a2efd97181');
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-08-30 15:46:49
