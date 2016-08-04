-- MySQL dump 10.13  Distrib 5.7.10, for osx10.11 (x86_64)
--
-- Host: localhost    Database: cmdb_v1
-- ------------------------------------------------------
-- Server version	5.7.10

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
-- Table structure for table `AuthNode`
--

DROP TABLE IF EXISTS `AuthNode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AuthNode` (
  `uuid` char(32) NOT NULL,
  `auth` tinyint(1) NOT NULL,
  `datetime` datetime NOT NULL,
  `node_id` char(32) DEFAULT NULL,
  `user_name_id` int(11) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `AuthNode_c693ebc8` (`node_id`),
  KEY `AuthNode_f10400a0` (`user_name_id`),
  CONSTRAINT `AuthNode_node_id_1f87fa44f6684140_fk_assets_host_uuid` FOREIGN KEY (`node_id`) REFERENCES `assets_host` (`uuid`),
  CONSTRAINT `AuthNode_user_name_id_2f11b0adc9c83a00_fk_users_customuser_id` FOREIGN KEY (`user_name_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AuthNode`
--

LOCK TABLES `AuthNode` WRITE;
/*!40000 ALTER TABLE `AuthNode` DISABLE KEYS */;
/*!40000 ALTER TABLE `AuthNode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AuthSudo`
--

DROP TABLE IF EXISTS `AuthSudo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AuthSudo` (
  `uuid` char(32) NOT NULL,
  `groupname` varchar(64) NOT NULL,
  `shell` longtext NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AuthSudo`
--

LOCK TABLES `AuthSudo` WRITE;
/*!40000 ALTER TABLE `AuthSudo` DISABLE KEYS */;
/*!40000 ALTER TABLE `AuthSudo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_conftemplate`
--

DROP TABLE IF EXISTS `assets_conftemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_conftemplate` (
  `uuid` char(32) NOT NULL,
  `name` varchar(30) NOT NULL,
  `init_file` longtext NOT NULL,
  `template_file` longtext NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_conftemplate`
--

LOCK TABLES `assets_conftemplate` WRITE;
/*!40000 ALTER TABLE `assets_conftemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_conftemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_host`
--

DROP TABLE IF EXISTS `assets_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_host` (
  `uuid` char(32) NOT NULL,
  `node_name` varchar(100) DEFAULT NULL,
  `eth1` char(15) DEFAULT NULL,
  `eth2` char(15) DEFAULT NULL,
  `mac` varchar(20) DEFAULT NULL,
  `internal_ip` char(15) DEFAULT NULL,
  `brand` varchar(64) DEFAULT NULL,
  `cpu` varchar(64) DEFAULT NULL,
  `hard_disk` varchar(128) DEFAULT NULL,
  `memory` varchar(128) DEFAULT NULL,
  `system` varchar(32) DEFAULT NULL,
  `system_cpuarch` varchar(32) DEFAULT NULL,
  `system_version` varchar(8) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `guarantee_date` date DEFAULT NULL,
  `cabinet` varchar(32) DEFAULT NULL,
  `server_cabinet_id` int(11) DEFAULT NULL,
  `number` varchar(32) DEFAULT NULL,
  `editor` longtext,
  `status` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `Services_Code` varchar(16) DEFAULT NULL,
  `env` varchar(32) DEFAULT NULL,
  `room_number` varchar(32) DEFAULT NULL,
  `server_sn` varchar(32) DEFAULT NULL,
  `switch_port` varchar(12) DEFAULT NULL,
  `idle` tinyint(1) NOT NULL,
  `idc_id` char(32),
  `vm_id` char(32),
  PRIMARY KEY (`uuid`),
  KEY `assets_host_0869e37a` (`idc_id`),
  KEY `assets_host_0e0cecb8` (`vm_id`),
  CONSTRAINT `assets_host_idc_id_fc02f1e2acbbcc_fk_assets_idc_uuid` FOREIGN KEY (`idc_id`) REFERENCES `assets_idc` (`uuid`),
  CONSTRAINT `assets_host_vm_id_75080968af94dfe0_fk_assets_host_uuid` FOREIGN KEY (`vm_id`) REFERENCES `assets_host` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_host`
--

LOCK TABLES `assets_host` WRITE;
/*!40000 ALTER TABLE `assets_host` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_host_business`
--

DROP TABLE IF EXISTS `assets_host_business`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_host_business` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` char(32) NOT NULL,
  `project_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `host_id` (`host_id`,`project_id`),
  KEY `assets_host_business_8396f175` (`host_id`),
  KEY `assets_host_business_b098ad43` (`project_id`),
  CONSTRAINT `assets_host_b_project_id_7e1fdf33706676c3_fk_assets_project_uuid` FOREIGN KEY (`project_id`) REFERENCES `assets_project` (`uuid`),
  CONSTRAINT `assets_host_busines_host_id_185b5e5decf9451d_fk_assets_host_uuid` FOREIGN KEY (`host_id`) REFERENCES `assets_host` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_host_business`
--

LOCK TABLES `assets_host_business` WRITE;
/*!40000 ALTER TABLE `assets_host_business` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_host_business` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_host_service`
--

DROP TABLE IF EXISTS `assets_host_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_host_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` char(32) NOT NULL,
  `service_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `host_id` (`host_id`,`service_id`),
  KEY `assets_host_service_8396f175` (`host_id`),
  KEY `assets_host_service_b0dc1e29` (`service_id`),
  CONSTRAINT `assets_host_s_service_id_1f5ce3d13bb0764b_fk_assets_service_uuid` FOREIGN KEY (`service_id`) REFERENCES `assets_service` (`uuid`),
  CONSTRAINT `assets_host_service_host_id_660cc79feac0eb15_fk_assets_host_uuid` FOREIGN KEY (`host_id`) REFERENCES `assets_host` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_host_service`
--

LOCK TABLES `assets_host_service` WRITE;
/*!40000 ALTER TABLE `assets_host_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_host_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_hostrecord`
--

DROP TABLE IF EXISTS `assets_hostrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_hostrecord` (
  `uuid` char(32) NOT NULL,
  `user` varchar(30) DEFAULT NULL,
  `time` datetime NOT NULL,
  `content` longtext,
  `comment` longtext,
  `host_id` char(32) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `assets_hostrecord_8396f175` (`host_id`),
  CONSTRAINT `assets_hostrecord_host_id_3b740786ef5f690a_fk_assets_host_uuid` FOREIGN KEY (`host_id`) REFERENCES `assets_host` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_hostrecord`
--

LOCK TABLES `assets_hostrecord` WRITE;
/*!40000 ALTER TABLE `assets_hostrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_hostrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_idc`
--

DROP TABLE IF EXISTS `assets_idc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_idc` (
  `uuid` char(32) NOT NULL,
  `name` varchar(64) NOT NULL,
  `bandwidth` varchar(64) DEFAULT NULL,
  `phone` varchar(32) NOT NULL,
  `linkman` varchar(32) DEFAULT NULL,
  `address` varchar(128) DEFAULT NULL,
  `network` longtext,
  `create_time` date NOT NULL,
  `operator` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `comment` longtext,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_idc`
--

LOCK TABLES `assets_idc` WRITE;
/*!40000 ALTER TABLE `assets_idc` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_idc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_iplist`
--

DROP TABLE IF EXISTS `assets_iplist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_iplist` (
  `uuid` char(32) NOT NULL,
  `network` varchar(32) DEFAULT NULL,
  `ip` varchar(16) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `idc_id` char(32) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `assets_iplist_0869e37a` (`idc_id`),
  CONSTRAINT `assets_iplist_idc_id_4118d0827945673f_fk_assets_idc_uuid` FOREIGN KEY (`idc_id`) REFERENCES `assets_idc` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_iplist`
--

LOCK TABLES `assets_iplist` WRITE;
/*!40000 ALTER TABLE `assets_iplist` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_iplist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_line`
--

DROP TABLE IF EXISTS `assets_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_line` (
  `uuid` char(32) NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) DEFAULT NULL,
  `sort` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_line`
--

LOCK TABLES `assets_line` WRITE;
/*!40000 ALTER TABLE `assets_line` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_project`
--

DROP TABLE IF EXISTS `assets_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_project` (
  `uuid` char(32) NOT NULL,
  `service_name` varchar(60) DEFAULT NULL,
  `aliases_name` varchar(60) DEFAULT NULL,
  `description` longtext,
  `project_doc` longtext,
  `project_user_group` longtext,
  `sort` int(11) DEFAULT NULL,
  `line_id` char(32) DEFAULT NULL,
  `project_contact_id` int(11) NOT NULL,
  `project_contact_backup_id` int(11) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `assets_project_line_id_3271c84b6deb8f1f_fk_assets_line_uuid` (`line_id`),
  KEY `assets_project_087d62fc` (`project_contact_id`),
  KEY `assets_project_227d338f` (`project_contact_backup_id`),
  CONSTRAINT `asset_project_contact_id_55a9a08f4b924c8c_fk_users_customuser_id` FOREIGN KEY (`project_contact_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `assets_project_line_id_3271c84b6deb8f1f_fk_assets_line_uuid` FOREIGN KEY (`line_id`) REFERENCES `assets_line` (`uuid`),
  CONSTRAINT `d46f719c8dcde971d1e0990f038ba85a` FOREIGN KEY (`project_contact_backup_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_project`
--

LOCK TABLES `assets_project` WRITE;
/*!40000 ALTER TABLE `assets_project` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_projectuser`
--

DROP TABLE IF EXISTS `assets_projectuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_projectuser` (
  `uuid` char(32) NOT NULL,
  `data_created` datetime NOT NULL,
  `env` varchar(100) DEFAULT NULL,
  `project_id` char(32) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `assets_projec_project_id_298fad6d989e9c44_fk_assets_project_uuid` (`project_id`),
  KEY `assets_projectuser_e8701ad4` (`user_id`),
  CONSTRAINT `assets_projec_project_id_298fad6d989e9c44_fk_assets_project_uuid` FOREIGN KEY (`project_id`) REFERENCES `assets_project` (`uuid`),
  CONSTRAINT `assets_projectus_user_id_53f8464903c02003_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_projectuser`
--

LOCK TABLES `assets_projectuser` WRITE;
/*!40000 ALTER TABLE `assets_projectuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_projectuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_service`
--

DROP TABLE IF EXISTS `assets_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_service` (
  `uuid` char(32) NOT NULL,
  `name` varchar(30) NOT NULL,
  `port` int(11) DEFAULT NULL,
  `remark` longtext,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_service`
--

LOCK TABLES `assets_service` WRITE;
/*!40000 ALTER TABLE `assets_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets_zabbixrecord`
--

DROP TABLE IF EXISTS `assets_zabbixrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets_zabbixrecord` (
  `uuid` char(32) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `info` longtext,
  `time` datetime NOT NULL,
  `comment` longtext,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets_zabbixrecord`
--

LOCK TABLES `assets_zabbixrecord` WRITE;
/*!40000 ALTER TABLE `assets_zabbixrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `assets_zabbixrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_ssh_audit`
--

DROP TABLE IF EXISTS `audit_ssh_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_ssh_audit` (
  `uuid` char(32) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `bash_shell` longtext NOT NULL,
  `audit_data_time` datetime NOT NULL,
  `server_ip` char(15) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_ssh_audit`
--

LOCK TABLES `audit_ssh_audit` WRITE;
/*!40000 ALTER TABLE `audit_ssh_audit` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_ssh_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add 部门组',6,'add_departmentgroup'),(17,'Can change 部门组',6,'change_departmentgroup'),(18,'Can delete 部门组',6,'delete_departmentgroup'),(19,'Can add 部门',7,'add_department_mode'),(20,'Can change 部门',7,'change_department_mode'),(21,'Can delete 部门',7,'delete_department_mode'),(22,'Can add user',8,'add_customuser'),(23,'Can change user',8,'change_customuser'),(24,'Can delete user',8,'delete_customuser'),(25,'Can add 日志记录',9,'add_server_auth'),(26,'Can change 日志记录',9,'change_server_auth'),(27,'Can delete 日志记录',9,'delete_server_auth'),(28,'Can add 产品线',10,'add_line'),(29,'Can change 产品线',10,'change_line'),(30,'Can delete 产品线',10,'delete_line'),(31,'Can add 业务',11,'add_project'),(32,'Can change 业务',11,'change_project'),(33,'Can delete 业务',11,'delete_project'),(34,'Can add IDC机房',12,'add_idc'),(35,'Can change IDC机房',12,'change_idc'),(36,'Can delete IDC机房',12,'delete_idc'),(37,'Can add 发布系统',13,'add_publishing_system'),(38,'Can change 发布系统',13,'change_publishing_system'),(39,'Can delete 发布系统',13,'delete_publishing_system'),(40,'Can add 业务管理人员',14,'add_projectuser'),(41,'Can change 业务管理人员',14,'change_projectuser'),(42,'Can delete 业务管理人员',14,'delete_projectuser'),(43,'Can add 服务',15,'add_service'),(44,'Can change 服务',15,'change_service'),(45,'Can delete 服务',15,'delete_service'),(46,'Can add 服务器',16,'add_host'),(47,'Can change 服务器',16,'change_host'),(48,'Can delete 服务器',16,'delete_host'),(49,'Can add host record',17,'add_hostrecord'),(50,'Can change host record',17,'change_hostrecord'),(51,'Can delete host record',17,'delete_hostrecord'),(52,'Can add git仓库',18,'add_gitcode'),(53,'Can change git仓库',18,'change_gitcode'),(54,'Can delete git仓库',18,'delete_gitcode'),(55,'Can add 项目发布',19,'add_project_swan'),(56,'Can change 项目发布',19,'change_project_swan'),(57,'Can delete 项目发布',19,'delete_project_swan'),(58,'Can add zabbix record',20,'add_zabbixrecord'),(59,'Can change zabbix record',20,'change_zabbixrecord'),(60,'Can delete zabbix record',20,'delete_zabbixrecord'),(61,'Can add ip list',21,'add_iplist'),(62,'Can change ip list',21,'change_iplist'),(63,'Can delete ip list',21,'delete_iplist'),(64,'Can add 模板文件',22,'add_conftemplate'),(65,'Can change 模板文件',22,'change_conftemplate'),(66,'Can delete 模板文件',22,'delete_conftemplate'),(67,'Can add salt操作日志',23,'add_salt_api_log'),(68,'Can change salt操作日志',23,'change_salt_api_log'),(69,'Can delete salt操作日志',23,'delete_salt_api_log'),(70,'Can add salt_conf',24,'add_salt_conf'),(71,'Can change salt_conf',24,'change_salt_conf'),(72,'Can delete salt_conf',24,'delete_salt_conf'),(73,'Can add 配置推送记录',25,'add_setuplog'),(74,'Can change 配置推送记录',25,'change_setuplog'),(75,'Can delete 配置推送记录',25,'delete_setuplog'),(76,'Can add 操作记录',26,'add_operationlog'),(77,'Can change 操作记录',26,'change_operationlog'),(78,'Can delete 操作记录',26,'delete_operationlog'),(79,'Can add rpm包名',27,'add_salt_mode_name'),(80,'Can change rpm包名',27,'change_salt_mode_name'),(81,'Can delete rpm包名',27,'delete_salt_mode_name'),(82,'Can add apply',28,'add_apply'),(83,'Can change apply',28,'change_apply'),(84,'Can delete apply',28,'delete_apply'),(85,'Can add 发布日志',29,'add_swanlog'),(86,'Can change 发布日志',29,'change_swanlog'),(87,'Can delete 发布日志',29,'delete_swanlog'),(88,'Can add 审计',30,'add_ssh_audit'),(89,'Can change 审计',30,'change_ssh_audit'),(90,'Can delete 审计',30,'delete_ssh_audit'),(91,'Can add 角色管理',31,'add_auth_group'),(92,'Can change 角色管理',31,'change_auth_group'),(93,'Can delete 角色管理',31,'delete_auth_group'),(94,'Can add 权限管理',32,'add_user_auth_cmdb'),(95,'Can change 权限管理',32,'change_user_auth_cmdb'),(96,'Can delete 权限管理',32,'delete_user_auth_cmdb'),(97,'Can add sudo授权',33,'add_authsudo'),(98,'Can change sudo授权',33,'change_authsudo'),(99,'Can delete sudo授权',33,'delete_authsudo'),(100,'Can add 主机权限',34,'add_authnode'),(101,'Can change 主机权限',34,'change_authnode'),(102,'Can delete 主机权限',34,'delete_authnode'),(103,'Can add 故障管理',35,'add_incident'),(104,'Can change 故障管理',35,'change_incident'),(105,'Can delete 故障管理',35,'delete_incident'),(106,'Can add http监控',36,'add_monitorhttp'),(107,'Can change http监控',36,'change_monitorhttp'),(108,'Can delete http监控',36,'delete_monitorhttp'),(109,'Can add http监控日志',37,'add_monitorhttplog'),(110,'Can change http监控日志',37,'change_monitorhttplog'),(111,'Can delete http监控日志',37,'delete_monitorhttplog'),(112,'Can add mysql监控',38,'add_monitormysql'),(113,'Can change mysql监控',38,'change_monitormysql'),(114,'Can delete mysql监控',38,'delete_monitormysql');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_auth_auth_group`
--

DROP TABLE IF EXISTS `cmdb_auth_auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_auth_auth_group` (
  `uuid` char(32) NOT NULL,
  `group_name` varchar(100) NOT NULL,
  `enable` tinyint(1) NOT NULL,
  `explanation` longtext NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `group_name` (`group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_auth_auth_group`
--

LOCK TABLES `cmdb_auth_auth_group` WRITE;
/*!40000 ALTER TABLE `cmdb_auth_auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_auth_auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_auth_auth_group_group_user`
--

DROP TABLE IF EXISTS `cmdb_auth_auth_group_group_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_auth_auth_group_group_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auth_group_id` char(32) NOT NULL,
  `customuser_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_id` (`auth_group_id`,`customuser_id`),
  KEY `cmdb_auth_auth_group_group_user_af3f5f04` (`auth_group_id`),
  KEY `cmdb_auth_auth_group_group_user_721e74b0` (`customuser_id`),
  CONSTRAINT `cmdb_auth__customuser_id_33ec160b6f4a2e93_fk_users_customuser_id` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `cmdb_auth_group_id_19c331db012ad2d9_fk_cmdb_auth_auth_group_uuid` FOREIGN KEY (`auth_group_id`) REFERENCES `cmdb_auth_auth_group` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_auth_auth_group_group_user`
--

LOCK TABLES `cmdb_auth_auth_group_group_user` WRITE;
/*!40000 ALTER TABLE `cmdb_auth_auth_group_group_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_auth_auth_group_group_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmdb_auth_user_auth_cmdb`
--

DROP TABLE IF EXISTS `cmdb_auth_user_auth_cmdb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmdb_auth_user_auth_cmdb` (
  `uuid` char(32) NOT NULL,
  `select_host` tinyint(1) NOT NULL,
  `edit_host` tinyint(1) NOT NULL,
  `update_host` tinyint(1) NOT NULL,
  `add_host` tinyint(1) NOT NULL,
  `bat_add_host` tinyint(1) NOT NULL,
  `delete_host` tinyint(1) NOT NULL,
  `add_line_auth` tinyint(1) NOT NULL,
  `auth_project` tinyint(1) NOT NULL,
  `auth_highstate` tinyint(1) NOT NULL,
  `add_user` tinyint(1) NOT NULL,
  `edit_user` tinyint(1) NOT NULL,
  `edit_pass` tinyint(1) NOT NULL,
  `delete_user` tinyint(1) NOT NULL,
  `add_department` tinyint(1) NOT NULL,
  `select_idc` tinyint(1) NOT NULL,
  `add_idc` tinyint(1) NOT NULL,
  `edit_idc` tinyint(1) NOT NULL,
  `del_idc` tinyint(1) NOT NULL,
  `setup_system` tinyint(1) NOT NULL,
  `upload_system` tinyint(1) NOT NULL,
  `salt_keys` tinyint(1) NOT NULL,
  `project_auth` tinyint(1) NOT NULL,
  `add_project` tinyint(1) NOT NULL,
  `edit_project` tinyint(1) NOT NULL,
  `delete_project` tinyint(1) NOT NULL,
  `auth_log` tinyint(1) NOT NULL,
  `cmdb_log` tinyint(1) NOT NULL,
  `server_audit` tinyint(1) NOT NULL,
  `group_name_id` char(32) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `cmdb_auth_user_auth_cmdb_e074f38c` (`group_name_id`),
  CONSTRAINT `cmdb_group_name_id_40e2c7660ed38540_fk_cmdb_auth_auth_group_uuid` FOREIGN KEY (`group_name_id`) REFERENCES `cmdb_auth_auth_group` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmdb_auth_user_auth_cmdb`
--

LOCK TABLES `cmdb_auth_user_auth_cmdb` WRITE;
/*!40000 ALTER TABLE `cmdb_auth_user_auth_cmdb` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmdb_auth_user_auth_cmdb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'部门组','users','departmentgroup'),(7,'部门','users','department_mode'),(8,'user','users','customuser'),(9,'日志记录','users','server_auth'),(10,'产品线','assets','line'),(11,'业务','assets','project'),(12,'IDC机房','assets','idc'),(13,'发布系统','assets','publishing_system'),(14,'业务管理人员','assets','projectuser'),(15,'服务','assets','service'),(16,'服务器','assets','host'),(17,'host record','assets','hostrecord'),(18,'git仓库','assets','gitcode'),(19,'项目发布','assets','project_swan'),(20,'zabbix record','assets','zabbixrecord'),(21,'ip list','assets','iplist'),(22,'模板文件','assets','conftemplate'),(23,'salt操作日志','salt_ui','salt_api_log'),(24,'salt_conf','salt_ui','salt_conf'),(25,'配置推送记录','salt_ui','setuplog'),(26,'操作记录','salt_ui','operationlog'),(27,'rpm包名','salt_ui','salt_mode_name'),(28,'apply','swan','apply'),(29,'发布日志','swan','swanlog'),(30,'审计','audit','ssh_audit'),(31,'角色管理','cmdb_auth','auth_group'),(32,'权限管理','cmdb_auth','user_auth_cmdb'),(33,'sudo授权','cmdb_auth','authsudo'),(34,'主机权限','cmdb_auth','authnode'),(35,'故障管理','malfunction','incident'),(36,'http监控','monitor','monitorhttp'),(37,'http监控日志','monitor','monitorhttplog'),(38,'mysql监控','monitor','monitormysql');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-08-04 18:15:22'),(2,'auth','0001_initial','2016-08-04 18:15:23'),(3,'users','0001_initial','2016-08-04 18:15:23'),(4,'admin','0001_initial','2016-08-04 18:15:23'),(5,'assets','0001_initial','2016-08-04 18:15:24'),(6,'audit','0001_initial','2016-08-04 18:15:24'),(7,'cmdb_auth','0001_initial','2016-08-04 18:15:25'),(8,'malfunction','0001_initial','2016-08-04 18:15:25'),(9,'monitor','0001_initial','2016-08-04 18:15:25'),(10,'salt_ui','0001_initial','2016-08-04 18:15:26'),(11,'sessions','0001_initial','2016-08-04 18:15:26'),(12,'swan','0001_initial','2016-08-04 18:15:26'),(13,'swan','0002_auto_20151229_1313','2016-08-04 18:15:26'),(14,'swan','0003_auto_20160112_1536','2016-08-04 18:15:26'),(15,'swan','0004_auto_20160112_1538','2016-08-04 18:15:26'),(16,'swan','0005_auto_20160112_1539','2016-08-04 18:15:26'),(17,'swan','0006_auto_20160112_1615','2016-08-04 18:15:26'),(18,'swan','0007_auto_20160112_1620','2016-08-04 18:15:26'),(19,'swan','0008_auto_20160112_1624','2016-08-04 18:15:26'),(20,'swan','0009_auto_20160804_1812','2016-08-04 18:15:26'),(21,'swan','0010_auto_20160804_1814','2016-08-04 18:15:26');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('02ztex1eu4g0c0c0gekbv8ov6nryjmf0','MGZhNGNkZDM0NTE3YzU5NzVkYjIwYzA5MzAyMWE2ZDNjYmE1NWQ3ODp7ImZ1bl9hdXRoIjp7fSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMTUzMzIwZTRkYTIxNWE0M2Q2M2QxNTYyY2YxZjBkODNiMTE0ZjA2IiwiX2F1dGhfdXNlcl9pZCI6MSwiX3Nlc3Npb25fZXhwaXJ5IjoyODgwMH0=','2016-08-05 02:17:48');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gitCode`
--

DROP TABLE IF EXISTS `gitCode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gitCode` (
  `uuid` char(32) NOT NULL,
  `codePath` varchar(64) NOT NULL,
  `codeserver` varchar(64) NOT NULL,
  `codeFqdn` varchar(64) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gitCode`
--

LOCK TABLES `gitCode` WRITE;
/*!40000 ALTER TABLE `gitCode` DISABLE KEYS */;
/*!40000 ALTER TABLE `gitCode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incident`
--

DROP TABLE IF EXISTS `incident`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incident` (
  `uuid` char(32) NOT NULL,
  `title` varchar(256) NOT NULL,
  `ip` char(15) DEFAULT NULL,
  `url` longtext,
  `projectuser` varchar(32) NOT NULL,
  `closeuser` varchar(32) DEFAULT NULL,
  `source` int(11) NOT NULL,
  `starttime` datetime NOT NULL,
  `scantime` datetime DEFAULT NULL,
  `stoptime` datetime DEFAULT NULL,
  `mailcomment` longtext NOT NULL,
  `status` int(11) NOT NULL,
  `classical` tinyint(1) NOT NULL,
  `grade` int(11) DEFAULT NULL,
  `comment` longtext NOT NULL,
  `project_principal` varchar(32) DEFAULT NULL,
  `incident_user` varchar(32) DEFAULT NULL,
  `createtime` datetime NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incident`
--

LOCK TABLES `incident` WRITE;
/*!40000 ALTER TABLE `incident` DISABLE KEYS */;
/*!40000 ALTER TABLE `incident` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitor_monitorhttp`
--

DROP TABLE IF EXISTS `monitor_monitorhttp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitor_monitorhttp` (
  `uuid` char(32) NOT NULL,
  `title` varchar(120) NOT NULL,
  `url` longtext NOT NULL,
  `monitor_type` tinyint(1) NOT NULL,
  `monitor_ip` longtext NOT NULL,
  `mail_status` tinyint(1) NOT NULL,
  `mail` longtext NOT NULL,
  `weixin_status` tinyint(1) NOT NULL,
  `weixin` longtext NOT NULL,
  `payload` longtext,
  `status` tinyint(1) NOT NULL,
  `result_code` tinyint(1) NOT NULL,
  `createtime` datetime NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitor_monitorhttp`
--

LOCK TABLES `monitor_monitorhttp` WRITE;
/*!40000 ALTER TABLE `monitor_monitorhttp` DISABLE KEYS */;
/*!40000 ALTER TABLE `monitor_monitorhttp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitor_monitorhttplog`
--

DROP TABLE IF EXISTS `monitor_monitorhttplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitor_monitorhttplog` (
  `uuid` char(32) NOT NULL,
  `monitorId` varchar(120) NOT NULL,
  `monitor_title` varchar(120) NOT NULL,
  `content` longtext,
  `code` int(11) NOT NULL,
  `job_id` varchar(32) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `createtime` datetime NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitor_monitorhttplog`
--

LOCK TABLES `monitor_monitorhttplog` WRITE;
/*!40000 ALTER TABLE `monitor_monitorhttplog` DISABLE KEYS */;
/*!40000 ALTER TABLE `monitor_monitorhttplog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitor_monitormysql`
--

DROP TABLE IF EXISTS `monitor_monitormysql`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitor_monitormysql` (
  `uuid` char(32) NOT NULL,
  `name` varchar(120) NOT NULL,
  `monitor_ip` longtext NOT NULL,
  `monitor_user` varchar(32) NOT NULL,
  `monitor_pass` varchar(128) NOT NULL,
  `monitor_port` int(11) NOT NULL,
  `mail` longtext NOT NULL,
  `weixin` longtext NOT NULL,
  `slave` tinyint(1) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `createtime` datetime NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitor_monitormysql`
--

LOCK TABLES `monitor_monitormysql` WRITE;
/*!40000 ALTER TABLE `monitor_monitormysql` DISABLE KEYS */;
/*!40000 ALTER TABLE `monitor_monitormysql` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_swan`
--

DROP TABLE IF EXISTS `project_swan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_swan` (
  `uuid` char(32) NOT NULL,
  `swan_name` varchar(100) NOT NULL,
  `code_name` varchar(100) NOT NULL,
  `choose` varchar(10) NOT NULL,
  `check_port_status` tinyint(1) NOT NULL,
  `check_port` varchar(30) DEFAULT NULL,
  `bat_push` int(11) NOT NULL,
  `tgt` longtext,
  `argall_str` varchar(20) DEFAULT NULL,
  `tomcat_init` varchar(128) DEFAULT NULL,
  `cache` longtext,
  `git_code_user` varchar(12) DEFAULT NULL,
  `code_path` varchar(128) DEFAULT NULL,
  `git_user` varchar(12) DEFAULT NULL,
  `git_pass` varchar(64) DEFAULT NULL,
  `shell` varchar(128) DEFAULT NULL,
  `shell_status` tinyint(1) NOT NULL,
  `CheckUrl` varchar(200) DEFAULT NULL,
  `datetime` datetime NOT NULL,
  `git_code_id` char(32) DEFAULT NULL,
  `project_name_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  KEY `project_swan_5890d2d4` (`git_code_id`),
  KEY `project_swan_6fa54945` (`project_name_id`),
  CONSTRAINT `project__project_name_id_7f50db0e92eba344_fk_assets_project_uuid` FOREIGN KEY (`project_name_id`) REFERENCES `assets_project` (`uuid`),
  CONSTRAINT `project_swan_git_code_id_108333599249714f_fk_gitCode_uuid` FOREIGN KEY (`git_code_id`) REFERENCES `gitCode` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_swan`
--

LOCK TABLES `project_swan` WRITE;
/*!40000 ALTER TABLE `project_swan` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_swan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_swan_node`
--

DROP TABLE IF EXISTS `project_swan_node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_swan_node` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_swan_id` char(32) NOT NULL,
  `host_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_swan_id` (`project_swan_id`,`host_id`),
  KEY `project_swan_node_a3e2b54e` (`project_swan_id`),
  KEY `project_swan_node_8396f175` (`host_id`),
  CONSTRAINT `project_sw_project_swan_id_4814a3a6ff88c636_fk_project_swan_uuid` FOREIGN KEY (`project_swan_id`) REFERENCES `project_swan` (`uuid`),
  CONSTRAINT `project_swan_node_host_id_633f2c729f485d77_fk_assets_host_uuid` FOREIGN KEY (`host_id`) REFERENCES `assets_host` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_swan_node`
--

LOCK TABLES `project_swan_node` WRITE;
/*!40000 ALTER TABLE `project_swan_node` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_swan_node` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_swan_push_user`
--

DROP TABLE IF EXISTS `project_swan_push_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_swan_push_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_swan_id` char(32) NOT NULL,
  `customuser_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_swan_id` (`project_swan_id`,`customuser_id`),
  KEY `project_swan_push_user_a3e2b54e` (`project_swan_id`),
  KEY `project_swan_push_user_721e74b0` (`customuser_id`),
  CONSTRAINT `project_sw_customuser_id_3822f6570ff53a30_fk_users_customuser_id` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `project_swa_project_swan_id_79291c907c649f9_fk_project_swan_uuid` FOREIGN KEY (`project_swan_id`) REFERENCES `project_swan` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_swan_push_user`
--

LOCK TABLES `project_swan_push_user` WRITE;
/*!40000 ALTER TABLE `project_swan_push_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_swan_push_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `push_system`
--

DROP TABLE IF EXISTS `push_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `push_system` (
  `uuid` char(32) NOT NULL,
  `project_name` int(11) NOT NULL,
  `push_url` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `push_system`
--

LOCK TABLES `push_system` WRITE;
/*!40000 ALTER TABLE `push_system` DISABLE KEYS */;
/*!40000 ALTER TABLE `push_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salt_ui_operationlog`
--

DROP TABLE IF EXISTS `salt_ui_operationlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `salt_ui_operationlog` (
  `uuid` char(32) NOT NULL,
  `content` longtext NOT NULL,
  `mail_list` longtext,
  `mail_title` varchar(100) NOT NULL,
  `date_created` datetime NOT NULL,
  `mail_status` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `salt_ui_operationlog_e8701ad4` (`user_id`),
  CONSTRAINT `salt_ui_operatio_user_id_69db0895519a6008_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salt_ui_operationlog`
--

LOCK TABLES `salt_ui_operationlog` WRITE;
/*!40000 ALTER TABLE `salt_ui_operationlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `salt_ui_operationlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salt_ui_salt_api_log`
--

DROP TABLE IF EXISTS `salt_ui_salt_api_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `salt_ui_salt_api_log` (
  `uuid` char(32) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `minions` varchar(2048) NOT NULL,
  `jobs_id` varchar(40) DEFAULT NULL,
  `stalt_type` varchar(20) NOT NULL,
  `salt_len_node` int(11) NOT NULL,
  `stalt_input` varchar(100) DEFAULT NULL,
  `api_return` longtext NOT NULL,
  `log_time` datetime NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salt_ui_salt_api_log`
--

LOCK TABLES `salt_ui_salt_api_log` WRITE;
/*!40000 ALTER TABLE `salt_ui_salt_api_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `salt_ui_salt_api_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salt_ui_salt_conf`
--

DROP TABLE IF EXISTS `salt_ui_salt_conf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `salt_ui_salt_conf` (
  `uuid` char(32) NOT NULL,
  `server_name` varchar(20) NOT NULL,
  `prod_name` varchar(20) NOT NULL,
  `file_name` varchar(20) NOT NULL,
  `server_code` longtext NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salt_ui_salt_conf`
--

LOCK TABLES `salt_ui_salt_conf` WRITE;
/*!40000 ALTER TABLE `salt_ui_salt_conf` DISABLE KEYS */;
/*!40000 ALTER TABLE `salt_ui_salt_conf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salt_ui_salt_mode_name`
--

DROP TABLE IF EXISTS `salt_ui_salt_mode_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `salt_ui_salt_mode_name` (
  `uuid` char(32) NOT NULL,
  `sls_name` varchar(20) NOT NULL,
  `sls_description` longtext,
  `sls_conf` int(11) DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salt_ui_salt_mode_name`
--

LOCK TABLES `salt_ui_salt_mode_name` WRITE;
/*!40000 ALTER TABLE `salt_ui_salt_mode_name` DISABLE KEYS */;
/*!40000 ALTER TABLE `salt_ui_salt_mode_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salt_ui_setuplog`
--

DROP TABLE IF EXISTS `salt_ui_setuplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `salt_ui_setuplog` (
  `uuid` char(32) NOT NULL,
  `content` longtext NOT NULL,
  `status` int(11) NOT NULL,
  `approve_time` datetime DEFAULT NULL,
  `reject_reason` longtext,
  `date_created` datetime NOT NULL,
  `run_time` datetime DEFAULT NULL,
  `approve_user_id` int(11) DEFAULT NULL,
  `business_id` char(32) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`uuid`),
  KEY `salt_ui_setuplog_549dea8c` (`approve_user_id`),
  KEY `salt_ui_setuplog_2f4e4ac4` (`business_id`),
  KEY `salt_ui_setuplog_e8701ad4` (`user_id`),
  CONSTRAINT `salt_ui__approve_user_id_6c1570f72dd3c666_fk_users_customuser_id` FOREIGN KEY (`approve_user_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `salt_ui_setu_business_id_3f48417490749bc5_fk_assets_project_uuid` FOREIGN KEY (`business_id`) REFERENCES `assets_project` (`uuid`),
  CONSTRAINT `salt_ui_setuplog_user_id_23d803f7d2e28ce0_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salt_ui_setuplog`
--

LOCK TABLES `salt_ui_setuplog` WRITE;
/*!40000 ALTER TABLE `salt_ui_setuplog` DISABLE KEYS */;
/*!40000 ALTER TABLE `salt_ui_setuplog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `swan_apply`
--

DROP TABLE IF EXISTS `swan_apply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `swan_apply` (
  `uuid` char(32) NOT NULL,
  `applyer` varchar(32) DEFAULT NULL,
  `project_name` varchar(20) DEFAULT NULL,
  `module_name` varchar(200) DEFAULT NULL,
  `module_type` int(10) unsigned DEFAULT NULL,
  `module_tgt` varchar(50) DEFAULT NULL,
  `qa` varchar(20) DEFAULT NULL,
  `op` varchar(20) DEFAULT NULL,
  `comment` longtext,
  `status` int(10) unsigned DEFAULT NULL,
  `date_added` datetime,
  `date_one` datetime DEFAULT NULL,
  `date_ended` datetime DEFAULT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `swan_apply`
--

LOCK TABLES `swan_apply` WRITE;
/*!40000 ALTER TABLE `swan_apply` DISABLE KEYS */;
/*!40000 ALTER TABLE `swan_apply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `swan_swanlog`
--

DROP TABLE IF EXISTS `swan_swanlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `swan_swanlog` (
  `uuid` char(32) NOT NULL,
  `username` varchar(32) DEFAULT NULL,
  `userID` varchar(128) DEFAULT NULL,
  `project_name` varchar(20) DEFAULT NULL,
  `project_uuid` varchar(64) DEFAULT NULL,
  `module_name` varchar(200) DEFAULT NULL,
  `module_args` varchar(32) DEFAULT NULL,
  `swan_datetime` datetime,
  `status` tinyint(1) NOT NULL,
  `message` longtext,
  `swan_name` varchar(64),
  `update_log` longtext,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `swan_swanlog`
--

LOCK TABLES `swan_swanlog` WRITE;
/*!40000 ALTER TABLE `swan_swanlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `swan_swanlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_customuser`
--

DROP TABLE IF EXISTS `users_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_customuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `mobile` varchar(30) NOT NULL,
  `session_key` varchar(60) DEFAULT NULL,
  `user_key` longtext,
  `menu_status` tinyint(1) NOT NULL,
  `user_active` tinyint(1) NOT NULL,
  `uuid` varchar(64) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  `department_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `users_customuser_bf691be4` (`department_id`),
  CONSTRAINT `users_department_id_7ef5db15268629e1_fk_users_department_mode_id` FOREIGN KEY (`department_id`) REFERENCES `users_department_mode` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_customuser`
--

LOCK TABLES `users_customuser` WRITE;
/*!40000 ALTER TABLE `users_customuser` DISABLE KEYS */;
INSERT INTO `users_customuser` VALUES (1,'pbkdf2_sha256$15000$QB5LTIl6eIf9$jjaVteipcNOHk5Kx7bdK7xZVb9r3/FergltFteUq6+I=','2016-08-04 18:17:40',1,'voilet@qq.com','admin','1','1','','02ztex1eu4g0c0c0gekbv8ov6nryjmf0',NULL,1,0,'',1,1,'2016-08-04 18:15:57',NULL);
/*!40000 ALTER TABLE `users_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_customuser_groups`
--

DROP TABLE IF EXISTS `users_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_customuser_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customuser_id` (`customuser_id`,`group_id`),
  KEY `users_customuser_groups_721e74b0` (`customuser_id`),
  KEY `users_customuser_groups_0e939a4f` (`group_id`),
  CONSTRAINT `users_cust_customuser_id_3ff7151cd75e2907_fk_users_customuser_id` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `users_customuser_grou_group_id_7bd979d963ceefdb_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_customuser_groups`
--

LOCK TABLES `users_customuser_groups` WRITE;
/*!40000 ALTER TABLE `users_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_customuser_user_permissions`
--

DROP TABLE IF EXISTS `users_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_customuser_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customuser_id` (`customuser_id`,`permission_id`),
  KEY `users_customuser_user_permissions_721e74b0` (`customuser_id`),
  KEY `users_customuser_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `users_custo_permission_id_26c8d8c42be54c0a_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_custom_customuser_id_cd602244af3539_fk_users_customuser_id` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_customuser_user_permissions`
--

LOCK TABLES `users_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_department_mode`
--

DROP TABLE IF EXISTS `users_department_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_department_mode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `department_name` varchar(64) DEFAULT NULL,
  `description` longtext,
  `desc_gid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_department_mode`
--

LOCK TABLES `users_department_mode` WRITE;
/*!40000 ALTER TABLE `users_department_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_department_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_departmentgroup`
--

DROP TABLE IF EXISTS `users_departmentgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_departmentgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `department_groups_name` varchar(64) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_departmentgroup`
--

LOCK TABLES `users_departmentgroup` WRITE;
/*!40000 ALTER TABLE `users_departmentgroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_departmentgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_server_auth`
--

DROP TABLE IF EXISTS `users_server_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_server_auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_ip` char(15) DEFAULT NULL,
  `user_name` varchar(20) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `auth_weights` tinyint(1) NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_server_auth`
--

LOCK TABLES `users_server_auth` WRITE;
/*!40000 ALTER TABLE `users_server_auth` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_server_auth` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-04 18:18:54
