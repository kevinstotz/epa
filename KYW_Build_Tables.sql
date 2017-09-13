CREATE DATABASE  IF NOT EXISTS `KYW2` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `KYW2`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: kaz16mysqlmedium.ckh7idnurzxi.us-west-2.rds.amazonaws.com    Database: KYW2
-- ------------------------------------------------------
-- Server version	5.6.27-log

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
-- Table structure for table `AGGREGATES`
--

DROP TABLE IF EXISTS `AGGREGATES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AGGREGATES` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(9) NOT NULL,
  `AGGREGATE` varchar(80) DEFAULT NULL,
  `CONTAMINANT` varchar(80) DEFAULT NULL,
  `DATE` varchar(10) DEFAULT NULL,
  `LEVEL` varchar(10) DEFAULT NULL,
  `UNITS` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `idx_AGGREGATES_PWSID` (`PWSID`),
  KEY `index4` (`AGGREGATE`)
) ENGINE=InnoDB AUTO_INCREMENT=2162656 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `CITY_NAMES`
--

DROP TABLE IF EXISTS `CITY_NAMES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CITY_NAMES` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(20) NOT NULL,
  `CITY_SERVED` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `index4` (`CITY_SERVED`,`PWSID`),
  KEY `idx_CITY_NAMES_PWSID` (`PWSID`)
) ENGINE=InnoDB AUTO_INCREMENT=196606 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `CONTAMINANTS`
--

DROP TABLE IF EXISTS `CONTAMINANTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CONTAMINANTS` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(20) NOT NULL DEFAULT '0',
  `CONTAMINANT` varchar(80) NOT NULL DEFAULT '0',
  `DATE` varchar(15) NOT NULL DEFAULT '0',
  `LEVEL` varchar(10) NOT NULL DEFAULT '0',
  `SIGN` char(2) NOT NULL DEFAULT '0',
  `UNITS` varchar(10) NOT NULL DEFAULT '0',
  `CITY` varchar(80) NOT NULL DEFAULT '0',
  `SDWIS_URI` varchar(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `idx_CONTAMINANTS_PWSID` (`PWSID`)
) ENGINE=InnoDB AUTO_INCREMENT=1900516 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `COUNTY_NAMES`
--

DROP TABLE IF EXISTS `COUNTY_NAMES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `COUNTY_NAMES` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(9) NOT NULL DEFAULT '0',
  `COUNTY_SERVED` varchar(45) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `index3` (`PWSID`,`COUNTY_SERVED`),
  UNIQUE KEY `index4` (`id`),
  KEY `index2` (`id`,`PWSID`,`COUNTY_SERVED`)
) ENGINE=InnoDB AUTO_INCREMENT=196606 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ENFORCEMENTS`
--

