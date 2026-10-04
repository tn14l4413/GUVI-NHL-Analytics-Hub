-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: hockeyteam
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `nhl_teams`
--

DROP TABLE IF EXISTS `nhl_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhl_teams` (
  `team_id` int NOT NULL AUTO_INCREMENT,
  `team_abbrev` varchar(10) NOT NULL,
  `team_name` varchar(100) NOT NULL,
  `conference_name` varchar(50) DEFAULT NULL,
  `division_name` varchar(50) DEFAULT NULL,
  `logo_url` text,
  PRIMARY KEY (`team_id`),
  UNIQUE KEY `team_abbrev` (`team_abbrev`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhl_teams`
--

LOCK TABLES `nhl_teams` WRITE;
/*!40000 ALTER TABLE `nhl_teams` DISABLE KEYS */;
INSERT INTO `nhl_teams` VALUES (1,'COL','Colorado Avalanche','Western','Central','https://assets.nhle.com/logos/nhl/svg/COL_light.svg'),(2,'CAR','Carolina Hurricanes','Eastern','Metropolitan','https://assets.nhle.com/logos/nhl/svg/CAR_light.svg'),(3,'DAL','Dallas Stars','Western','Central','https://assets.nhle.com/logos/nhl/svg/DAL_light.svg'),(4,'BUF','Buffalo Sabres','Eastern','Atlantic','https://assets.nhle.com/logos/nhl/svg/BUF_light.svg'),(5,'TBL','Tampa Bay Lightning','Eastern','Atlantic','https://assets.nhle.com/logos/nhl/svg/TBL_light.svg'),(6,'MTL','Montréal Canadiens','Eastern','Atlantic','https://assets.nhle.com/logos/nhl/svg/MTL_light.svg'),(7,'MIN','Minnesota Wild','Western','Central','https://assets.nhle.com/logos/nhl/svg/MIN_light.svg'),(8,'BOS','Boston Bruins','Eastern','Atlantic','https://assets.nhle.com/logos/nhl/svg/BOS_light.svg?season=20252026'),(9,'OTT','Ottawa Senators','Eastern','Atlantic','https://assets.nhle.com/logos/nhl/svg/OTT_light.svg'),(10,'PIT','Pittsburgh Penguins','Eastern','Metropolitan','https://assets.nhle.com/logos/nhl/svg/PIT_light.svg'),(11,'PHI','Philadelphia Flyers','Eastern','Metropolitan','https://assets.nhle.com/logos/nhl/svg/PHI_light.svg'),(12,'WSH','Washington Capitals','Eastern','Metropolitan','https://assets.nhle.com/logos/nhl/svg/WSH_secondary_light.svg'),(13,'VGK','Vegas Golden Knights','Western','Pacific','https://assets.nhle.com/logos/nhl/svg/VGK_light.svg'),(14,'EDM','Edmonton Oilers','Western','Pacific','https://assets.nhle.com/logos/nhl/svg/EDM_light.svg'),(15,'UTA','Utah Mammoth','Western','Central','https://assets.nhle.com/logos/nhl/svg/UTA_light.svg?season=20252026'),(16,'DET','Detroit Red Wings','Eastern','Atlantic','https://assets.nhle.com/logos/nhl/svg/DET_light.svg?season=20252026'),(17,'CBJ','Columbus Blue Jackets','Eastern','Metropolitan','https://assets.nhle.com/logos/nhl/svg/CBJ_light.svg'),(18,'ANA','Anaheim Ducks','Western','Pacific','https://assets.nhle.com/logos/nhl/svg/ANA_light.svg'),(19,'NYI','New York Islanders','Eastern','Metropolitan','https://assets.nhle.com/logos/nhl/svg/NYI_light.svg'),(20,'LAK','Los Angeles Kings','Western','Pacific','https://assets.nhle.com/logos/nhl/svg/LAK_light.svg'),(21,'NJD','New Jersey Devils','Eastern','Metropolitan','https://assets.nhle.com/logos/nhl/svg/NJD_light.svg'),(22,'STL','St. Louis Blues','Western','Central','https://assets.nhle.com/logos/nhl/svg/STL_light.svg?season=20252026'),(23,'NSH','Nashville Predators','Western','Central','https://assets.nhle.com/logos/nhl/svg/NSH_light.svg'),(24,'SJS','San Jose Sharks','Western','Pacific','https://assets.nhle.com/logos/nhl/svg/SJS_light.svg'),(25,'FLA','Florida Panthers','Eastern','Atlantic','https://assets.nhle.com/logos/nhl/svg/FLA_light.svg'),(26,'WPG','Winnipeg Jets','Western','Central','https://assets.nhle.com/logos/nhl/svg/WPG_light.svg'),(27,'SEA','Seattle Kraken','Western','Pacific','https://assets.nhle.com/logos/nhl/svg/SEA_light.svg'),(28,'TOR','Toronto Maple Leafs','Eastern','Atlantic','https://assets.nhle.com/logos/nhl/svg/TOR_light.svg'),(29,'CGY','Calgary Flames','Western','Pacific','https://assets.nhle.com/logos/nhl/svg/CGY_light.svg'),(30,'NYR','New York Rangers','Eastern','Metropolitan','https://assets.nhle.com/logos/nhl/svg/NYR_light.svg'),(31,'CHI','Chicago Blackhawks','Western','Central','https://assets.nhle.com/logos/nhl/svg/CHI_light.svg?season=20252026'),(32,'VAN','Vancouver Canucks','Western','Pacific','https://assets.nhle.com/logos/nhl/svg/VAN_light.svg');
/*!40000 ALTER TABLE `nhl_teams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-04  8:16:53
