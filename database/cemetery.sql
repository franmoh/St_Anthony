-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: cemetery-1.cf1lxre0nkgj.ca-central-1.rds.amazonaws.com    Database: cemetery
-- ------------------------------------------------------
-- Server version	11.4.9-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ContactDetails`
--

DROP TABLE IF EXISTS `ContactDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ContactDetails` (
  `ContactDetailsID` int(11) NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(100) NOT NULL,
  `MiddleName` varchar(100) DEFAULT NULL,
  `LastName` varchar(100) NOT NULL,
  `PhoneNumber` varchar(100) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `NoteID` int(11) DEFAULT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`ContactDetailsID`),
  KEY `FK_ContactDetails_Notes` (`NoteID`),
  KEY `FK_ContactDetails_CreatedBy` (`CreatedBy`),
  KEY `FK_ContactDetails_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_ContactDetails_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_ContactDetails_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_ContactDetails_Notes` FOREIGN KEY (`NoteID`) REFERENCES `Notes` (`NoteID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ContactDetails`
--

LOCK TABLES `ContactDetails` WRITE;
/*!40000 ALTER TABLE `ContactDetails` DISABLE KEYS */;
INSERT INTO `ContactDetails` VALUES (1,'James',NULL,'Brennan','506-555-0101','12 King St, Fredericton, NB','jbrennan@example.com',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(2,'Maria','Rose','Chen','506-555-0102','88 Smythe St, Fredericton, NB','mchen@example.com',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(3,'Patrick',NULL,'OConnor','506-555-0103','5 Cathedral Ln, Fredericton, NB','poconnor@example.com',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(4,'Anne','Marie','Tremblay','506-555-0104','210 Regent St, Fredericton, NB','atremblay@example.com',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(5,'Michael',NULL,'Nguyen','506-555-0105','7 Acadian Ave, Fredericton, NB','mnguyen@example.com',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(6,'Sophia',NULL,'Adams','506-555-0106','34 Queen St, Fredericton, NB','sadams@example.com',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(7,'David','John','Robichaud','506-555-0107','102 Brunswick St, Fredericton, NB','drobichaud@example.com',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(8,'Emma',NULL,'Hartley','506-555-0108','19 Forest Hill Rd, Fredericton, NB','ehartley@example.com',NULL,'2026-04-25 09:00:00',1,NULL,NULL);
/*!40000 ALTER TABLE `ContactDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DeceasedContactMapping`
--

DROP TABLE IF EXISTS `DeceasedContactMapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DeceasedContactMapping` (
  `DeceasedContactMappingID` int(11) NOT NULL AUTO_INCREMENT,
  `DeceasedDetailsID` int(11) NOT NULL,
  `ContactDetailsID` int(11) NOT NULL,
  `IsPrimaryContact` bit(1) NOT NULL DEFAULT b'1',
  `RelationshipType` varchar(100) DEFAULT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`DeceasedContactMappingID`),
  UNIQUE KEY `UQ_DeceasedContactMapping` (`DeceasedDetailsID`,`ContactDetailsID`),
  KEY `FK_DeceasedContactMapping_ContactDetails` (`ContactDetailsID`),
  KEY `FK_DeceasedContactMapping_CreatedBy` (`CreatedBy`),
  KEY `FK_DeceasedContactMapping_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_DeceasedContactMapping_ContactDetails` FOREIGN KEY (`ContactDetailsID`) REFERENCES `ContactDetails` (`ContactDetailsID`),
  CONSTRAINT `FK_DeceasedContactMapping_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_DeceasedContactMapping_DeceasedDetails` FOREIGN KEY (`DeceasedDetailsID`) REFERENCES `DeceasedDetails` (`DeceasedDetailsID`),
  CONSTRAINT `FK_DeceasedContactMapping_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DeceasedContactMapping`
--

LOCK TABLES `DeceasedContactMapping` WRITE;
/*!40000 ALTER TABLE `DeceasedContactMapping` DISABLE KEYS */;
INSERT INTO `DeceasedContactMapping` VALUES (1,1,2,_binary '\1','Spouse','2026-04-25 09:00:00',1,NULL,NULL),(2,2,4,_binary '\1','Spouse','2026-04-25 09:00:00',1,NULL,NULL),(3,3,5,_binary '\1','Spouse','2026-04-25 09:00:00',1,NULL,NULL),(4,4,6,_binary '\1','Father','2026-04-25 09:00:00',1,NULL,NULL),(5,5,7,_binary '\1','Mother','2026-04-25 09:00:00',1,NULL,NULL),(6,6,8,_binary '\1','Spouse','2026-04-25 09:00:00',1,NULL,NULL),(7,7,7,_binary '\1','Brother','2026-04-25 09:00:00',1,NULL,NULL),(8,8,6,_binary '\1','Mother','2026-04-25 09:00:00',1,NULL,NULL);
/*!40000 ALTER TABLE `DeceasedContactMapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DeceasedDetails`
--

DROP TABLE IF EXISTS `DeceasedDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DeceasedDetails` (
  `DeceasedDetailsID` int(11) NOT NULL AUTO_INCREMENT,
  `PlotID` int(11) NOT NULL,
  `ZoneID` int(11) NOT NULL DEFAULT 0,
  `DeceasedStatusID` int(11) NOT NULL,
  `FirstName` varchar(100) DEFAULT NULL,
  `LastName` varchar(100) DEFAULT NULL,
  `MiddleName` varchar(100) DEFAULT NULL,
  `Gender` varchar(20) DEFAULT NULL,
  `DateBuried` date DEFAULT NULL,
  `DOBYear` smallint(5) unsigned DEFAULT NULL,
  `DOBMonth` tinyint(3) unsigned DEFAULT NULL,
  `DOBDay` tinyint(3) unsigned DEFAULT NULL,
  `DODYear` smallint(5) unsigned DEFAULT NULL,
  `DODMonth` tinyint(3) unsigned DEFAULT NULL,
  `DODDay` tinyint(3) unsigned DEFAULT NULL,
  `NoteID` int(11) DEFAULT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`DeceasedDetailsID`),
  UNIQUE KEY `uq_plot_zone` (`PlotID`,`ZoneID`),
  KEY `ix_DeceasedPlotStatus` (`PlotID`,`DeceasedStatusID`),
  KEY `ix_DateBuried` (`DateBuried`),
  KEY `FK_DeceasedDetails_DeceasedStatus` (`DeceasedStatusID`),
  KEY `FK_DeceasedDetails_Notes` (`NoteID`),
  KEY `FK_DeceasedDetails_CreatedBy` (`CreatedBy`),
  KEY `FK_DeceasedDetails_ModifiedBy` (`ModifiedBy`),
  KEY `idx_dobyear` (`DOBYear`),
  KEY `idx_dodyear` (`DODYear`),
  KEY `idx_deceased_plot` (`PlotID`),
  KEY `idx_deceased_zone` (`ZoneID`),
  CONSTRAINT `FK_DeceasedDetails_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_DeceasedDetails_DeceasedStatus` FOREIGN KEY (`DeceasedStatusID`) REFERENCES `DeceasedStatus` (`DeceasedStatusID`),
  CONSTRAINT `FK_DeceasedDetails_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_DeceasedDetails_Notes` FOREIGN KEY (`NoteID`) REFERENCES `Notes` (`NoteID`),
  CONSTRAINT `FK_DeceasedDetails_PlotDetails` FOREIGN KEY (`PlotID`) REFERENCES `PlotDetails` (`PlotDetailsID`),
  CONSTRAINT `chk_zone_range` CHECK (`ZoneID` between 0 and 8)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DeceasedDetails`
