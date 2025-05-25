-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: hetuvan
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `tuongtac`
--

DROP TABLE IF EXISTS `tuongtac`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tuongtac` (
  `InteractionID` int NOT NULL AUTO_INCREMENT,
  `GhiChu` text,
  `UserID` int NOT NULL,
  `ProductID` int NOT NULL,
  `InteractionType` enum('view','cart','wishlist') NOT NULL,
  `Rating` smallint DEFAULT NULL,
  `InteractionTime` datetime DEFAULT NULL,
  `SoLanXem` int DEFAULT NULL,
  `ThoiGianXem` int DEFAULT NULL,
  PRIMARY KEY (`InteractionID`),
  KEY `UserID` (`UserID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `tuongtac_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `nguoidung` (`UserID`),
  CONSTRAINT `tuongtac_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `sanpham` (`ProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tuongtac`
--

LOCK TABLES `tuongtac` WRITE;
/*!40000 ALTER TABLE `tuongtac` DISABLE KEYS */;
INSERT INTO `tuongtac` VALUES (1,'Xem sản phẩm',1,1,'view',5,'2025-05-12 16:54:14',3,120),(2,'Thêm vào giỏ hàng',1,3,'cart',NULL,'2025-05-12 16:54:14',1,0),(3,'Thêm vào danh sách yêu thích',1,5,'wishlist',NULL,'2025-05-12 16:54:14',1,0),(4,'Xem sản phẩm',2,2,'view',4,'2025-05-12 16:54:14',2,90),(5,'Thêm vào giỏ hàng',2,4,'cart',NULL,'2025-05-12 16:54:14',1,0),(6,'Thêm vào danh sách yêu thích',2,6,'wishlist',NULL,'2025-05-12 16:54:14',1,0),(7,'Xem sản phẩm',3,7,'view',5,'2025-05-12 16:54:14',3,150),(8,'Thêm vào giỏ hàng',3,9,'cart',NULL,'2025-05-12 16:54:14',1,0),(9,'Thêm vào danh sách yêu thích',3,10,'wishlist',NULL,'2025-05-12 16:54:14',1,0);
/*!40000 ALTER TABLE `tuongtac` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-12 22:20:27