DROP TABLE IF EXISTS `ENFORCEMENTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ENFORCEMENTS` (
  `ENFORCEMENT_ID` varchar(20) NOT NULL,
  `VIOLATION_ID` varchar(20) NOT NULL,
  `PWSID` varchar(9) NOT NULL,
  `ENFORCEMENT_ACTION_TYPE_CODE` varchar(5) DEFAULT '0',
  `ENFORCEMENT_ACTION_TYPE_CODE_EXPLAIN` varchar(100) DEFAULT NULL,
  `ENFORCEMENT_DATE` date DEFAULT NULL,
  `ORIGINATOR_CODE` varchar(1) DEFAULT NULL,
  `SDWIS_URI` varchar(200) DEFAULT NULL,
  `ENFORCEMENT_COMMENT_TEXT` varchar(255) DEFAULT NULL,
  UNIQUE KEY `index1` (`VIOLATION_ID`,`PWSID`,`ENFORCEMENT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SOURCE_RESERVOIR`
--

DROP TABLE IF EXISTS `SOURCE_RESERVOIR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SOURCE_RESERVOIR` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(9) NOT NULL DEFAULT '0',
  `FACILITY_ID` varchar(20) NOT NULL DEFAULT '0',
  `FACILITY_NAME` varchar(80) NOT NULL DEFAULT '0',
  `SDWIS_URI` varchar(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `index3` (`FACILITY_ID`,`PWSID`)
) ENGINE=InnoDB AUTO_INCREMENT=327676 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `SOURCE_TREATMENTPLANT`
--

DROP TABLE IF EXISTS `SOURCE_TREATMENTPLANT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SOURCE_TREATMENTPLANT` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(9) NOT NULL DEFAULT '0',
  `FACILITY_ID` varchar(20) NOT NULL DEFAULT '0',
  `FACILITY_NAME` varchar(80) NOT NULL DEFAULT '0',
  `SDWIS_URI` varchar(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `index4` (`PWSID`,`FACILITY_ID`),
  KEY `idx_SOURCE_TREATMENTPLANT_PWSID` (`PWSID`)
) ENGINE=InnoDB AUTO_INCREMENT=131071 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `TREATMENTS`
--

DROP TABLE IF EXISTS `TREATMENTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TREATMENTS` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(9) DEFAULT '0',
  `FACILITY_ID` varchar(20) DEFAULT '0',
  `OBJECTIVE` varchar(1) DEFAULT '0',
  `OBJECTIVE_EXPLAIN` varchar(100) DEFAULT '0',
  `TREATMENT` varchar(3) DEFAULT '0',
  `COMMENTS` varchar(100) DEFAULT '0',
  `TREATMENT_EXPLAIN` varchar(100) DEFAULT '0',
  `SDWIS_URI` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `idx_TREATMENTS_PWSID` (`PWSID`)
) ENGINE=InnoDB AUTO_INCREMENT=196606 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `VIOLATIONS`
--

DROP TABLE IF EXISTS `VIOLATIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `VIOLATIONS` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(20) NOT NULL DEFAULT '0',
  `VIOLATION_ID` varchar(20) NOT NULL DEFAULT '0',
  `PWS_TYPE_CODE` varchar(6) DEFAULT '0',
  `SDWIS_URI` varchar(200) DEFAULT '0',
  `RTC_ENFORCEMENT_ID` varchar(20) DEFAULT '0',
  `SEVERITY_IND_CNT` int(11) DEFAULT '0',
  `UNIT_OF_MEASURE` varchar(9) DEFAULT '0',
  `CONTAMINANT_CODE_EXPLAIN` varchar(45) DEFAULT '0',
  `RULE_GROUP_CODE` varchar(3) DEFAULT '0',
  `CONTAMINANT_CODE` varchar(80) DEFAULT '0',
  `IS_MAJOR_VIOL_IND` char(1) DEFAULT '0',
  `COMPLIANCE_STATUS_CODE` char(4) DEFAULT '0',
  `IS_HEALTH_BASED_IND` char(1) DEFAULT '0',
  `COMPL_PER_END_DATE` varchar(15) DEFAULT '0',
  `COMPL_PER_BEGIN_DATE` varchar(15) DEFAULT '0',
  `ORIGINATOR_CODE` varchar(20) DEFAULT '0',
  `RULE_FAMILY_CODE` varchar(3) DEFAULT '0',
  `PRIMACY_AGENCY_CODE` varchar(2) DEFAULT '0',
  `FACILITY_ID` varchar(12) DEFAULT '0',
  `RULE_CODE` varchar(3) DEFAULT '0',
  `EPA_REGION` varchar(2) DEFAULT '0',
  `ENFORCEMENTS` int(11) NOT NULL DEFAULT '0',
  `VIOL_MEASURE` varchar(15) DEFAULT '0',
  `RTC_DATE` varchar(15) DEFAULT '0',
  `VIOLATION_CODE` varchar(4) DEFAULT '0',
  `PRIMARY_SOURCE_CODE` varchar(2) DEFAULT '0',
  `VIOLATION_CATEGORY_CODE` varchar(5) DEFAULT NULL,
  `VIOLATION_CODE_EXPLAIN` varchar(100) DEFAULT '0',
  `STATE_MCL` varchar(15) DEFAULT '0',
  `NPM_CANDIDATE` varchar(1) DEFAULT '0',
  `POPULATION_SERVED_COUNT` varchar(10) DEFAULT '0',
  `LATEST_ENFORCEMENT_ID` varchar(20) DEFAULT '0',
  `PUBLIC_NOTIFICATION_TIER` char(10) DEFAULT '0',
  `POP_CAT_5_CODE` varchar(2) DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `idx_VIOLATIONS_PWSID` (`PWSID`)
) ENGINE=InnoDB AUTO_INCREMENT=589816 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `WATER_SYSTEMS`
--

DROP TABLE IF EXISTS `WATER_SYSTEMS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `WATER_SYSTEMS` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(20) NOT NULL,
  `PWS_NAME` varchar(80) DEFAULT '0',
  `STATE_CODE` varchar(2) DEFAULT '0',
  `CITY_NAME` varchar(40) DEFAULT '0',
  `COUNTY_NAME` varchar(80) DEFAULT '0',
  `ZIP_CODE` varchar(12) DEFAULT '0',
  `ORG_NAME` varchar(80) DEFAULT '0',
  `ORG_ADDRESS_LINE1` varchar(80) DEFAULT '0',
  `ORG_ADDRESS_LINE2` varchar(80) DEFAULT '0',
  `ORG_PHONE_NUMBER` varchar(20) DEFAULT '0',
  `ORG_URI` varchar(256) DEFAULT '0',
  `ORG_CCR_REPORT_URI` varchar(256) DEFAULT '0',
  `IS_SCHOOL` char(1) DEFAULT '0',
  `OUTSTANDING_PERFORMER` varchar(3) DEFAULT '0',
  `POPULATION_SERVED` int(11) DEFAULT '0',
  `SOURCE_PURCHASED_PWSID` varchar(12) DEFAULT '0',
  `WATER_SOURCE_TYPE` varchar(10) DEFAULT '0',
  `SDWIS_URI` varchar(255) DEFAULT '0',
  PRIMARY KEY (`ID`,`PWSID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `PWSID_UNIQUE` (`PWSID`),
  KEY `idx_WATER_SYSTEMS_PWSID` (`PWSID`)
) ENGINE=InnoDB AUTO_INCREMENT=131071 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ZIP_CODES`
--

DROP TABLE IF EXISTS `ZIP_CODES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ZIP_CODES` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PWSID` varchar(20) NOT NULL,
  `ZIP_CODE` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `index4` (`ZIP_CODE`,`PWSID`),
  KEY `idx_ZIP_CODES_PWSID` (`PWSID`,`ZIP_CODE`)
) ENGINE=InnoDB AUTO_INCREMENT=196606 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'KYW2'
--

--
-- Dumping routines for database 'KYW2'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-09-01 17:26:53