--

LOCK TABLES `DeceasedDetails` WRITE;
/*!40000 ALTER TABLE `DeceasedDetails` DISABLE KEYS */;
INSERT INTO `DeceasedDetails` VALUES (1,3,0,4,'Robert','Chen','J','M','2024-09-15',1948,3,22,2024,9,10,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(2,7,0,3,'Marc','Tremblay','P','M','2023-12-01',1952,11,8,2023,11,25,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(3,10,0,6,'Linh','Nguyen',NULL,'F','2025-04-12',1955,7,19,2025,4,5,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(4,13,0,6,'Walter','Adams','H','M','2024-06-22',1942,2,14,2024,6,18,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(5,17,0,6,'Mary','Robichaud','E','F','2024-11-03',1949,9,30,2024,10,28,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(6,20,0,6,'Thomas','Hartley','W','M','2025-08-17',1950,12,5,2025,8,12,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(7,25,0,6,'Joseph','Robichaud','P','M','2025-02-09',1947,4,25,2025,2,4,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(8,30,0,6,'Edith','Adams',NULL,'F','2025-10-14',1944,8,3,2025,10,9,NULL,'2026-04-25 09:00:00',1,NULL,NULL);
/*!40000 ALTER TABLE `DeceasedDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DeceasedStatus`
--

DROP TABLE IF EXISTS `DeceasedStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DeceasedStatus` (
  `DeceasedStatusID` int(11) NOT NULL AUTO_INCREMENT,
  `DeceasedStatusConstant` varchar(100) NOT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`DeceasedStatusID`),
  UNIQUE KEY `ixDeceasedStatusConstant` (`DeceasedStatusConstant`),
  UNIQUE KEY `uq_deceasedstatus_constant` (`DeceasedStatusConstant`),
  KEY `FK_DeceasedStatus_CreatedBy` (`CreatedBy`),
  KEY `FK_DeceasedStatus_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_DeceasedStatus_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_DeceasedStatus_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DeceasedStatus`
--

LOCK TABLES `DeceasedStatus` WRITE;
/*!40000 ALTER TABLE `DeceasedStatus` DISABLE KEYS */;
INSERT INTO `DeceasedStatus` VALUES (3,'FB','2026-02-08 16:25:20',1,NULL,NULL),(4,'L','2026-02-08 16:25:20',1,NULL,NULL),(5,'I','2026-02-08 16:25:20',1,NULL,NULL),(6,'A','2026-02-08 16:25:20',1,NULL,NULL),(7,'S','2026-02-22 17:44:17',1,NULL,NULL);
/*!40000 ALTER TABLE `DeceasedStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MaintenanceDetails`
--

DROP TABLE IF EXISTS `MaintenanceDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MaintenanceDetails` (
  `MaintenanceDetailsID` int(11) NOT NULL AUTO_INCREMENT,
  `PlotID` int(11) NOT NULL,
  `MaintenanceTypeID` int(11) NOT NULL,
  `ContactDetailsID` int(11) DEFAULT NULL,
  `NoteID` int(11) DEFAULT NULL,
  `MaintenanceDate` datetime DEFAULT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`MaintenanceDetailsID`),
  KEY `ix_PlotMaintenanceDetails` (`PlotID`,`MaintenanceTypeID`),
  KEY `FK_MaintenanceDetails_Contact` (`ContactDetailsID`),
  KEY `FK_MaintenanceDetails_Notes` (`NoteID`),
  KEY `FK_MaintenanceDetails_CreatedBy` (`CreatedBy`),
  KEY `FK_MaintenanceDetails_ModifiedBy` (`ModifiedBy`),
  KEY `FK_MaintenanceDetails_Type` (`MaintenanceTypeID`),
  CONSTRAINT `FK_MaintenanceDetails_Contact` FOREIGN KEY (`ContactDetailsID`) REFERENCES `ContactDetails` (`ContactDetailsID`),
  CONSTRAINT `FK_MaintenanceDetails_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_MaintenanceDetails_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_MaintenanceDetails_Notes` FOREIGN KEY (`NoteID`) REFERENCES `Notes` (`NoteID`),
  CONSTRAINT `FK_MaintenanceDetails_Plot` FOREIGN KEY (`PlotID`) REFERENCES `PlotDetails` (`PlotDetailsID`),
  CONSTRAINT `FK_MaintenanceDetails_Type` FOREIGN KEY (`MaintenanceTypeID`) REFERENCES `MaintenanceType` (`MaintenanceTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MaintenanceDetails`
--

LOCK TABLES `MaintenanceDetails` WRITE;
/*!40000 ALTER TABLE `MaintenanceDetails` DISABLE KEYS */;
INSERT INTO `MaintenanceDetails` VALUES (7,7,1,NULL,5,'2025-12-15 10:00:00','2026-02-08 17:14:58',1,NULL,NULL),(8,8,2,NULL,NULL,'2025-12-20 14:30:00','2026-02-08 17:14:58',1,NULL,NULL),(9,9,3,NULL,NULL,'2025-12-25 09:15:00','2026-02-08 17:14:58',1,NULL,NULL),(10,10,1,5,NULL,'2026-01-05 11:45:00','2026-02-08 17:14:58',1,NULL,NULL),(11,11,2,6,NULL,'2026-01-10 16:20:00','2026-02-08 17:14:58',1,NULL,NULL),(12,12,3,NULL,NULL,'2026-01-15 08:00:00','2026-02-08 17:14:58',1,NULL,NULL);
/*!40000 ALTER TABLE `MaintenanceDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MaintenanceStatus`
--

DROP TABLE IF EXISTS `MaintenanceStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MaintenanceStatus` (
  `MaintenanceStatusID` int(11) NOT NULL AUTO_INCREMENT,
  `MaintenanceStatusConstant` varchar(100) NOT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`MaintenanceStatusID`),
  UNIQUE KEY `ixMaintenanceStatusConstant` (`MaintenanceStatusConstant`),
  UNIQUE KEY `uq_maintenancestatus_constant` (`MaintenanceStatusConstant`),
  KEY `FK_MaintenanceStatus_CreatedBy` (`CreatedBy`),
  KEY `FK_MaintenanceStatus_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_MaintenanceStatus_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_MaintenanceStatus_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MaintenanceStatus`
--

LOCK TABLES `MaintenanceStatus` WRITE;
/*!40000 ALTER TABLE `MaintenanceStatus` DISABLE KEYS */;
INSERT INTO `MaintenanceStatus` VALUES (1,'GOOD','2025-12-11 03:25:25',1,NULL,NULL),(2,'BAD','2025-12-11 03:25:25',1,NULL,NULL),(3,'UGLY','2025-12-11 03:25:25',1,NULL,NULL);
/*!40000 ALTER TABLE `MaintenanceStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MaintenanceType`
--

DROP TABLE IF EXISTS `MaintenanceType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MaintenanceType` (
  `MaintenanceTypeID` int(11) NOT NULL AUTO_INCREMENT,
  `MaintenanceTypeConstant` varchar(100) NOT NULL,
  `Description` varchar(255) NOT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`MaintenanceTypeID`),
  UNIQUE KEY `uq_maintenancetype_constant` (`MaintenanceTypeConstant`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MaintenanceType`
--

LOCK TABLES `MaintenanceType` WRITE;
/*!40000 ALTER TABLE `MaintenanceType` DISABLE KEYS */;
INSERT INTO `MaintenanceType` VALUES (1,'Inspection','Regular inspection of the plot','2026-02-08 16:52:53',1,NULL,NULL),(2,'Cleaning','Cleaning or tidying up the plot','2026-02-08 16:52:53',1,NULL,NULL),(3,'Repair','Fixing damages to plot or markers','2026-02-08 16:52:53',1,NULL,NULL),(4,'Contact Update','Updating contact information for the plot','2026-02-08 16:52:53',1,NULL,NULL);
/*!40000 ALTER TABLE `MaintenanceType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Notes`
--

DROP TABLE IF EXISTS `Notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Notes` (
  `NoteID` int(11) NOT NULL AUTO_INCREMENT,
  `Note` varchar(4000) NOT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`NoteID`),
  KEY `FK_Notes_CreatedBy` (`CreatedBy`),
  KEY `FK_Notes_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_Notes_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_Notes_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Notes`
--

LOCK TABLES `Notes` WRITE;
/*!40000 ALTER TABLE `Notes` DISABLE KEYS */;
INSERT INTO `Notes` VALUES (1,'Plot is near the cemetery entrance, easy access.','2026-02-08 17:21:27',1,NULL,NULL),(2,'Deceased had requested a special ceremony.','2026-02-08 17:21:27',1,NULL,NULL),(3,'Contact prefers email notifications only.','2026-02-08 17:21:27',1,NULL,NULL),(4,'Payment plan approved for 3 installments.','2026-02-08 17:21:27',1,NULL,NULL),(5,'Maintenance scheduled quarterly for this plot.','2026-02-08 17:21:27',1,NULL,NULL),(6,'Special inscription requested on the headstone.','2026-02-08 17:21:27',1,NULL,NULL),(7,'These plots are reserved for the Butterfly Garden','2026-03-01 18:11:14',1,NULL,NULL),(8,'Test','2026-03-16 00:00:00',1,NULL,NULL);
/*!40000 ALTER TABLE `Notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PaymentDetails`
--

DROP TABLE IF EXISTS `PaymentDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PaymentDetails` (
  `PaymentDetailsID` int(11) NOT NULL AUTO_INCREMENT,
  `PlotID` int(11) NOT NULL,
  `DeceasedDetailsID` int(11) DEFAULT NULL,
  `ContactDetailsID` int(11) NOT NULL,
  `PaymentStatusID` int(11) NOT NULL,
  `BalancePaid` decimal(10,2) NOT NULL DEFAULT 0.00,
  `BalanceDue` decimal(10,2) NOT NULL DEFAULT 0.00,
  `DatePaid` datetime DEFAULT NULL,
  `NoteID` int(11) DEFAULT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`PaymentDetailsID`),
  KEY `ix_PlotPaymentStatus` (`PlotID`,`PaymentStatusID`),
  KEY `ix_DeceasedDetails` (`DeceasedDetailsID`),
  KEY `ix_ContactPaymentDetails` (`ContactDetailsID`),
  KEY `ix_DatePaid` (`DatePaid`),
  KEY `FK_PaymentDetails_PaymentStatus` (`PaymentStatusID`),
  KEY `FK_PaymentDetails_Notes` (`NoteID`),
  KEY `FK_PaymentDetails_CreatedBy` (`CreatedBy`),
  KEY `FK_PaymentDetails_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_PaymentDetails_ContactDetails` FOREIGN KEY (`ContactDetailsID`) REFERENCES `ContactDetails` (`ContactDetailsID`),
  CONSTRAINT `FK_PaymentDetails_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_PaymentDetails_DeceasedDetails` FOREIGN KEY (`DeceasedDetailsID`) REFERENCES `DeceasedDetails` (`DeceasedDetailsID`),
  CONSTRAINT `FK_PaymentDetails_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_PaymentDetails_Notes` FOREIGN KEY (`NoteID`) REFERENCES `Notes` (`NoteID`),
  CONSTRAINT `FK_PaymentDetails_PaymentStatus` FOREIGN KEY (`PaymentStatusID`) REFERENCES `PaymentStatus` (`PaymentStatusID`),
  CONSTRAINT `FK_PaymentDetails_PlotDetails` FOREIGN KEY (`PlotID`) REFERENCES `PlotDetails` (`PlotDetailsID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PaymentDetails`
--

LOCK TABLES `PaymentDetails` WRITE;
/*!40000 ALTER TABLE `PaymentDetails` DISABLE KEYS */;
INSERT INTO `PaymentDetails` VALUES (1,2,NULL,1,1,800.00,0.00,'2024-09-01 10:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(2,6,NULL,3,5,400.00,600.00,'2024-11-12 11:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(3,12,NULL,5,4,0.00,1200.00,NULL,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(4,19,NULL,8,3,0.00,1200.00,NULL,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(5,23,NULL,1,2,0.00,1200.00,NULL,NULL,'2026-04-25 09:00:00',1,NULL,NULL),(6,3,1,2,1,1500.00,0.00,'2024-09-14 14:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(7,7,2,4,1,1200.00,0.00,'2023-11-30 09:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(8,10,3,5,1,1200.00,0.00,'2025-04-11 10:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(9,13,4,6,1,1200.00,0.00,'2024-06-21 13:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(10,17,5,7,1,1200.00,0.00,'2024-11-02 15:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(11,20,6,8,1,1200.00,0.00,'2025-08-16 11:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(12,25,7,7,1,1200.00,0.00,'2025-02-08 12:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(13,30,8,6,1,1200.00,0.00,'2025-10-13 14:00:00',NULL,'2026-04-25 09:00:00',1,NULL,NULL);
/*!40000 ALTER TABLE `PaymentDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PaymentStatus`
--

DROP TABLE IF EXISTS `PaymentStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PaymentStatus` (
  `PaymentStatusID` int(11) NOT NULL AUTO_INCREMENT,
  `PaymentStatusConstant` varchar(100) NOT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`PaymentStatusID`),
  UNIQUE KEY `ixPaymentStatusConstant` (`PaymentStatusConstant`),
  UNIQUE KEY `uq_paymentstatus_constant` (`PaymentStatusConstant`),
  KEY `FK_PaymentStatus_CreatedBy` (`CreatedBy`),
  KEY `FK_PaymentStatus_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_PaymentStatus_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_PaymentStatus_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PaymentStatus`
--

LOCK TABLES `PaymentStatus` WRITE;
/*!40000 ALTER TABLE `PaymentStatus` DISABLE KEYS */;
INSERT INTO `PaymentStatus` VALUES (1,'PAID','2025-12-11 03:23:50',1,NULL,NULL),(2,'UNPAID','2025-12-11 03:23:50',1,NULL,NULL),(3,'PENDING','2025-12-11 03:23:50',1,NULL,NULL),(4,'PROMISETOPAY','2026-02-22 18:06:08',1,NULL,NULL),(5,'PARTIAL','2026-02-22 18:06:08',1,NULL,NULL);
/*!40000 ALTER TABLE `PaymentStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PlotContactMapping`
--

DROP TABLE IF EXISTS `PlotContactMapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PlotContactMapping` (
  `PlotContactMappingID` int(11) NOT NULL AUTO_INCREMENT,
  `PlotDetailsID` int(11) NOT NULL,
  `ContactDetailsID` int(11) NOT NULL,
  `IsPrimaryContact` bit(1) NOT NULL DEFAULT b'1',
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`PlotContactMappingID`),
  UNIQUE KEY `UQ_PlotContactMapping` (`PlotDetailsID`,`ContactDetailsID`),
  KEY `FK_PlotContactMapping_ContactDetails` (`ContactDetailsID`),
  KEY `FK_PlotContactMapping_CreatedBy` (`CreatedBy`),
  KEY `FK_PlotContactMapping_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_PlotContactMapping_ContactDetails` FOREIGN KEY (`ContactDetailsID`) REFERENCES `ContactDetails` (`ContactDetailsID`),
  CONSTRAINT `FK_PlotContactMapping_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_PlotContactMapping_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_PlotContactMapping_PlotDetails` FOREIGN KEY (`PlotDetailsID`) REFERENCES `PlotDetails` (`PlotDetailsID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PlotContactMapping`
--

LOCK TABLES `PlotContactMapping` WRITE;
/*!40000 ALTER TABLE `PlotContactMapping` DISABLE KEYS */;
INSERT INTO `PlotContactMapping` VALUES (1,2,1,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(2,3,2,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(3,6,3,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(4,7,4,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(5,10,5,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(6,12,5,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(7,13,6,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(8,17,7,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(9,19,8,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(10,20,8,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(11,23,1,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(12,25,7,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL),(13,30,6,_binary '\1','2026-04-25 09:00:00',1,NULL,NULL);
/*!40000 ALTER TABLE `PlotContactMapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PlotDetails`
--

DROP TABLE IF EXISTS `PlotDetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PlotDetails` (
  `PlotDetailsID` int(11) NOT NULL AUTO_INCREMENT,
  `PlotID` int(11) NOT NULL,
  `SectionID` int(11) NOT NULL,
  `Row` varchar(100) DEFAULT NULL,
  `Unit` varchar(100) DEFAULT NULL,
  `Side` varchar(100) DEFAULT NULL,
  `Niche` varchar(100) DEFAULT NULL,
  `MaintenanceStatusID` int(11) NOT NULL,
  `PlotStatus` enum('Available','Reserved','Occupied','Unknown') NOT NULL DEFAULT 'Available',
  `IsAvailable` bit(1) NOT NULL DEFAULT b'1',
  `NoteID` int(11) DEFAULT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`PlotDetailsID`),
  KEY `ix_MaintenanceStatus` (`MaintenanceStatusID`),
  KEY `ix_Notes` (`NoteID`),
  KEY `FK_PlotDetails_CreatedBy` (`CreatedBy`),
  KEY `FK_PlotDetails_ModifiedBy` (`ModifiedBy`),
  KEY `idx_plotdetails_section` (`SectionID`),
  KEY `idx_plotdetails_plot` (`PlotID`),
  CONSTRAINT `FK_PlotDetails_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_PlotDetails_MaintenanceStatus` FOREIGN KEY (`MaintenanceStatusID`) REFERENCES `MaintenanceStatus` (`MaintenanceStatusID`),
  CONSTRAINT `FK_PlotDetails_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_PlotDetails_Notes` FOREIGN KEY (`NoteID`) REFERENCES `Notes` (`NoteID`),
  CONSTRAINT `fk_plotdetails_section` FOREIGN KEY (`SectionID`) REFERENCES `Section` (`SectionID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PlotDetails`
--

LOCK TABLES `PlotDetails` WRITE;
/*!40000 ALTER TABLE `PlotDetails` DISABLE KEYS */;
INSERT INTO `PlotDetails` VALUES (1,1101,11,'1','A',NULL,NULL,1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(2,1102,11,'1','B',NULL,NULL,1,'Reserved',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(3,1103,11,'2','A',NULL,NULL,1,'Occupied',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(4,1104,11,'2','B',NULL,NULL,2,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(5,1401,14,NULL,NULL,NULL,NULL,1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(6,1402,14,NULL,NULL,NULL,NULL,1,'Reserved',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(7,1403,14,NULL,NULL,NULL,NULL,2,'Occupied',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(8,1404,14,NULL,NULL,NULL,NULL,3,'Unknown',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(9,3001,8,'Left','30','A','1',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(10,3002,8,'Left','30','A','2',1,'Occupied',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(11,3003,8,'Left','30','A','3',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(12,3004,8,'Left','30','A','4',1,'Reserved',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(13,3005,8,'Left','30','A','5',1,'Occupied',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(14,3006,8,'Left','30','A','6',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(15,3051,8,'Left','30','B','1',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(16,3052,8,'Left','30','B','2',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(17,3053,8,'Left','30','B','3',1,'Occupied',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(18,3054,8,'Left','30','B','4',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(19,3055,8,'Left','30','B','5',1,'Reserved',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(20,3056,8,'Left','30','B','6',1,'Occupied',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(21,5001,8,'Right','50','A','1',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(22,5002,8,'Right','50','A','2',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(23,5003,8,'Right','50','A','3',1,'Reserved',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(24,5004,8,'Right','50','A','4',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(25,5005,8,'Right','50','A','5',1,'Occupied',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(26,5006,8,'Right','50','A','6',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(27,5051,8,'Right','50','B','1',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(28,5052,8,'Right','50','B','2',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(29,5053,8,'Right','50','B','3',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(30,5054,8,'Right','50','B','4',1,'Occupied',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(31,5055,8,'Right','50','B','5',1,'Available',_binary '\1',NULL,'2026-04-25 09:00:00',1,NULL,NULL),(32,5056,8,'Right','50','B','6',1,'Unknown',_binary '\0',NULL,'2026-04-25 09:00:00',1,NULL,NULL);
/*!40000 ALTER TABLE `PlotDetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PlotReservationHistory`
--

DROP TABLE IF EXISTS `PlotReservationHistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PlotReservationHistory` (
  `PlotReservationHistoryID` int(11) NOT NULL AUTO_INCREMENT,
  `PlotDetailsID` int(11) NOT NULL,
  `CertNumber` varchar(50) DEFAULT NULL,
  `FirstName` varchar(100) DEFAULT NULL,
  `MiddleName` varchar(100) DEFAULT NULL,
  `LastName` varchar(100) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `PhoneNumber` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `AmountPaid` decimal(10,2) NOT NULL DEFAULT 0.00,
  `ReservedByName` varchar(200) DEFAULT NULL,
  `WitnessName` varchar(200) DEFAULT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  PRIMARY KEY (`PlotReservationHistoryID`),
  KEY `IX_PLOT_HISTORY` (`PlotDetailsID`,`CreatedDate`),
  KEY `FK_PlotReservationHistory_CreatedBy` (`CreatedBy`),
  CONSTRAINT `FK_PlotReservationHistory_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_PlotReservationHistory_PlotDetails` FOREIGN KEY (`PlotDetailsID`) REFERENCES `PlotDetails` (`PlotDetailsID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PlotReservationHistory`
--

LOCK TABLES `PlotReservationHistory` WRITE;
/*!40000 ALTER TABLE `PlotReservationHistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `PlotReservationHistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Section`
--

DROP TABLE IF EXISTS `Section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Section` (
  `SectionID` int(11) NOT NULL AUTO_INCREMENT,
  `SectionConstant` varchar(100) NOT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`SectionID`),
  UNIQUE KEY `uq_section_constant` (`SectionConstant`),
  KEY `ixSectionConstant` (`SectionConstant`,`SectionID`),
  KEY `FK_Section_CreatedBy` (`CreatedBy`),
  KEY `FK_Section_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_Section_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_Section_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Section`
--

LOCK TABLES `Section` WRITE;
/*!40000 ALTER TABLE `Section` DISABLE KEYS */;
INSERT INTO `Section` VALUES (8,'Columbarium','2025-12-11 03:15:05',1,'2026-02-22 17:47:57',1),(9,'GardenOfAngels','2025-12-11 03:15:05',1,'2026-02-22 17:47:57',1),(10,'Lower','2025-12-11 03:15:05',1,'2026-02-22 17:47:57',1),(11,'Middle','2025-12-11 03:15:05',1,'2026-02-22 17:47:57',1),(12,'Paul','2025-12-11 03:15:05',1,'2026-02-22 17:47:57',1),(13,'Upper','2025-12-11 03:15:05',1,'2026-02-22 17:47:57',1),(14,'Western','2025-12-11 03:15:05',1,'2026-02-22 17:47:57',1),(15,'ButterflyGarden','2026-02-22 17:48:02',1,NULL,NULL);
/*!40000 ALTER TABLE `Section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `UserID` int(11) NOT NULL AUTO_INCREMENT,
  `Password` varchar(255) NOT NULL,
  `ForcePasswordChange` bit(1) NOT NULL DEFAULT b'0',
  `IsLocked` bit(1) NOT NULL DEFAULT b'0',
  `Role` varchar(50) NOT NULL DEFAULT 'Admin',
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `IsActive` tinyint(1) NOT NULL DEFAULT 1,
  `LastLogin` date DEFAULT NULL,
  `CreatedDate` datetime NOT NULL,
  `CreatedBy` int(11) NOT NULL,
  `ModifiedDate` datetime DEFAULT NULL,
  `ModifiedBy` int(11) DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `ixUniqueUserName` (`Username`),
  KEY `ixActiveUser` (`Username`,`IsActive`),
  KEY `FK_User_CreatedBy` (`CreatedBy`),
  KEY `FK_User_ModifiedBy` (`ModifiedBy`),
  CONSTRAINT `FK_User_CreatedBy` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_User_ModifiedBy` FOREIGN KEY (`ModifiedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,_binary '1\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0',_binary '\0',_binary '\0','Admin','Admin','User','adminUser',1,NULL,'2025-12-11 03:14:07',1,NULL,NULL);
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'cemetery'
--

--
-- Dumping routines for database 'cemetery'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-11 23:26:20
