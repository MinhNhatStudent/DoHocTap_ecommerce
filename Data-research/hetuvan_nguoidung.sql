-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: hetuvan
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `nguoidung`
--

DROP TABLE IF EXISTS `nguoidung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nguoidung` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Ten` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Pass` varchar(255) NOT NULL,
  `Role` enum('user','admin') DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nguoidung`
--

LOCK TABLES `nguoidung` WRITE;
/*!40000 ALTER TABLE `nguoidung` DISABLE KEYS */;
INSERT INTO `nguoidung` VALUES (1,'Nguyen Van A','nguyenvana@example.com','12345','user',25,'2025-05-12 16:54:14'),(2,'Tran Thi B','tranthib@example.com','hashed_password_2','user',30,'2025-05-12 16:54:14'),(3,'Le Van C','levanc@example.com','hashed_password_3','user',35,'2025-05-12 16:54:14'),(4,'Laura Martinez','clarkpaul@example.org','%o6VGrKe','user',33,'2025-04-17 21:36:01'),(5,'Cynthia Bond','brennanmichael@example.net','$3)Ee!Du','user',30,'2023-05-14 18:25:31'),(6,'Maureen Chan','stephanie31@example.com','$*M)4iPt','user',28,'2023-10-22 17:43:43'),(7,'Jason Murray','josephkrueger@example.net',')6Z!r$iW','user',25,'2025-03-09 02:25:22'),(8,'Elizabeth Horn','doylejason@example.com','#8Ub_Sa7','user',18,'2024-04-03 18:01:29'),(9,'Melanie Weeks','lisawoods@example.com','(1yN$GMb','user',18,'2023-05-22 21:44:06'),(10,'Maurice Gutierrez','whitethomas@example.org','@5nM4eNg','user',26,'2023-07-09 16:14:55'),(11,'Daniel Miller','snowcheryl@example.org','!M_r0+Lc','user',19,'2024-04-05 13:17:36'),(12,'Scott Gonzales','xhowell@example.net','D!2QVt4m','user',27,'2025-03-23 05:11:45'),(13,'Justin Davenport','ann20@example.com','m*q7lySq','user',24,'2025-01-22 10:32:51'),(14,'Daniel Carlson','meadowstiffany@example.com','Aa^4RMmJ','user',32,'2024-05-27 00:59:10'),(15,'Kristi Stewart','james46@example.org','_S0Bbrzq','user',31,'2024-10-05 17:16:51'),(16,'Courtney Owens','agarcia@example.com','&+6DHmu5','user',26,'2025-04-18 06:11:47'),(17,'Erica Munoz','tammymcguire@example.org','^z8Qtt^i','user',21,'2023-06-29 09:03:33'),(18,'Andrew Cox','tiffany73@example.net','(1Z+t5dC','user',23,'2024-09-21 03:27:50'),(19,'Lauren Allen','samuelobrien@example.net','m!I9NPvf','user',20,'2025-03-03 11:54:43'),(20,'Pamela Gutierrez','griffithandrew@example.org','0^8N9Upw','user',31,'2024-10-18 10:55:35'),(21,'Mark Ortega','lewiskevin@example.com','t*1Ojud$','user',25,'2023-10-11 17:20:54'),(22,'Christopher Gross','reynoldslindsey@example.org','B)6HGw+9','user',28,'2023-06-07 09:23:54'),(23,'Caitlin Wolf','sbrown@example.org','$#0S0vTw','user',20,'2024-04-17 17:47:10'),(24,'Sarah Taylor','abriggs@example.com','^u26rxFx','user',31,'2025-03-23 21:00:36'),(25,'Jennifer Dixon','archerjennifer@example.org','y@6HCruI','user',34,'2024-06-29 00:09:28'),(26,'Crystal Stout','duncankevin@example.net','5$N5Dqxp','user',29,'2024-11-09 05:37:43'),(27,'Timothy Phillips','jgarcia@example.com','B$9FwC8b','user',29,'2024-09-03 04:43:27'),(28,'Debra Wong','garybarton@example.com','9+1HQ2jC','user',28,'2024-12-20 09:17:28'),(29,'Sean Valdez','derek16@example.com','&9A8S6Ax','user',32,'2024-01-06 16:14:27'),(30,'Beth Mcbride','pbowman@example.org','P@6Mgzk#','user',30,'2023-05-25 00:38:12'),(31,'Kathy Gomez','april56@example.org','8#7^m_Vu','user',26,'2023-07-05 01:28:46'),(32,'Dr. Jaime Mathis II','chad43@example.org','4^!6NIx%','user',23,'2025-03-15 10:40:48'),(33,'Susan Smith','darrenmiller@example.com','%v+5OIl#','user',35,'2023-12-07 14:18:36'),(34,'Rebecca Stewart','jenniferwilson@example.com','O%6*T#ir','user',18,'2024-01-25 16:02:47'),(35,'Hannah Vazquez','vargasjames@example.org','x&6SSOXe','user',29,'2024-03-29 07:06:29'),(36,'Steven Wilson','katie31@example.net','@8ZIqJwM','user',30,'2023-09-21 10:07:33'),(37,'Katie Page','tiffany66@example.net','&1ftZ3Pg','user',21,'2023-11-11 00:36:41'),(38,'Amy Fischer','haasthomas@example.com','&&4LZoEL','user',24,'2024-04-09 16:27:00'),(39,'Erin Green','phelpsbenjamin@example.com','gg$17kYx','user',23,'2023-12-01 06:18:53'),(40,'Shannon Stephenson','bryceespinoza@example.net','t(q9DulP','user',23,'2023-12-29 02:45:10'),(41,'Margaret Chambers','amiller@example.com','&n$63Eim','user',31,'2024-06-26 12:19:53'),(42,'Samantha Hardin','danielwall@example.com','^x0Y7^na','user',20,'2024-11-01 08:31:07'),(43,'Jordan Cole','xmartin@example.net','%(93aKue','user',19,'2024-11-17 12:59:12'),(44,'Sandra Herrera','ashley74@example.com','B$32iKXk','user',34,'2025-03-25 13:46:33'),(45,'Matthew Lee','cory86@example.net','#8Yuz4vl','user',25,'2025-03-04 13:39:51'),(46,'Deborah Gray','zsanders@example.com',')2zVUL0v','user',24,'2024-10-04 09:38:11'),(47,'Dr. Megan Robinson DDS','lloydbrandon@example.net','#8IW5yha','user',25,'2024-05-08 20:06:02'),(48,'Randy Mccall','april00@example.org','_4UlpW$d','user',30,'2023-08-27 12:05:00'),(49,'Miss Deborah Stevens DVM','richardbuchanan@example.org','G_I8y@Ut','user',20,'2024-05-03 09:17:12'),(50,'Emma Bowers','velazquezrobert@example.net','v+%83*Hd','user',24,'2023-09-24 00:31:59'),(51,'David Austin','nmartin@example.net','_f0X5Zec','user',25,'2025-04-16 11:25:43'),(52,'Kim Wright','rcunningham@example.net','e#8ByPOR','user',28,'2023-10-11 05:08:47'),(53,'Rebecca Fox','moorecarolyn@example.net','S+D22IsT','user',25,'2023-11-02 10:53:56'),(54,'Brett Charles','dillonjames@example.net','%W0gH+yn','user',30,'2025-01-06 09:31:25'),(55,'Margaret Hobbs','milestanner@example.org','t5^2lTeA','user',31,'2024-11-02 21:59:29'),(56,'Carly Lewis','amyrobinson@example.com','Q$f_Y2Ck','user',35,'2024-12-24 03:09:00'),(57,'Roger Spears','jesusrios@example.net','(03T0@Yz','user',20,'2024-07-02 22:00:32'),(58,'Lisa Cohen','floyddavid@example.org','_G11FDSk','user',27,'2023-10-19 08:31:30'),(59,'Michael Sullivan','sarah74@example.org','@+M3rSft','user',33,'2023-09-07 14:20:38'),(60,'Joshua Lowe','hgutierrez@example.org','%2kM1(lp','user',18,'2025-03-28 20:16:01'),(61,'Bethany Blake','jamieblackwell@example.com','YQ)1OUJi','user',21,'2023-11-29 01:30:12'),(62,'Colton Jackson','andrewcontreras@example.org','I@0&VpfB','user',29,'2024-07-04 23:12:35'),(63,'Angel Madden','cookjeremy@example.org','!5^hGvmY','user',34,'2024-11-13 14:14:45'),(64,'Kelly Combs','pricetyrone@example.org','JI$1u5Pi','user',28,'2023-06-01 02:16:30'),(65,'Kenneth Short','lowevickie@example.com','Ab(9LeGR','user',32,'2023-07-21 21:45:16'),(66,'Kristina Vargas','perkinsnichole@example.com','T@Sg1DTd','user',27,'2023-06-06 11:58:59'),(67,'Justin Davis','rebecca59@example.net','$b_s0Ewx','user',21,'2024-01-12 23:35:49'),(68,'Brian Graves','robertclark@example.net','j)K9V1ni','user',33,'2023-09-26 01:03:11'),(69,'Michelle Allen','maryhall@example.org','(331Wsql','user',35,'2024-11-13 02:14:48'),(70,'Denise Chaney','michele90@example.org','^6AXtFx3','user',32,'2024-06-21 12:51:23'),(71,'Francisco Powell','markvargas@example.com','$B8cHaCy','user',30,'2025-04-27 03:06:08'),(72,'Andrew Kelly','kristin86@example.org','%60&7lSv','user',35,'2024-11-19 20:35:11'),(73,'Lisa Martinez','gabrielle66@example.org','FT#7Bz+I','user',22,'2024-07-19 16:22:56'),(74,'Michael Scott','raymond91@example.com',')9C8asBe','user',19,'2024-01-31 11:48:13'),(75,'Wayne Bridges','janet81@example.net','^6JCsf_0','user',28,'2024-09-14 06:52:29'),(76,'Andrea Jones','zchristensen@example.net','+1X(NTf&','user',22,'2023-06-12 13:34:18'),(77,'Jorge Goodwin','amanda20@example.org','Ot$1Lx#3','user',21,'2023-06-05 10:04:43'),(78,'Timothy Dawson','cherryjoseph@example.net','&3VySJ1q','user',24,'2025-04-09 10:10:42'),(79,'Kelly Hernandez','tammy55@example.com','n@Yx6XPl','user',32,'2024-09-14 14:07:48'),(80,'Sierra Trevino DDS','cmueller@example.com','+S(*6CQn','user',23,'2024-06-07 20:21:11'),(81,'Julie Jimenez','ghess@example.org','D7!7GGwm','user',34,'2024-05-10 15:04:37'),(82,'Sarah Watkins MD','andrewobrien@example.com','n#e#9Y3g','user',21,'2023-09-18 13:38:40'),(83,'Jamie Navarro','kgonzalez@example.org','N)7MZ+mJ','user',23,'2025-04-04 06:08:49'),(84,'Beverly Lee','tamara62@example.com','^3@ZIEcL','user',33,'2024-11-25 09:05:51'),(85,'Justin Savage','theresa38@example.com','qX&1Aoqu','user',31,'2024-12-05 01:38:43'),(86,'Christine Hoffman','boyercourtney@example.com','6&k1anDa','user',33,'2023-08-16 05:36:51'),(87,'Jennifer Novak','hjenkins@example.net','+0gM9akX','user',23,'2025-04-02 08:41:02'),(88,'Erin Chen','wcummings@example.net','(tFB7GUm','user',21,'2024-10-01 05:29:37'),(89,'Christopher Grant','jonathan25@example.net','#8Gx^_ER','user',31,'2023-06-05 15:51:50'),(90,'Kristen Riley','omacias@example.com','z+#1DOxh','user',24,'2025-05-04 05:41:09'),(91,'Yolanda Grant','crawfordlindsay@example.net','uZ)Ka1Wx','user',24,'2023-11-27 02:56:39'),(92,'Stephanie White','ebrown@example.org','(1X5E&f$','user',24,'2024-11-03 01:09:06'),(93,'Marc Miller','hshelton@example.com','_0dYuv)p','user',20,'2023-06-26 23:14:22'),(94,'Gloria Mills','opowell@example.com','9(O%62Md','user',31,'2024-04-08 07:10:41'),(95,'Allison Kelly','ricardowest@example.com','_N!0yLe1','user',28,'2023-06-14 15:07:06'),(96,'Shaun Copeland','cainfrank@example.com','G#Z0HPg#','user',24,'2023-07-01 17:14:53'),(97,'Karen White','gnorris@example.net','^Oz8MQvE','user',26,'2024-07-15 12:49:00'),(98,'Brandon Castro','ashleyperez@example.org','Pe&6BelH','user',18,'2023-11-29 12:15:36'),(99,'Antonio King','samanthahorn@example.org','S@y$19Ko','user',19,'2024-11-25 05:17:22'),(100,'Zoe Navarro','brownbrenda@example.net','F*1v!QRp','user',34,'2023-10-17 23:32:34'),(101,'Carrie Blevins','rebecca90@example.com','P#9*CTCm','user',33,'2024-12-04 07:06:10'),(102,'Jeremy Caldwell','robert89@example.org','+3Zn18Ni','user',20,'2024-02-22 09:16:19'),(103,'Gregory Baker','evanschase@example.net','W$0E9Qwv','user',32,'2024-09-08 12:56:20');
/*!40000 ALTER TABLE `nguoidung` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 17:39:58
