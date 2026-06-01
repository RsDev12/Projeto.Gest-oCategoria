-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: GestaoCategoria
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Categoria`
--

DROP TABLE IF EXISTS `Categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Categoria` (
  `idCategoria` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `idCategoria_pai` int(11) DEFAULT NULL,
  `descricao` varchar(255) DEFAULT NULL,
  `statusCategoria` varchar(20) DEFAULT 'ativo',
  `imagem` varchar(255) DEFAULT 'default.jpg',
  PRIMARY KEY (`idCategoria`),
  KEY `fk_categoria_pai` (`idCategoria_pai`),
  CONSTRAINT `fk_categoria_pai` FOREIGN KEY (`idCategoria_pai`) REFERENCES `Categoria` (`idCategoria`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Categoria`
--

LOCK TABLES `Categoria` WRITE;
/*!40000 ALTER TABLE `Categoria` DISABLE KEYS */;
INSERT INTO `Categoria` VALUES (10,'Escolar',NULL,'Materias escolares','ativo','default.jpg'),(11,'Mochila de estudante',10,'Mochila de estudante','ativo','default.jpg'),(12,'Esportes',NULL,'Categoria voltada para Esporte','ativo','default.jpg'),(13,'Bola de futebol',12,'SubCategoria voltada para os produtos de Bola de futebol','ativo','default.jpg'),(14,'Bola de basquete',12,'','ativo','default.jpg'),(15,'Beleza',NULL,'Categoria voltada para produtos de beleza','ativo','default.jpg'),(16,'Maquiagem',15,'Subcategoria que pertence a categoria pai \"Beleza\", sendo voltada para produtos de maquiagem','ativo','default.jpg'),(17,'Tecnologia',NULL,'Categoria voltada para produtos de tecnologia','ativo','default.jpg'),(18,'Smart Tv',17,'Categoria filha, que faz parte da categoria tecnologia','ativo','default.jpg');
/*!40000 ALTER TABLE `Categoria` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-24 20:33:56
