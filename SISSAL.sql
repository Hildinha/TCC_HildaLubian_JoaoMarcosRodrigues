CREATE DATABASE  IF NOT EXISTS `sissal` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sissal`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sissal
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `userName` varchar(255) DEFAULT NULL,
  `userPassword` varchar(255) DEFAULT NULL,
  `userRole` varchar(15) DEFAULT NULL,
  `userCard` int DEFAULT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'root','$2b$12$MVCJNLqXVj/3yGU1nKw0MO7o0SEFFJ4meOuu8Q0dGLoXs/isnKpYS','Admin',NULL)
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Rooms`
--

DROP TABLE IF EXISTS `Rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Rooms` (
  `roomId` int NOT NULL AUTO_INCREMENT,
  `roomFloor` int NOT NULL,
  `roomNumber` int NOT NULL,
  `roomCapacity` int NOT NULL,
  `roomCooling` enum('Sim','Não') DEFAULT NULL,
  PRIMARY KEY (`roomId`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Rooms`
--

LOCK TABLES `Rooms` WRITE;
/*!40000 ALTER TABLE `Rooms` DISABLE KEYS */;
INSERT INTO `Rooms` VALUES (1,1,101,40,'Sim'),(2,1,102,40,'Sim'),(3,1,103,40,'Sim'),(4,1,104,40,'Sim'),(5,1,105,40,'Sim'),(6,1,106,40,'Sim'),(7,1,107,40,'Sim'),(8,1,108,40,'Sim'),(9,1,109,40,'Sim'),(10,1,110,40,'Sim'),(11,2,201,40,'Sim'),(12,2,202,40,'Sim'),(13,2,203,40,'Sim'),(14,2,204,40,'Sim'),(15,2,205,40,'Sim'),(16,2,206,40,'Sim'),(17,2,207,40,'Sim'),(18,2,208,40,'Sim'),(19,2,209,40,'Sim'),(20,2,210,40,'Sim'),(21,3,301,40,'Sim'),(22,3,302,40,'Sim'),(23,3,303,40,'Sim'),(24,3,304,40,'Sim'),(25,3,305,40,'Sim'),(26,3,306,40,'Sim'),(27,3,307,40,'Sim'),(28,3,308,40,'Sim'),(29,3,309,40,'Sim'),(30,3,310,40,'Sim'),(31,4,401,40,'Sim'),(32,4,402,40,'Sim'),(33,4,403,40,'Sim'),(34,4,404,40,'Sim'),(35,4,405,40,'Sim'),(36,4,406,40,'Sim'),(37,4,407,40,'Sim'),(38,4,408,40,'Sim'),(39,4,409,40,'Sim'),(40,4,410,40,'Sim'),(41,4,401,40,'Sim'),(42,4,402,40,'Sim'),(43,4,403,40,'Sim'),(44,4,404,40,'Sim'),(45,4,405,40,'Sim'),(46,4,406,40,'Sim'),(47,4,407,40,'Sim'),(48,4,408,40,'Sim'),(49,4,409,40,'Sim'),(50,4,410,40,'Sim');
/*!40000 ALTER TABLE `Rooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `BookingRooms`
--

DROP TABLE IF EXISTS `BookingRooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `BookingRooms`` (
  `bookingId` int NOT NULL AUTO_INCREMENT,
  `userId` int NOT NULL,
  `roomId` int NOT NULL,
  `roomNumber` int NOT NULL,
  `userCard` int NOT NULL,
  `userName` varchar(255) NOT NULL,
  `startHour` time NOT NULL,
  `endHour` time NOT NULL,
  `bookingDate` date NOT NULL,
  PRIMARY KEY (`bookingId`),
  FOREIGN KEY (`userId`) REFERENCES `Users`(`userId`),
  FOREIGN KEY (`roomId`) REFERENCES `rooms`(`roomId`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-01 15:47:10