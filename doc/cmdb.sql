/*
SQLyog v10.2 
MySQL - 5.5.46-log : Database - cmdb_v2
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`cmdb_v2` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `cmdb_v2`;

/*Table structure for table `AuthNode` */

DROP TABLE IF EXISTS `AuthNode`;

CREATE TABLE `AuthNode` (
	  `uuid` char(32) NOT NULL,
	  `user_name_id` int(11) NOT NULL,
	  `node_id` char(32) DEFAULT NULL,
	  `auth` tinyint(1) NOT NULL,
	  `datetime` datetime NOT NULL,
	  PRIMARY KEY (`uuid`),
	  KEY `AuthNode_3e838ccb` (`user_name_id`),
	  KEY `AuthNode_e453c5c5` (`node_id`),
	  CONSTRAINT `user_name_id_refs_id_d1ce95fe` FOREIGN KEY (`user_name_id`) REFERENCES `users_customuser` (`id`),
	  CONSTRAINT `node_id_refs_uuid_def1f9a0` FOREIGN KEY (`node_id`) REFERENCES `assets_host` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `AuthNode` */

/*Table structure for table `AuthSudo` */

DROP TABLE IF EXISTS `AuthSudo`;

CREATE TABLE `AuthSudo` (
	  `uuid` char(32) NOT NULL,
	  `groupname` varchar(64) NOT NULL,
	  `shell` longtext NOT NULL,
	  `datetime` datetime NOT NULL,
	  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `AuthSudo` */

/*Table structure for table `assets_conftemplate` */

DROP TABLE IF EXISTS `assets_conftemplate`;

CREATE TABLE `assets_conftemplate` (
	  `uuid` char(32) NOT NULL,
	  `name` varchar(30) NOT NULL,
	  `init_file` longtext NOT NULL,
	  `template_file` longtext NOT NULL,
	  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `assets_conftemplate` */

/*Table structure for table `assets_host` */

DROP TABLE IF EXISTS `assets_host`;

CREATE TABLE `assets_host` (
	  `uuid` char(32) NOT NULL,
	  `node_name` varchar(100) DEFAULT NULL,
	  `idc_id` char(32) DEFAULT NULL,
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
	  `vm_id` char(32) DEFAULT NULL,
	  `type` int(11) NOT NULL,
	  `Services_Code` varchar(16) DEFAULT NULL,
	  `env` varchar(32) DEFAULT NULL,
	  `room_number` varchar(32) DEFAULT NULL,
	  `server_sn` varchar(32) DEFAULT NULL,
	  `switch_port` varchar(12) DEFAULT NULL,
	  `idle` tinyint(1) NOT NULL,
	  PRIMARY KEY (`uuid`),
	  KEY `assets_host_7f604875` (`idc_id`),
	  KEY `assets_host_528edfa9` (`vm_id`),
	  CONSTRAINT `idc_id_refs_uuid_8e0b1de6` FOREIGN KEY (`idc_id`) REFERENCES `assets_idc` (`uuid`),
	  CONSTRAINT `vm_id_refs_uuid_fcb04db2` FOREIGN KEY (`vm_id`) REFERENCES `assets_host` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `assets_host` */

/*Table structure for table `assets_host_business` */

DROP TABLE IF EXISTS `assets_host_business`;

CREATE TABLE `assets_host_business` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `host_id` char(32) NOT NULL,
	  `project_id` char(32) NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `host_id` (`host_id`,`project_id`),
	  KEY `assets_host_business_27f00f5d` (`host_id`),
	  KEY `assets_host_business_37952554` (`project_id`),
	  CONSTRAINT `host_id_refs_uuid_ddd7b8fd` FOREIGN KEY (`host_id`) REFERENCES `assets_host` (`uuid`),
	  CONSTRAINT `project_id_refs_uuid_294be64b` FOREIGN KEY (`project_id`) REFERENCES `assets_project` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `assets_host_business` */

/*Table structure for table `assets_host_service` */

DROP TABLE IF EXISTS `assets_host_service`;

CREATE TABLE `assets_host_service` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `host_id` char(32) NOT NULL,
	  `service_id` char(32) NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `host_id` (`host_id`,`service_id`),
	  KEY `assets_host_service_27f00f5d` (`host_id`),
	  KEY `assets_host_service_91a0ac17` (`service_id`),
	  CONSTRAINT `host_id_refs_uuid_10499861` FOREIGN KEY (`host_id`) REFERENCES `assets_host` (`uuid`),
	  CONSTRAINT `service_id_refs_uuid_b1448f84` FOREIGN KEY (`service_id`) REFERENCES `assets_service` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `assets_host_service` */

/*Table structure for table `assets_hostrecord` */

DROP TABLE IF EXISTS `assets_hostrecord`;

CREATE TABLE `assets_hostrecord` (
	  `uuid` char(32) NOT NULL,
	  `host_id` char(32) NOT NULL,
	  `user` varchar(30) DEFAULT NULL,
	  `time` datetime NOT NULL,
	  `content` longtext,
	  `comment` longtext,
	  PRIMARY KEY (`uuid`),
	  KEY `assets_hostrecord_27f00f5d` (`host_id`),
	  CONSTRAINT `host_id),
  KEY `assets_iplist_7f604875` (`idc_id`),
  CONSTRAINT `idc_id_refs_uuid_8cb7b050` FOREIGN KEY (`idc_id`) REFERENCES `assets_idc` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `assets_iplist` */

/*Table structure for table `assets_line` */

DROP TABLE IF EXISTS `assets_line`;

CREATE TAES `users_customuser` (`id`),
  CONSTRAINT `line_id_refs_uuid_ba3db459` FOREIGN KEY (`line_id`) REFERENCES `assets_line` (`uuid`),
  CONSTRAINT `project_contact_id_refs_id_7de991c6` FOREIGN KEY (`project_contact_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `assets_project` */

/*Table structure for table `assets_projectuser` */

DROP TABLE IF EXISTS `assets_projectuser`;

CREATE TABLE `assets_projectuser` (
	  `uuid` char(32) NOT NULL,
	  `project_id` char(32) NOT NULL,
	  `user_id` int(11) DEFAULT NULL,
	  `data_created` datetime NOT NULL,
	  `env` varchar(100) DEFAULT NULL,
	  PRIMARY KEY (`uuid`),
	  KEY `project_id_refs_uuid_ff6360a0` (`project_id`),
	  KEY `assets_projectuser_6340c63c` (`user_id`),
	  CONSTRAINT `user_id_refs_id_f339c929` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`),
	  CONSTRAINT `project_id_refs_uuid_ff6360a0` FOREIGN KEY (`project_id`) REFERENCES `assets_project` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `assets_projectuser` */

/*Table structure for table `assets_service` */

DROP TABLE IF EXISTS `assets_service`;

CREATE TABLE `assets_service` (
	  `uuid` char(32) NOT NULL,
	  `name` varchar(30) NOT NULL,
	  `port` int(11) DEFAULT NULL,
	  `remark` longtext,
	  PRIMARY KEY (`uuid`),
	  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `assets_service` */

/*Table structure for table `assets_zabbixrecord` */

DROP TABLE IF EXISTS `assets_zabbixrecord`;

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

/*Data for the table `assets_zabbixrecord` */

/*Table structure for table `audit_ssh_audit` */

DROP TABLE IF EXISTS `audit_ssh_au_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `name` varchar(50) NOT NULL,
	  `content_type_id` int(11) NOT NULL,
	  `codename` varchar(100) NOT NULL,
	  PRIMARY d session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add 部门组',6,'add_departmentgroup'),(17,'Can change 部门组',6,'change_departmentgroup'),(18,'Can delete 部门组',6,'delete_departmentgroup'),(19,'Can add 部门',7,'add_department_mode'),(20,'Can change 部门',7,'change_department_mode'),(21,'Can delete 部门',7,'delete_department_mode'),(22,'Can add user',8,'add_customuser'),(23,'Can change user',8,'change_customuser'),(24,'Can delete user',8,'delete_customuser'),(25,'Can add 日志记录',9,'add_server_auth'),(26,'Can change 日志记录',9,'change_server_auth'),(27,'Can delete 日志记录',9,'delete_server_auth'),(28,'Can add 产品线',10,'add_line'),(29,'cord',17,'change_hostrecord'),(51,'Can delete host record',17,'delete_hostrecord'),(52,'Can add git仓库',18,'add_gitcode'),(53,'Can change git仓库',18,'change_gitcode'),(54,'Can delete git仓库',18,'delete_gitcode'),(55,'Can add 项目发布',19,'add_project_swan'),(56,'Can change 项目发布',19,'change_project_swan'),(57,'Can delete 项目发布',19,'delete_project_swan'),(58,'Can add zabbix record',20,'add_zabbixrecord'),(59,'Can change zabbix record',20,'change_zabbixrecord'),(60,'Can delete zabbix record',20,'delete_zabbixrecord'),(61,'Can add ip list',21,'add_iplist'),(62,'Can change ip list',21,'change_iplist'),(63,'Can delete ip list',21,'delete_iplist'),(64,'Can add 模板文件',22,'add_conftemplate'),(65,'Can change 模板文件',22,'change_conftemplate'),(66,'Can delete 模板文件',22,'delete_conftemplate'),(67,'Can add salt操作日志',23,'add_salt_api_log'),(68,'Can change salt操作日志',23,'change_salt_api_log'),(69,'Can delete salt操作日志',23,'delete_salt_api_lelete_ssh_audit'),(91,'Can add 角色管理',31,'add_auth_group'),(92,'Can change 角色管理',31,'change_auth_group'),(93,'Can delete 角色管理',31,'delete_auth_group'),(94,'Can add 权限管理',32,'add_user_auth_cmdb'),(95,'Can change 权限管理',32,'change_user_auth_cmdb'),(96,'Can delete 权限管理',32,'delete_user_auth_cmdb'),(97,'Can add sudo授权',33,'add_authsudo'),(98,'Can change sudo授权',33,'change_authsudo'),(99,'Can delete sudo授权',33,'delete_authsudo'),(100,'Can add 主机权限',34,'add_authnode'),(101,'Can change 主机权限',34,'change_authnode'),(102,'Can delete 主机权限',34,'delete_authnode'),(103,'Can add 故障管理',35,'add_incident'),(104,'Can change 故障管理',35,'change_incident'),(105,'Can delete 故障管理',35,'delete_incident'),(106,'Can add http监控',36,'add_monitorhttp'),(107,'Can change http监控',36,'change_monitorhttp'),(108,'Can delete http监控',36,'delete_monitorhttp'),(109,'Can add http监控日志',37,'add_monitorhttplog'),(110,'Can change http监控日志',37,'change_monitorhttplog'),(11h_group_id`,`customuser_id`),
  KEY `cmdb_auth_auth_group_group_user_64ff69ae` (`auth_group_id`),
  KEY `cmdb_auth_auth_group_group_user_a110e492` (`customuser_id`),
  CONSTRAINT `auth_group_id_refs_uuid_01ddcd3c` FOREIGN KEY (`auth_group_id`) REFERENCES `cmdb_auth_auth_group` (`uuid`),
  CONSTRAINT `customuser_id_refs_id_a1e35508` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/l`,`model`) values (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'部门组','users','departmentgroup'),(7,'部门','users','department_mode'),(8,'user','users','customuser'),(9,'日志记录','users','server_auth'),(10,'产品线','assets','line'),(11,'业务','assets','project'),(12,'IDC机房','assets','idc'),(13,'发布系统','assets','publishing_system'),(1,'monitormysql');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `app` varchar(255) NOT NULL,
	  `name` varchar(255) NOT NULL,
	  `applied` datetime NOT NULL,
	  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values (1,'contenttypes','0001_initial','2016-08-04 13:50:45'),(2,'admin','0001_initial','2016-08-04 13:50:47'),(3,'auth','0001_initial','2016-08-04 13:50:49'),(4,'sessions','0001_initial','2016-08-04 13:50:49');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
	  `session_key` varchar(40) NOT NULL,
	  `session_data` longtext NOT NULL,
	  `expire_date` datetime NOT NULL,
	  PRIMARY KEY (`session_key`),
	  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `django_session` */

/*Table structure for table `gitCode` */

DROP TABLE IF EXISTS `gitCode`;

CREATE TABLE `gitCode` (
	  `uuid` char(32) NOT NULL,
	  `codePath` varchar(64) NOT NULL,
	  `codeserver` varchar(64) NOT NULL,
	  `codeFqdn` varchar(64) NOT NULL,
	  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `gitCode` */

/*Table structure for table `incident` */

DROP TABLE IF EXISTS `incident`;

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

/*Data for the table `incident` */

/*Table structure for table `monitor_monitorhttp` */

DROP TABLE IF EXISTS `monitor_monitorhttp`;

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

/*Data for the table `monitor_monitorhttp` */

/*Table structure for table `monitor_monitorhttplog` */

DROP TABLE IF EXISTS `monitor_monitorhttplog`;

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

/*Data for the table `monitor_monitorhttplog` */

/*Table structure for table `monitor_monitormysql` */

DROP TABLE IF EXISTS `monitor_monitormysql`;

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

/*Data for the table `monitor_monitormysql` */

/*Table structure for table `project_swan` */

DROP TABLE IF EXISTS `project_swan`;

CREATE TABLE `project_swan` (
	  `uuid` char(32) NOT NULL,
	  `swan_name` varchar(100) NOT NULL,
	  `code_name` varchar(100) NOT NULL,
	  `project_name_id` char(32) DEFAULT NULL,
	  `choose` varchar(10) NOT NULL,
	  `check_port_status` tinyint(1) NOT NULL,
	  `check_port` varchar(30) DEFAULT NULL,
	  `bat_push` int(11) NOT NULL,
	  (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `project_swan_id` c`project_swan_id_refs_uuid_f652869d` FOREIGN KEY (`project_swan_id`) REFERENCES `project_swan` (`uuid`),
		  CONSTRAINT `customuser_id_refs_id_536aadf0` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;

	/*Data for the table `project_swan_push_user` */

	/*Table structure for table `push_system` */

	DROP TABLE IF EXISTS `push_system`;

	CREATE TABLE `push_system` (
		  `uuid` char(32) NOT NULL,
		  `project_name` int(11) NOT NULL,
		  `push_url` varchar(100) DEFAULT NULL,
		  PRIMARY KEY (`uuid`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;

	/*Data for the table `push_system` */

	/*Table structure for table `salt_ui_operationlog` */

	DROP TABLE IF ERY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `salt_ui_salt_api_log` */

/*Table structure for table `salt_ui_salt_conf` */

DROP TABLE IF EXISTS `salt_ui_salt_conf`;

CREATE TABLE `salt_ui_salt_conf` (
	  `uuid` char(32) NOT NULL,
	  `server_name` varchar(20) NOT NULL,
	  `prod_name` vadatetime DEFAULT NULL,
	  PRIMARY KEY (`uuid`),
	  KEY `salt_ui_setuplog_6340c63c` (`user_id`),
	  KEY `salt_ui_setuplog_de174412` (`approve_user_id`),
	  KEY `salt_ui_setuplog_311726d6` (`business_id`),
	  CONSTRAINT `approve_user_id_refs_id_9fc17a54` FOREIGN KEY (`approve_user_id`) REFERENCES `users_customuser` (`id`),
	  CONSTRAINT `business_id_refs_uuid_cd262c01` FOREIGN KEY (`business_id`) REFERENCES `assets_project` (`uuid`),
	  CONSTRAINT `user_id_refs_id_9fc17a54` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `salt_ui_setuplog` */

/*Table structure for table `swan_apply` */

DROP TABLE IF EXISTS `swan_apply`;

CREATE TABLE `swan_apply` (
	  `uuid` char(32) NOT NULL,
	  `applyer` varchar(32) DEFAULT NULL,
	  `project_name` varchar(20) D DEFAULT NULL,
	  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `swan_swanlog` */

/*Table structure for table `users_customuser` */

DROP TABLE IF EXISTS `users_customuser`;

CREATE TABLE `users_customuser` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `password` varchar(128) NOT NULL,
	  `last_login` datetime NOT NULL,
	  `is_superuser` tinyint(1) NOT NULL,
	  `email` varchar(254) NOT NULL,
	  `username` varchar(30) NOT NULL,
	  `first_name` varchar(30) NOT NULL,
	  `last_name` varchar(30) NOT NULL,
	  `department_id` int(11) DEFAULT NULL,
	  `mobile` varchar(30) NOT NULL,
	  `session_key` varchar(60) DEFAULT NULL,
	  `user_key` longtext,
	  `menu_status` tinyint(1) NOT NULL,
	  `user_active` tinyint(1) NOT NULL,
	  `uuid` varchar(64) NOT NULL,
	  `is_staff` tinyint(1) NOT NULL,
	  `is_active` tinyint(1) NOT NULL,
	  `date_joined` datetime NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `email` (`email`),
	  UNIQUE KEY `username` (`username`),
	  UNIQUE KEY `uuid` (`uuid`),
	  KEY `users_customuser_69d14838` (`department_id`),
	  CONSTRAINT `department_id_refs_id_c1027f86` FOREIGN KEY (`department_id`) REFERENCES `users_department_mode` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `users_customuser` */

/*Table structure for table `users_customuser_groups` */

DROP TABLE IF EXISTS `users_customuser_groups`;

CREATE TABLE `users_customuser_groups` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `customuser_id` int(11) NOT NULL,
	  `group_id` int(11) NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `customuser_id` (`customuser_id`,`group_id`),
	  KEY `users_customuser_groups_a110e492` (`customuser_id`),
	  KEY `users_customuser_groups_5f412f9a` (`group_id`),
	  CONSTRAINT `customuser_id_refs_id_87477e43` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `users_customuser_groups` */

/*Table structure for table `users_customuser_user_permissions` */

DROP TABLE IF EXISTS `users_customuser_user_permissions`;

CREATE TABLE `users_customuser_user_permissions` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `customuser_id` int(11) NOT NULL,
	  `permission_id` int(11) NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `customuser_id` (`customuser_id`,`permission_id`),
	  KEY `users_customuser_user_permissions_a110e492` (`customuser_id`),
	  KEY `users_customuser_user_permissions_83d7f98b` (`permission_id`),
	  CONSTRAINT `customuser_id_refs_id_55fe159d` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHAp` char(15) DEFAULT NULL,
  `user_name` varchar(20) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `auth_weights` tinyint(1) NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the 
