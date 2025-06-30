CREATE DATABASE  IF NOT EXISTS `mobileservice_n7` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `mobileservice_n7`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: mobileservice_n7
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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (10,'nguyenvana','12',1),(11,'tranthib','nJjwIGCuL4',1),(12,'levanc','WVTADVyson',1),(13,'phamthid','12345678',1),(14,'hoangminhe','12345678',0),(15,'vungocf','12345678',1),(16,'ngothig','12345678',1),(17,'dangvanh','12345678',0),(18,'lythii','12345678',1),(19,'trinhcongj','12345678',1),(20,'0912345678','12345678',1),(21,'0933221144','12345678',1),(22,'0909888777','12345678',1),(23,'0988997766','12345678',0),(24,'0977886655','12345678',1),(25,'0123456789','12345678',1),(26,'0123456788','12345678',1),(28,'0329518648','0329518648',1),(29,'0375648394555','0375648394555',1),(31,'09332211444444','09332211444444',1),(32,'0933221144444','0933221144444',0),(33,'09332211444442','09332211444442',0),(34,'09332','09332',1),(36,'0184638394','0184638394',1),(37,'0483766486','0483766486',1),(38,'04837664863','04837664863',1),(41,'048376648','048376648',1),(44,'04837664','04837664',1),(46,'0385647483','0385647483',1),(47,'0578736485','0578736485',1),(48,'0578736488','0578736488',1),(49,'0483648576','0483648576',1),(50,'0329618363','0329618363',1),(52,'0912345679','0912345679',1),(53,'tranhatđong-123456789101','s1cRqP0Hys',1),(54,'tranhatđong-123456788787','pzEsrrqp6B',1);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_accounts_is_active_sync_contracts` AFTER UPDATE ON `accounts` FOR EACH ROW BEGIN
    DECLARE v_subscriber_id INT;

    -- Chỉ xử lý khi có thay đổi is_active
    IF OLD.is_active != NEW.is_active THEN

        -- Lấy subscriber_id tương ứng
        SELECT id INTO v_subscriber_id
        FROM subscribers
        WHERE account_id = NEW.id
        LIMIT 1;

        -- Nếu tồn tại subscriber_id thì xử lý
        IF v_subscriber_id IS NOT NULL THEN

            -- Nếu account bị khóa thì cập nhật hợp đồng đang hoạt động
            IF NEW.is_active = 0 THEN
                UPDATE contracts
                SET is_active = 0,
                    end_date = NOW()
                WHERE subscriber_id = v_subscriber_id AND is_active = 1;

            -- Nếu account được mở lại thì kích hoạt lại hợp đồng gần nhất (nếu chưa có cái nào đang hoạt động)
            ELSE
                IF NOT EXISTS (
                    SELECT 1 FROM contracts
                    WHERE subscriber_id = v_subscriber_id AND is_active = 1
                ) THEN
                    UPDATE contracts
                    SET is_active = 1,
                        end_date = NULL
                    WHERE subscriber_id = v_subscriber_id
                    ORDER BY start_date DESC
                    LIMIT 1;
                END IF;
            END IF;

        END IF;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `contracts`
--

DROP TABLE IF EXISTS `contracts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contracts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `contents` text,
  `title` varchar(255) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `subscriber_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `contracts_ibfk_1_idx` (`subscriber_id`),
  CONSTRAINT `contracts_ibfk_1` FOREIGN KEY (`subscriber_id`) REFERENCES `subscribers` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contracts`
--

LOCK TABLES `contracts` WRITE;
/*!40000 ALTER TABLE `contracts` DISABLE KEYS */;
INSERT INTO `contracts` VALUES (1,'2025-01-18 14:55:06','Hợp đồng sử dụng dịch vụ cho thuê bao 6','Hợp đồng thuê bao #6','2025-01-18','2025-06-15',0,6),(2,'2024-11-15 14:55:06','Hợp đồng sử dụng dịch vụ cho thuê bao 7','Hợp đồng thuê bao #7','2024-11-15','2025-08-20',1,7),(3,'2024-08-16 14:55:06','Hợp đồng sử dụng dịch vụ cho thuê bao 8','Hợp đồng thuê bao #8','2024-08-16','2025-07-16',1,8),(4,'2024-11-29 14:55:06','Hợp đồng sử dụng dịch vụ cho thuê bao 9','Hợp đồng thuê bao #9','2024-11-29','2025-01-19',1,9),(5,'2024-09-21 14:55:06','Hợp đồng sử dụng dịch vụ cho thuê bao 10','Hợp đồng thuê bao #10','2024-09-21','2025-03-15',1,10),(6,'2024-12-08 14:55:06','Hợp đồng sử dụng dịch vụ cho thuê bao 11','Hợp đồng thuê bao #11','2024-12-08','2025-10-30',1,11),(7,'2024-08-23 14:55:06','Hợp đồng sử dụng dịch vụ cho thuê bao 12','Hợp đồng thuê bao #12','2024-08-23','2025-05-22',1,12),(11,'2025-04-16 16:30:47','Chi tiết hợp đồng hợp tác đại lý cấp 1','Hợp đồng đại lý 2024','2024-01-01','2025-06-15',0,6),(12,'2025-04-16 16:30:47','Cam kết phân phối SIM số đẹp','Hợp đồng bán SIM đặc biệt','2024-03-01','2025-04-25',0,7),(13,'2025-04-16 16:30:47','Gia hạn thêm 6 tháng với các điều khoản mới','Gia hạn hợp đồng cung cấp dịch vụ','2024-07-01','2025-06-15',0,6),(14,'2025-04-16 16:30:47','Thông báo chấm dứt hợp đồng từ ngày 01/05/2024','Hợp đồng chấm dứt','2024-04-01',NULL,1,8),(15,'2025-04-16 16:30:47','Hợp đồng truyền thông và quảng cáo trên nền tảng số','Thỏa thuận hợp tác quảng bá','2024-02-15',NULL,1,9),(16,'2025-04-22 23:43:29','\r\nHỢP ĐỒNG ĐĂNG KÝ THUÊ BAO TRẢ TRƯỚC\r\n\r\nĐiều 1: Phạm vi hợp đồng  \r\nKhách hàng đăng ký thuê bao di động trả trước với các điều kiện và quyền lợi được quy định trong hợp đồng này.\r\n\r\nĐiều 2: Quyền lợi của khách hàng  \r\n- Được sử dụng dịch vụ thoại, nhắn tin, dữ liệu theo gói cước đã đăng ký.  \r\n- Không bị ràng buộc thanh toán định kỳ, sử dụng đến đâu trả tiền đến đó.\r\n\r\nĐiều 3: Nghĩa vụ của khách hàng  \r\n- Nạp tiền vào tài khoản thuê bao để duy trì dịch vụ.  \r\n- Tuân thủ các quy định sử dụng dịch vụ của nhà mạng.\r\n\r\nĐiều 4: Hiệu lực hợp đồng  \r\nHợp đồng có hiệu lực kể từ ngày ký và áp dụng cho toàn bộ thời gian sử dụng thuê bao trả trước.\r\n\r\nĐiều 5: Chấm dứt hợp đồng  \r\nKhách hàng có thể tự động chấm dứt hợp đồng bằng cách không sử dụng hoặc yêu cầu nhà mạng hủy thuê bao.\r\n\r\n(Ký tên và đóng dấu)\r\n','Hợp đồng đăng ký thuê bao trả trước','2025-04-24',NULL,0,6),(17,'2025-04-22 23:45:03','\r\nHỢP ĐỒNG ĐĂNG KÝ THUÊ BAO TRẢ SAU\r\n\r\nĐiều 1: Phạm vi hợp đồng  \r\nKhách hàng đăng ký thuê bao di động trả sau với các điều kiện và cam kết thanh toán định kỳ.\r\n\r\nĐiều 2: Quyền lợi của khách hàng  \r\n- Được sử dụng dịch vụ thoại, nhắn tin, dữ liệu theo gói cước đã đăng ký.  \r\n- Được nhận hóa đơn thanh toán hàng tháng với các khoản phí sử dụng dịch vụ.\r\n\r\nĐiều 3: Nghĩa vụ của khách hàng  \r\n- Thanh toán đầy đủ, đúng hạn các khoản phí dịch vụ theo hóa đơn.  \r\n- Tuân thủ các quy định sử dụng dịch vụ và chính sách của nhà mạng.\r\n\r\nĐiều 4: Hiệu lực hợp đồng  \r\nHợp đồng có hiệu lực từ ngày ký và kéo dài theo thời gian cam kết hoặc cho đến khi chấm dứt.\r\n\r\nĐiều 5: Chấm dứt hợp đồng  \r\nKhách hàng có thể chấm dứt hợp đồng theo quy định hoặc khi hết hạn hợp đồng.\r\n\r\n(Ký tên và đóng dấu)\r\n','Hợp đồng đăng ký thuê bao trả sau','2025-04-25','2025-04-25',0,7),(23,'2025-06-15 11:24:23',NULL,NULL,'2025-06-15',NULL,1,14),(24,'2025-06-15 11:35:42',NULL,NULL,'2025-06-15',NULL,1,15),(25,'2025-06-15 11:38:52',NULL,NULL,'2025-06-15',NULL,1,16),(26,'2025-06-15 11:45:12',NULL,NULL,'2025-06-15','2025-06-16',0,17),(27,'2025-06-15 11:52:56',NULL,NULL,'2025-06-15','2025-06-16',0,18),(28,'2025-06-15 11:54:59',NULL,NULL,'2025-06-15',NULL,1,19),(29,'2025-06-15 11:55:09',NULL,NULL,'2025-06-15',NULL,1,20),(30,'2025-06-15 12:07:17',NULL,NULL,'2025-06-15',NULL,1,21),(31,'2025-06-15 12:14:32',NULL,NULL,'2025-06-15',NULL,1,22),(32,'2025-06-15 12:18:05',NULL,NULL,'2025-06-15',NULL,1,23),(33,'2025-06-15 12:23:07',NULL,NULL,'2025-06-15',NULL,1,24),(34,'2025-06-15 12:24:52',NULL,NULL,'2025-06-15',NULL,1,25),(35,'2025-06-15 12:25:50',NULL,NULL,'2025-06-15',NULL,1,26),(36,'2025-06-15 12:28:43',NULL,NULL,'2025-06-15',NULL,1,27),(37,'2025-06-15 13:05:34',NULL,NULL,'2025-06-15',NULL,1,28),(38,'2025-06-16 11:38:56','điều khoản','gdga','2025-06-19',NULL,1,6);
/*!40000 ALTER TABLE `contracts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `countries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `country_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `country_name` (`country_name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countries`
--

LOCK TABLES `countries` WRITE;
/*!40000 ALTER TABLE `countries` DISABLE KEYS */;
INSERT INTO `countries` VALUES (12,'Canada'),(4,'Hàn Quốc'),(2,'Hoa Kỳ'),(3,'Nhật Bản'),(1,'Việt Nam');
/*!40000 ALTER TABLE `countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `card_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_id` (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Tô Thương',1,'012345678901'),(2,'Nguyễn Văn A',1,'012345678902'),(3,'Trần Thị B',1,'012345678903'),(4,'Lê Văn C',1,'012345678904'),(5,'Phạm Thị D',0,'012345678905'),(6,'Ngô Minh E',1,'012345678906'),(7,'Tô Thương',1,'012345678909');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `functions`
--

DROP TABLE IF EXISTS `functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `functions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `function_name` varchar(255) NOT NULL,
  `syntax_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `functions`
--

LOCK TABLES `functions` WRITE;
/*!40000 ALTER TABLE `functions` DISABLE KEYS */;
INSERT INTO `functions` VALUES (1,'Xem danh sách thuê bao','VIEW_SUBSCRIBERS'),(2,'Thêm thuê bao','ADD_SUBSCRIBER'),(3,'Sửa thông tin thuê bao','EDIT_SUBSCRIBER'),(4,'Xóa thuê bao','DELETE_SUBSCRIBER'),(5,'Gia hạn gói cước','RENEW_SUBSCRIPTION'),(6,'Hủy thuê bao','CANCEL_SUBSCRIPTION'),(7,'Xem gói cước','VIEW_PLANS'),(8,'Đăng kí gói cước','create_subscription'),(9,'Xem hóa đơn','VIEW_PAYMENTS'),(10,'Xem logs sử dụng','VIEW_USAGE_LOGS'),(11,'Đăng xuất','logout'),(12,'Xem thông tin thuê bao','view_subscriber'),(13,'Xem trang cách hình thức thanh toán','index_payment_api'),(14,'Trừ tiền tài khoản gốc thuê bao','deduct_balance'),(15,'Lấy thông tin thuê bao','get_subscriber'),(16,'Thanh toán hóa đơn','create_payment'),(17,'Thêm ưu đãi cho hóa đơn','create_payment_detail'),(18,'Yêu cầu thanh toán PayPal','pay_paypal'),(19,'Lấy kết quả thanh toán PayPal','payment_paypal_execute'),(20,'Trả về kết quả thanh toán QRCode','payment_result'),(21,'Xem danh sách tài khoản','get_all_accounts'),(22,'Thêm tài khoản','create_account'),(23,'Sửa tài khoản','update_account'),(24,'Xem chi tiết tài khoản','get_account_by_id'),(25,'Khóa tài khoản','delete_account'),(26,'Truy cập trang admin','admin_index'),(27,'Truy cập trang quản lý hợp đồng','index_contracts'),(28,'Xem danh sách hợp đông','get_all_contracts'),(29,'Xem chi tiết hợp đồng','get_contract_by_id'),(30,'Tạo hợp đồng','create_contract'),(31,'Sửa hợp đồng','update_contract'),(32,'Hủy hợp đồng','delete_contract'),(33,'Truy cập trang quản lý đất nước','index_countries'),(34,'Xem danh sách đất nước','get_all_countries'),(35,'Xem chi tiết đất nước','get_country_by_id'),(36,'Tạo đất nước','create_country'),(37,'Sửa đất nước','update_country'),(38,'Xóa đất nước','delete_country'),(39,'Xem danh sách khách hàng','get_all_customers'),(40,'Xem chi tiết khách hàng','get_customer_by_id'),(41,'Thêm khách hàng','create_customer'),(42,'Sửa khách hàng','update_customer'),(43,'Truy cập trang quản lý mạng','index_networks'),(44,'Xem danh sách mạng','get_all_networks'),(45,'Xem chi tiết mạng','get_network_by_id'),(46,'Thêm mạng','create_network'),(47,'Sửa mạng','update_network'),(48,'Xóa mạng','delete_network'),(49,'Tạo gói cước','create_plan'),(50,'Sửa gói cước','update_plan'),(51,'Khóa gói cước','lock_plan'),(52,'Xem báo cáo danh thu ','revenue_report_view'),(53,'Xem danh sách nhóm quyền','get_all_role_groups'),(54,'Xem danh sách nhân viên theo nhóm quyền','get_staffs_by_role_group'),(55,'Thêm nhân viên vào nhóm quyền','add_staffs_by_role_group'),(56,'Lấy danh sách chức năng thuộc nhóm quyền','get_role_group_functions'),(57,'Loại bỏ chức năng khỏi nhóm quyền','remove_function_from_role_group'),(58,'Thêm chức năng vào nhóm quyền','add_functions_to_role_group'),(59,'Loại nhân viên khỏi nhóm quyền','remove_staff_from_role_group'),(60,'Lấy danh sách nhân viên không thuộc nhóm quyền','get_staffs_not_in_role_group'),(61,'Tạo nhóm quyền','create_role_group'),(62,'Cập nhật nhóm quyền','update_role_group'),(63,'Xóa nhóm quyền','delete_role_group'),(64,'Lấy danh sách dịch vụ','service_list'),(65,'Thêm dịch vụ','service_create'),(66,'Sửa dịch vụ','service_edit'),(67,'Xóa dịch vụ','service_delete'),(68,'Xem danh sách nhân viên','get_all_staffs'),(69,'Thêm nhân viên','create_staff'),(70,'Sửa nhân viên','update_staff'),(71,'Khóa nhân viên','lock_staff'),(72,'Xem chi tiết nhân viên','get_staff_by_id'),(73,'Xem danh sách khuyến mãi','voucher_list'),(74,'Tạo khuyến mãi','voucher_create'),(75,'Sửa khuyến mãi','voucher_edit'),(76,'Kết thúc khuyến mãi','voucher_delete'),(77,'Xem chi tiết khuyến mãi','get_voucher_by_id'),(78,'Xem báo cáo doanh thu theo yêu cầu','revenue_data_api'),(79,'Đặt lại mật khẩu cho nhân viên','edit_account_of_staff'),(80,'Xem thông tin cá nhân nhân viên','staff_detail'),(81,'Hủy gói cước','delete_subscription');
/*!40000 ALTER TABLE `functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `networks`
--

DROP TABLE IF EXISTS `networks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `networks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `network_name` varchar(100) NOT NULL,
  `display_name` varchar(100) DEFAULT NULL,
  `country_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `network_name` (`network_name`),
  KEY `country_id` (`country_id`),
  CONSTRAINT `networks_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `networks`
--

LOCK TABLES `networks` WRITE;
/*!40000 ALTER TABLE `networks` DISABLE KEYS */;
INSERT INTO `networks` VALUES (1,'Viettel','Viettel Mobile',1),(2,'Verizon','Verizon Wireless',2),(3,'ATT','AT&T Mobility',2),(4,'SoftBank','SoftBank Mobile',3),(5,'NTTDocomo','NTT Docomo',3),(6,'SKTelecom','SK Telecom (SKT)',4);
/*!40000 ALTER TABLE `networks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_detail`
--

DROP TABLE IF EXISTS `payment_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `payment_id` int NOT NULL,
  `free_data` float NOT NULL,
  `free_ON_a_call` float DEFAULT NULL,
  `free_OffN_a_call` float DEFAULT NULL,
  `free_ON_call` float DEFAULT NULL,
  `free_OffN_call` float DEFAULT NULL,
  `free_ON_SMS` float DEFAULT NULL,
  `free_OffN_SMS` int DEFAULT NULL,
  `ON_a_call_cost` float DEFAULT NULL,
  `ON_SMS_cost` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_id_idx` (`payment_id`),
  CONSTRAINT `payment_id` FOREIGN KEY (`payment_id`) REFERENCES `payments` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_detail`
--

LOCK TABLES `payment_detail` WRITE;
/*!40000 ALTER TABLE `payment_detail` DISABLE KEYS */;
INSERT INTO `payment_detail` VALUES (113,113,30720,0,0,600,1800,0,0,NULL,NULL),(114,114,7168,0,0,0,0,0,0,NULL,NULL),(115,115,7168,0,0,0,0,0,0,NULL,NULL),(116,116,1024,10,5,3000,10,20,5,NULL,NULL),(117,117,1024,10,5,3000,10,20,5,NULL,NULL),(118,118,7168,0,0,0,0,0,0,NULL,NULL),(119,119,1024,10,5,3000,10,20,5,NULL,NULL),(120,120,5120,0,0,0,0,0,0,NULL,NULL),(121,121,1,0,0,0,0,0,0,NULL,NULL),(122,122,7168,0,0,0,0,0,0,NULL,NULL),(123,123,7168,0,0,0,0,0,0,NULL,NULL),(124,124,15,0,0,0,0,0,0,NULL,NULL),(125,125,7168,0,0,0,0,0,0,NULL,NULL),(126,126,15,0,0,0,0,0,0,NULL,NULL),(127,127,20480,0,0,0,1800,0,0,NULL,NULL),(128,128,7168,0,0,0,0,0,0,NULL,NULL),(129,129,20480,0,0,0,1800,0,0,NULL,NULL),(130,130,30,0,0,0,50,0,0,NULL,NULL),(131,131,1,0,0,0,0,0,0,NULL,NULL),(132,132,7168,0,0,0,0,0,0,NULL,NULL),(133,133,15,0,0,0,0,0,0,NULL,NULL),(134,134,30695.5,0,0,600,1789,0,0,NULL,NULL),(135,135,15,0,0,0,0,0,0,NULL,NULL),(136,136,1,0,0,0,0,0,0,NULL,NULL),(137,137,7168,0,0,0,0,0,0,NULL,NULL),(138,138,5120,0,0,0,0,0,0,NULL,NULL),(139,139,7168,0,0,0,0,0,0,NULL,NULL),(140,140,7168,0,0,0,0,0,0,NULL,NULL),(141,141,7168,0,0,0,0,0,0,NULL,NULL),(142,142,5120,0,0,0,0,0,0,NULL,NULL),(143,143,7168,0,0,0,0,0,0,NULL,NULL),(144,144,15,0,0,0,0,0,0,NULL,NULL),(145,145,7168,0,0,0,0,0,0,NULL,NULL),(146,146,7168,0,0,0,0,0,0,NULL,NULL),(147,147,0,0,0,0,0,0,0,NULL,NULL);
/*!40000 ALTER TABLE `payment_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subscription_id` int NOT NULL,
  `payment_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `total_amount` float NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `is_paid` tinyint(1) DEFAULT '0',
  `due_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `subscription_id_idx` (`subscription_id`),
  CONSTRAINT `subscription_id` FOREIGN KEY (`subscription_id`) REFERENCES `subscriptions` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (113,109,'2025-06-16 04:46:20',90000,'account',1,'2025-06-16 04:46:21'),(114,110,'2025-06-16 04:48:40',30000,'account',1,'2025-06-16 04:48:40'),(115,111,'2025-06-16 05:17:06',30000,'account',1,'2025-06-16 05:17:06'),(116,112,'2025-06-16 05:18:04',100,'account',1,'2025-06-16 05:18:05'),(117,113,'2025-06-16 05:20:21',100,'account',1,'2025-06-16 05:20:22'),(118,114,'2025-06-16 09:24:04',30000,'QRcode',0,'2025-07-01 00:00:00'),(119,115,'2025-06-16 09:33:03',100,'QRcode',0,'2025-07-01 00:00:00'),(120,116,'2025-06-16 09:36:30',30000,'account',1,'2025-06-16 09:36:30'),(121,117,'2025-06-16 09:37:08',5000,'account',1,'2025-06-16 09:37:09'),(122,118,'2025-06-16 09:37:13',30000,'account',1,'2025-06-16 09:37:14'),(123,119,'2025-06-16 09:37:19',30000,'account',1,'2025-06-16 09:37:19'),(124,120,'2025-06-16 09:37:32',70000,'account',1,'2025-06-16 09:37:32'),(125,121,'2025-06-16 09:39:27',30000,'account',1,'2025-06-16 09:39:28'),(126,122,'2025-06-16 09:39:31',70000,'account',1,'2025-06-16 09:39:32'),(127,123,'2025-06-16 09:39:36',120000,'account',1,'2025-06-16 09:39:36'),(128,124,'2025-06-16 09:40:22',30000,'account',1,'2025-06-16 09:40:23'),(129,125,'2025-06-16 09:43:53',120000,'account',1,'2025-06-16 09:43:53'),(130,126,'2025-06-16 09:43:58',150000,'account',1,'2025-06-16 09:43:58'),(131,127,'2025-06-16 09:44:33',5000,'account',1,'2025-06-16 09:44:33'),(132,128,'2025-06-16 09:44:37',30000,'account',1,'2025-06-16 09:44:38'),(133,129,'2025-06-16 09:44:47',70000,'account',1,'2025-06-16 09:44:48'),(134,130,'2025-06-16 14:06:15',90000,'account',1,NULL),(135,131,'2025-06-16 09:45:20',70000,'account',1,'2025-06-16 09:45:20'),(136,132,'2025-06-16 09:45:36',5000,'account',1,'2025-06-16 09:45:37'),(137,133,'2025-06-16 09:48:21',30000,'account',1,'2025-06-16 09:48:21'),(138,134,'2025-06-16 10:27:07',30000,'account',1,'2025-06-16 10:27:07'),(139,135,'2025-06-16 10:27:14',30000,'account',1,'2025-06-16 10:27:14'),(140,136,'2025-06-16 10:56:43',30000,'account',1,'2025-06-16 10:56:43'),(141,137,'2025-06-16 11:03:54',30000,'account',1,'2025-06-16 11:03:54'),(142,138,'2025-06-16 11:15:46',30000,'account',1,'2025-06-16 11:15:46'),(143,139,'2025-06-16 11:15:55',30000,'account',1,'2025-06-16 11:15:56'),(144,140,'2025-06-16 11:18:35',70000,'account',1,'2025-06-16 11:18:35'),(145,141,'2025-06-16 11:18:46',30000,'account',1,'2025-06-16 11:18:47'),(146,142,'2025-06-16 11:19:15',30000,'account',1,'2025-06-16 11:19:15'),(147,143,'2025-06-16 14:06:15',5000,'QRCode',1,NULL);
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissiondetail`
--

DROP TABLE IF EXISTS `permissiondetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissiondetail` (
  `role_group_id` int NOT NULL,
  `account_id` int NOT NULL,
  PRIMARY KEY (`role_group_id`,`account_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `permissiondetail_ibfk_1` FOREIGN KEY (`role_group_id`) REFERENCES `rolegroup` (`id`) ON DELETE CASCADE,
  CONSTRAINT `permissiondetail_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissiondetail`
--

LOCK TABLES `permissiondetail` WRITE;
/*!40000 ALTER TABLE `permissiondetail` DISABLE KEYS */;
INSERT INTO `permissiondetail` VALUES (1,10),(1,11),(2,11),(1,12),(2,12),(2,13),(2,14),(2,15),(2,16),(2,17),(2,18),(2,19),(3,20),(3,21),(3,22),(3,23),(3,24),(3,25),(3,26),(2,53),(1,54);
/*!40000 ALTER TABLE `permissiondetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plan_detail`
--

DROP TABLE IF EXISTS `plan_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plan_detail` (
  `plan_id` int NOT NULL,
  `object_type` varchar(50) NOT NULL,
  `duration` int NOT NULL,
  PRIMARY KEY (`plan_id`,`object_type`),
  CONSTRAINT `plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plan_detail`
--

LOCK TABLES `plan_detail` WRITE;
/*!40000 ALTER TABLE `plan_detail` DISABLE KEYS */;
INSERT INTO `plan_detail` VALUES (1,'TRASAU',30),(1,'TRATRUOC',30),(13,'TRASAU',30),(13,'TRATRUOC',30),(14,'TRASAU',3),(14,'TRATRUOC',3),(37,'TRASAU',30),(37,'TRATRUOC',30),(38,'TRASAU',30),(38,'TRATRUOC',30),(39,'TRASAU',30),(39,'TRATRUOC',30),(40,'TRASAU',30),(40,'TRATRUOC',30),(41,'TRASAU',30),(41,'TRATRUOC',30),(42,'TRASAU',30),(42,'TRATRUOC',30),(43,'TRASAU',7),(43,'TRATRUOC',7),(44,'TRASAU',15),(44,'TRATRUOC',15),(45,'TRASAU',1),(45,'TRATRUOC',1),(46,'TRASAU',30),(46,'TRATRUOC',30),(47,'TRASAU',30),(47,'TRATRUOC',30),(48,'TRASAU',30),(48,'TRATRUOC',30),(49,'TRASAU',30),(49,'TRATRUOC',30),(50,'TRASAU',30),(50,'TRATRUOC',30),(51,'TRASAU',30),(51,'TRATRUOC',30),(55,'TRASAU',3),(55,'TRATRUOC',3),(56,'TRASAU',7),(56,'TRATRUOC',7),(57,'TRASAU',15),(57,'TRATRUOC',15),(58,'TRATRUOC',44);
/*!40000 ALTER TABLE `plan_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plan_network`
--

DROP TABLE IF EXISTS `plan_network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plan_network` (
  `id` int NOT NULL AUTO_INCREMENT,
  `network_id` int NOT NULL,
  `plan_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `network_id` (`network_id`),
  KEY `plan_network_ibfk_2_idx` (`plan_id`),
  CONSTRAINT `plan_network_ibfk_1` FOREIGN KEY (`network_id`) REFERENCES `networks` (`id`) ON DELETE CASCADE,
  CONSTRAINT `plan_network_ibfk_2` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plan_network`
--

LOCK TABLES `plan_network` WRITE;
/*!40000 ALTER TABLE `plan_network` DISABLE KEYS */;
INSERT INTO `plan_network` VALUES (32,2,55),(33,4,55),(34,5,55),(35,2,56),(36,3,56),(37,4,56),(38,5,56),(39,6,56),(40,2,57),(41,3,57),(42,4,57),(43,5,57),(44,6,57);
/*!40000 ALTER TABLE `plan_network` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plans`
--

DROP TABLE IF EXISTS `plans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `description` text,
  `service_id` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `renewal_syntax` varchar(255) DEFAULT NULL,
  `registration_syntax` varchar(255) DEFAULT NULL,
  `cancel_syntax` varchar(255) DEFAULT NULL,
  `free_data` int DEFAULT '0',
  `free_on_network_a_call` int DEFAULT '0',
  `free_on_network_call` int DEFAULT '0',
  `free_on_network_SMS` int DEFAULT '0',
  `free_off_network_a_call` int DEFAULT '0',
  `free_off_network_call` int DEFAULT '0',
  `free_off_network_SMS` int DEFAULT '0',
  `auto_renew` tinyint(1) DEFAULT '0',
  `staff_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `maximum_on_network_call` int DEFAULT '0',
  `ON_SMS_cost` float DEFAULT NULL,
  `ON_a_call_cost` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `staff_id` (`staff_id`),
  KEY `service_id_idx` (`service_id`),
  CONSTRAINT `plans_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `staffs` (`id`) ON DELETE SET NULL,
  CONSTRAINT `service_id` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plans`
--

LOCK TABLES `plans` WRITE;
/*!40000 ALTER TABLE `plans` DISABLE KEYS */;
INSERT INTO `plans` VALUES (1,'SD90',90000,'30GB/30 ngày, tự động gia hạn sau 3 ngày khi hết dung lượng',1,1,'HUY SD90|191','SD90|191','HUYDATA SD90|191',30720,0,0,0,0,0,0,1,7,'2025-04-16 22:14:52','2025-06-11 10:36:49',0,NULL,NULL),(13,'PRE100',100,'Trả trước 100K, 1024MB, 3000s gọi, 20 SMS nội mạng',4,1,'HUY PRE100|191','PRE100|191','HUYDATA PRE100|191',1024,10,3000,20,5,10,5,0,7,'2025-04-12 18:11:39','2025-06-11 10:36:49',100,NULL,NULL),(14,'5G30',30000,'5GB sử dụng trong 3 ngày, có thể gia hạn',3,1,'HUY 5G30|191','5G30|191','HUYDATA 5G30|191',5120,0,0,0,0,0,0,1,7,'2025-04-16 22:14:52','2025-06-11 10:36:49',0,NULL,NULL),(37,'V90B',90000,'30GB (1GB/ngày), miễn phí gọi nội mạng <600s, 1800s ngoại mạng',2,1,'HUY V90B|191','V90B|191','HUYDATA V90B|191',30720,0,600,0,0,1800,0,0,NULL,'2025-06-07 23:03:30','2025-06-16 04:40:42',0,NULL,NULL),(38,'V120B',120000,'45GB, miễn phí nội mạng, 3000s ngoại mạng',2,1,'HUY V120B|191','V120B|290','HUYDATA V90B|191',46080,0,-1,0,0,3000,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(39,'V150B',150000,'60GB (2GB/ngày), miễn phí gọi nội mạng, 80 phút gọi ngoại mạng',2,1,'HUY V150B|191','V150B|290','HUYDATA V120B|191',60,0,0,0,0,80,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(40,'V200B',200000,'240GB (8GB/ngày), miễn phí gọi nội mạng, 100 phút gọi ngoại mạng',2,1,'HUY V200B|191','V200B|290','HUYDATA V150B|191',240,0,0,0,0,100,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(41,'MXH120',120,'30GB + miễn phí Facebook, TikTok, Youtube, 30 phút ngoại mạng',2,1,'HUY MXH120|191','MXH120|290','HUYDATA MXH120|191',30,0,0,0,0,30,0,1,NULL,'2025-06-07 23:03:30','2025-06-15 20:41:20',0,NULL,NULL),(42,'MXH150',150000,'45GB + miễn phí Facebook, TikTok, Youtube, 50 phút ngoại mạng',2,1,'HUY MXH150|191','MXH150|290','HUYDATA MXH150|191',45,0,0,0,0,50,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(43,'ST30K',30000,'7168MB sử dụng trong 7 ngày',3,1,'HUY ST30K|191','ST30K|191','HUYDATA ST30K|191',7168,0,0,0,0,0,0,0,NULL,'2025-06-07 23:03:30','2025-06-15 14:00:34',0,NULL,NULL),(44,'ST70K',70000,'15GB trong 15 ngày',3,1,'HUY ST70K|191','ST70K|191','HUYDATA ST70K|191',15,0,0,0,0,0,0,0,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(45,'MI5D',5000,'1GB sử dụng trong 1 ngày',3,1,'HUY MI5D|191','MI5D|191','HUYDATA MI5D|191',1,0,0,0,0,0,0,0,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(46,'CS120',120000,'20480MB + miễn phí MXH + 1800s ngoại mạng',4,1,'HUY CS120|191','CS120|191','HUYDATA CS120|191',20480,0,0,0,0,1800,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(47,'CS150',150000,'Miễn phí Facebook, TikTok, Youtube + 30GB tốc độ cao',4,1,'HUY CS150|191','CS150|191','HUYDATA CS150|191',30,0,0,0,0,50,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(48,'MT30K',30000,'Miễn phí gọi nội mạng dưới 10 phút + 10 phút ngoại mạng',2,1,'HUY MT30K|191','MT30K|191','HUYDATA MT30K|191',0,0,0,0,0,10,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(49,'MT50K',50000,'Miễn phí gọi nội mạng toàn thời gian + 1800s ngoại mạng',2,1,'HUY MT50K|191','MT50K|191','HUYDATA MT50K|191',0,0,-1,0,0,1800,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(50,'DN120',120000,'45GB + gọi nội mạng không giới hạn + 60 phút gọi ngoại mạng',2,1,'HUY DN120|191','DN120|191','HUYDATA DN120|191',45,0,0,0,0,60,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(51,'DN200',200000,'92160MB + nội mạng không giới hạn + 6000s ngoại mạng',2,1,'HUY DN200|191','DN200|191','HUYDATA DN200|191',92160,0,-1,0,0,6000,0,1,NULL,'2025-06-07 23:03:30','2025-06-11 10:36:49',0,NULL,NULL),(55,'DR90',90000,'Gói roaming quốc tế 3 ngày, 1GB/ngày tại các quốc gia Đông Nam Á',2,1,'HUY DR90|191','DR90|191','HUYDATA DR90|191',3,0,0,0,0,0,0,0,7,'2025-06-08 21:25:42','2025-06-11 10:36:49',0,NULL,NULL),(56,'DR200',200000,'Gói roaming quốc tế 7 ngày, tổng 3GB tại Châu Á và Mỹ',2,1,'HUY DR200|191','DR200|191','HUYDATA DR200|191',3,0,0,0,0,0,0,0,7,'2025-06-08 21:25:42','2025-06-11 10:36:49',0,NULL,NULL),(57,'DR500',500000,'Gói roaming toàn cầu 15 ngày, tổng 5GB + miễn phí Facebook/Youtube',2,1,'HUY DR500|191','DR500|191','HUYDATA DR500|191',5,0,0,0,0,0,0,0,7,'2025-06-08 21:25:42','2025-06-11 10:36:49',0,NULL,NULL),(58,'KT',43,'df',4,0,'ab','DK KT','ab',1,2,1,1,1,0,0,0,7,'2025-06-16 11:23:50','2025-06-16 11:59:06',0,0.01,0.01);
/*!40000 ALTER TABLE `plans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rolegroup`
--

DROP TABLE IF EXISTS `rolegroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rolegroup` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rolegroup`
--

LOCK TABLES `rolegroup` WRITE;
/*!40000 ALTER TABLE `rolegroup` DISABLE KEYS */;
INSERT INTO `rolegroup` VALUES (1,'Quản lý'),(2,'Nhân viên'),(3,'Thuê bao');
/*!40000 ALTER TABLE `rolegroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rolegroupdetail`
--

DROP TABLE IF EXISTS `rolegroupdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rolegroupdetail` (
  `role_group_id` int NOT NULL,
  `function_id` int NOT NULL,
  PRIMARY KEY (`role_group_id`,`function_id`),
  KEY `function_id` (`function_id`),
  CONSTRAINT `rolegroupdetail_ibfk_1` FOREIGN KEY (`role_group_id`) REFERENCES `rolegroup` (`id`) ON DELETE CASCADE,
  CONSTRAINT `rolegroupdetail_ibfk_2` FOREIGN KEY (`function_id`) REFERENCES `functions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rolegroupdetail`
--

LOCK TABLES `rolegroupdetail` WRITE;
/*!40000 ALTER TABLE `rolegroupdetail` DISABLE KEYS */;
INSERT INTO `rolegroupdetail` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(3,8),(1,9),(1,11),(2,11),(3,12),(3,13),(3,14),(3,15),(3,16),(3,17),(3,18),(3,19),(3,20),(1,21),(1,22),(1,23),(1,24),(1,25),(1,26),(2,26),(2,27),(3,27),(1,28),(2,28),(1,29),(2,29),(1,30),(2,30),(1,31),(2,31),(1,32),(2,32),(1,33),(2,33),(1,34),(2,34),(1,35),(2,35),(1,36),(2,36),(1,37),(2,37),(1,38),(2,38),(1,39),(2,39),(1,40),(2,40),(1,41),(2,41),(1,42),(2,42),(1,43),(2,43),(1,44),(2,44),(1,45),(2,45),(1,46),(2,46),(1,47),(2,47),(1,48),(2,48),(1,49),(2,49),(1,50),(2,50),(1,51),(2,51),(1,52),(1,53),(1,54),(1,55),(1,56),(1,57),(1,58),(1,59),(1,60),(1,61),(1,62),(1,63),(1,64),(2,64),(1,65),(2,65),(1,66),(2,66),(1,67),(2,67),(1,68),(1,69),(1,70),(1,71),(1,72),(1,73),(1,74),(1,75),(1,76),(1,77),(1,78),(1,79),(1,80),(2,80),(3,81);
/*!40000 ALTER TABLE `rolegroupdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `id` int NOT NULL AUTO_INCREMENT,
  `service_name` varchar(100) NOT NULL,
  `parent_id` int DEFAULT NULL,
  `coverage_area` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'Gói dịch vụ di động',NULL,_binary '\0'),(2,'Gói dịch vụ cước chính',NULL,_binary '\0'),(3,'Gói cước 4G/5G',1,_binary '\0'),(4,'Gói cước hot',1,_binary '\0'),(5,'Gói cước DCOM',1,_binary ''),(6,'Gói cước Roaming',1,_binary '\0');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staffs`
--

DROP TABLE IF EXISTS `staffs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `card_id` varchar(50) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `gender` enum('Nam','Nữ','Khác') NOT NULL,
  `birthday` date DEFAULT NULL,
  `account_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_id` (`card_id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `staffs_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffs`
--

LOCK TABLES `staffs` WRITE;
/*!40000 ALTER TABLE `staffs` DISABLE KEYS */;
INSERT INTO `staffs` VALUES (7,'Nguyễn Văn A','001234567890','0987654321','nguyenvana@example.com',1,'Nam','1990-05-20',10),(8,'Trần Thị B','001234567891','0912345678','tranthib@example.com',1,'Nữ','1985-10-15',11),(9,'Lê Văn C','001234567892','0977123456','levanc@example.com',1,'Nam','1992-03-10',12),(10,'Phạm Thị D','001234567893','0909123456','phamthid@example.com',1,'Nữ','1995-07-25',13),(11,'Hoàng Minh E','001234567894','0934123456','hoangminhe@example.com',0,'Nam','1988-12-30',14),(12,'Vũ Ngọc F','001234567895','0968123456','vungocf@example.com',1,'Khác','2000-01-01',15),(13,'Trà Nhật Đông','123456789101','1234567898','tranhatdong1808@gmail.com',1,'Nam','2004-06-15',53),(14,'Trà Nhật Đông','123456788787','1234566545','tranhatdong18087755556@gmail.com',1,'Nam','2004-06-15',54);
/*!40000 ALTER TABLE `staffs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscribers`
--

DROP TABLE IF EXISTS `subscribers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscribers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(15) NOT NULL,
  `main_balance` decimal(10,2) DEFAULT '0.00',
  `activation_date` date NOT NULL,
  `expiration_date` date NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `customer_id` int DEFAULT NULL,
  `warning_date` datetime DEFAULT NULL,
  `subscriber` varchar(45) DEFAULT 'TRATRUOC',
  `account_id` int DEFAULT NULL,
  `ON_a_call_cost` float NOT NULL,
  `ON_SMS_cost` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone_number` (`phone_number`),
  KEY `subscribers_ibfk_1` (`customer_id`),
  KEY `subscribers_account_id_idx` (`account_id`),
  CONSTRAINT `subscribers_account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `subscribers_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscribers`
--

LOCK TABLES `subscribers` WRITE;
/*!40000 ALTER TABLE `subscribers` DISABLE KEYS */;
INSERT INTO `subscribers` VALUES (6,'0912345678',1307880.00,'2024-01-01','2025-01-01',1,1,NULL,'TRATRUOC',20,1500,100),(7,'0933221144',25000.00,'2024-02-15','2025-02-15',1,2,NULL,'TRATRUOC',21,1500,100),(8,'0909888777',20000.00,'2024-03-10','2024-12-10',1,3,NULL,'TRATRUOC',22,1500,100),(9,'0988997766',0.00,'2024-01-20','2024-08-20',0,4,NULL,'TRATRUOC',23,1500,100),(10,'0977886655',30000.00,'2024-04-01','2025-04-01',1,2,NULL,'TRATRUOC',24,1500,100),(11,'0123456789',10700.00,'2024-05-01','2025-08-30',1,1,NULL,'TRASAU',25,1500,100),(12,'0123456788',0.00,'2024-05-01','2025-04-04',1,1,NULL,'TRATRUOC',26,1500,100),(14,'0329518648',1.00,'2025-06-15','2025-01-01',1,5,NULL,'TRASAU',28,1,1),(15,'0375648394555',1000.00,'2025-06-15','2025-06-20',1,5,NULL,'TRASAU',29,1500,100),(16,'09332211444444',25000.00,'2025-06-15','2025-02-15',1,2,NULL,'TRASAU',31,1500,100),(17,'0933221144444',25000.00,'2025-06-15','2025-02-15',0,2,NULL,'TRASAU',32,1500,100),(18,'09332211444442',25000.00,'2025-06-15','2025-02-15',1,2,NULL,'TRASAU',33,1500,100),(19,'09332',25000.00,'2025-06-15','2025-02-15',1,2,NULL,'TRASAU',34,1500,100),(20,'0184638394',25000.00,'2025-06-15','2025-02-15',1,2,NULL,'TRASAU',36,1500,100),(21,'0483766486',25000.00,'2025-06-15','2025-12-20',1,6,NULL,'TRASAU',37,1500,100),(22,'04837664863',25000.00,'2025-06-15','2025-02-15',1,6,NULL,'TRASAU',38,1500,100),(23,'048376648',25000.00,'2025-06-15','2025-02-15',1,6,NULL,'TRASAU',41,1500,100),(24,'04837664',25000.00,'2025-06-15','2025-02-15',1,6,NULL,'TRASAU',44,1500,100),(25,'0385647483',25000.00,'2025-06-15','2025-08-15',1,6,NULL,'TRASAU',46,1500,100),(26,'0578736485',1.00,'2025-06-15','2025-07-04',1,5,NULL,'TRASAU',47,1500,100),(27,'0578736488',1.00,'2025-06-15','2025-07-04',1,5,NULL,'TRASAU',48,1500,100),(28,'0483648576',1.00,'2025-06-15','2025-07-02',1,1,NULL,'TRASAU',49,1500,100),(29,'0329618363',10000.00,'2025-06-16','2025-06-27',1,3,NULL,'TRASAU',50,1500,100),(30,'09123456776',10000.00,'2025-06-16','2025-06-19',1,3,NULL,'TRASAU',52,1500,100);
/*!40000 ALTER TABLE `subscribers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscriptions`
--

DROP TABLE IF EXISTS `subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plan_id` int NOT NULL,
  `subscriber_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `expiration_date` datetime DEFAULT NULL,
  `renewal_total` int DEFAULT '0',
  `is_renewal` tinyint(1) NOT NULL DEFAULT '1',
  `cancel_at` datetime DEFAULT NULL,
  `activation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `subscriptions_ibfk_2_idx` (`subscriber_id`),
  KEY `subscriptions_ibfk_1_idx` (`plan_id`),
  CONSTRAINT `subscriptions_ibfk_1` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `subscriptions_ibfk_2` FOREIGN KEY (`subscriber_id`) REFERENCES `subscribers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscriptions`
--

LOCK TABLES `subscriptions` WRITE;
/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;
INSERT INTO `subscriptions` VALUES (109,37,6,'2025-06-16 04:46:19','2025-07-16 00:00:00',0,1,'2025-06-16 09:44:26','2025-06-16 04:46:19'),(110,43,6,'2025-06-16 04:48:40','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 04:48:40'),(111,43,6,'2025-06-16 05:17:06','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 05:17:06'),(112,13,6,'2025-06-16 05:18:04','2025-07-16 00:00:00',0,0,NULL,'2025-06-16 05:18:04'),(113,13,6,'2025-06-16 05:20:21','2025-07-16 00:00:00',0,0,NULL,'2025-06-16 05:20:21'),(114,43,6,'2025-06-16 09:24:05','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 09:24:05'),(115,13,6,'2025-06-16 09:33:03','2025-07-16 00:00:00',0,0,NULL,'2025-06-16 09:33:03'),(116,14,6,'2025-06-16 09:36:30','2025-06-19 00:00:00',0,1,'2025-06-16 09:36:52','2025-06-16 09:36:30'),(117,45,6,'2025-06-16 09:37:08','2025-06-17 00:00:00',0,0,NULL,'2025-06-16 09:37:08'),(118,43,6,'2025-06-16 09:37:14','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 09:37:14'),(119,43,6,'2025-06-16 09:37:19','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 09:37:19'),(120,44,6,'2025-06-16 09:37:32','2025-07-01 00:00:00',0,0,NULL,'2025-06-16 09:37:32'),(121,43,6,'2025-06-16 09:39:27','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 09:39:27'),(122,44,6,'2025-06-16 09:39:32','2025-07-01 00:00:00',0,0,NULL,'2025-06-16 09:39:32'),(123,46,6,'2025-06-16 09:39:36','2025-07-16 00:00:00',0,1,'2025-06-16 09:40:22','2025-06-16 09:39:36'),(124,43,6,'2025-06-16 09:40:23','2025-06-23 00:00:00',0,1,'2025-06-16 09:43:52','2025-06-16 09:40:23'),(125,46,6,'2025-06-16 09:43:53','2025-07-16 00:00:00',0,1,'2025-06-16 09:43:58','2025-06-16 09:43:53'),(126,47,6,'2025-06-16 09:43:58','2025-07-16 00:00:00',0,1,'2025-06-16 09:44:23','2025-06-16 09:43:58'),(127,45,6,'2025-06-16 09:44:33','2025-06-17 00:00:00',0,0,NULL,'2025-06-16 09:44:33'),(128,43,6,'2025-06-16 09:44:38','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 09:44:38'),(129,44,6,'2025-06-16 09:44:47','2025-07-01 00:00:00',0,0,NULL,'2025-06-16 09:44:47'),(130,37,6,'2025-06-16 09:45:02','2025-07-16 00:00:00',0,1,'2025-06-16 11:18:26','2025-06-16 09:45:02'),(131,44,6,'2025-06-16 09:45:20','2025-07-01 00:00:00',0,0,NULL,'2025-06-16 09:45:20'),(132,45,6,'2025-06-16 09:45:36','2025-06-17 00:00:00',0,0,NULL,'2025-06-16 09:45:36'),(133,43,6,'2025-06-16 09:48:21','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 09:48:21'),(134,14,6,'2025-06-16 10:27:07','2025-06-19 00:00:00',0,1,'2025-06-16 10:27:14','2025-06-16 10:27:07'),(135,43,6,'2025-06-16 10:27:14','2025-06-23 00:00:00',0,0,'2025-06-16 10:56:35','2025-06-16 10:27:14'),(136,43,6,'2025-06-16 10:56:43','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 10:56:43'),(137,43,6,'2025-06-16 11:03:54','2025-06-23 00:00:00',0,0,NULL,'2025-06-16 11:03:54'),(138,14,6,'2025-06-16 11:15:46','2025-06-19 00:00:00',0,1,'2025-06-16 11:15:55','2025-06-16 11:15:46'),(139,43,6,'2025-06-16 11:15:56','2025-06-23 00:00:00',0,1,'2025-06-16 11:16:11','2025-06-16 11:15:56'),(140,44,6,'2025-06-16 11:18:35','2025-07-01 00:00:00',0,1,'2025-06-16 11:18:46','2025-06-16 11:18:35'),(141,43,6,'2025-06-16 11:18:46','2025-06-23 00:00:00',0,1,'2025-06-16 11:19:15','2025-06-16 11:18:47'),(142,43,6,'2025-06-16 11:19:15','2025-06-23 00:00:00',0,1,NULL,'2025-06-16 11:19:15'),(143,45,6,'2025-06-16 11:19:35','2025-06-17 00:00:00',5000,0,NULL,'2025-06-16 11:19:35');
/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_table`
--

DROP TABLE IF EXISTS `test_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `value` int DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_table`
--

LOCK TABLES `test_table` WRITE;
/*!40000 ALTER TABLE `test_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `test_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usage_logs`
--

DROP TABLE IF EXISTS `usage_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usage_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  `usage_value` decimal(10,0) NOT NULL,
  `subscriber_id` int NOT NULL,
  `start_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_date` datetime DEFAULT NULL,
  `by_from` varchar(10) DEFAULT NULL,
  `to` varchar(10) DEFAULT NULL,
  `contents` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usage_logs_ibfk_1_idx` (`subscriber_id`),
  CONSTRAINT `usage_logs_ibfk_1` FOREIGN KEY (`subscriber_id`) REFERENCES `subscribers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=574 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usage_logs`
--

LOCK TABLES `usage_logs` WRITE;
/*!40000 ALTER TABLE `usage_logs` DISABLE KEYS */;
INSERT INTO `usage_logs` VALUES (529,'DULIEU',5,6,'2025-06-05 08:03:00','2025-06-12 16:11:07','0912345606','0987654321','Lướt web Facebook'),(530,'CUOCGOI',60,6,'2025-06-05 08:06:00','2025-06-05 09:06:00','0912345606','0987654322','Gọi nội mạng'),(531,'TINNHAN',1,6,'2025-06-05 08:09:00','2025-06-12 16:11:07','0912345606','0987654323','Chúc mừng ngày mới'),(532,'DULIEU',300,7,'2025-06-05 08:12:00','2025-06-12 16:11:07','0912345607','0987654324','Xem video TikTok'),(533,'CUOCGOI',120,7,'2025-06-05 08:15:00','2025-06-05 10:15:00','0912345607','0987654325','Gọi ngoại mạng'),(534,'TINNHAN',1,7,'2025-06-05 08:18:00','2025-06-12 16:11:07','0912345607','0987654326','Gửi lời chúc'),(535,'DULIEU',1,8,'2025-06-05 08:21:00','2025-06-12 16:11:07','0912345608','0987654327','Xem YouTube'),(536,'CUOCGOI',2,8,'2025-06-05 08:24:00','2025-06-05 11:24:00','0912345608','0987654328','Gọi quốc tế'),(537,'TINNHAN',1,8,'2025-06-05 08:27:00','2025-06-12 16:11:07','0912345608','0987654329','SMS roaming'),(538,'TINNHAN',1,7,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0933221144','Gói DR90 đã hết hạn. Hủy tự động.'),(539,'TINNHAN',1,7,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0933221144','DR90 gia hạn thất bại (không đủ tiền)'),(540,'TINNHAN',1,9,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0988997766','Gói DR90 đã hết hạn. Hủy tự động.'),(541,'TINNHAN',1,10,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0977886655','DR90 gia hạn thành công'),(542,'TINNHAN',1,7,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0933221144','Gói DR90 đã hết hạn. Hủy tự động.'),(543,'TINNHAN',1,9,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0988997766','Gói DR90 đã hết hạn. Hủy tự động.'),(544,'TINNHAN',1,11,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0123456789','DR90 gia hạn thành công'),(545,'TINNHAN',1,11,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0123456789','DR90 gia hạn thành công'),(546,'TINNHAN',1,12,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0123456788','DR90 gia hạn thành công'),(547,'TINNHAN',1,12,'2025-06-12 17:00:00','2025-06-12 17:00:00','191','0123456788','DR90 gia hạn thành công'),(548,'TINNHAN',1,10,'2025-06-12 18:00:00','2025-06-12 18:00:00','191','0977886655','Gói DR90 đã hết hạn. Hủy tự động.'),(549,'TINNHAN',1,12,'2025-06-12 18:00:00','2025-06-12 18:00:00','191','0123456788','DR90 chưa thanh toán nợ (90000.00). Không thể gia hạn.'),(550,'TINNHAN',1,12,'2025-06-12 18:00:00','2025-06-12 18:00:00','191','0123456788','DR90 chưa thanh toán nợ (90000.00). Không thể gia hạn.'),(551,'TINNHAN',1,11,'2025-06-12 18:00:00','2025-06-12 18:00:00','191','0123456789','Gói DR90 đã hết hạn. Hủy tự động.'),(552,'TINNHAN',1,12,'2025-06-12 18:00:00','2025-06-12 18:00:00','191','0123456788','Gói DR90 đã hết hạn. Hủy tự động.'),(553,'TINNHAN',1,11,'2025-06-12 18:00:00','2025-06-12 18:00:00','191','0123456789','Gói DR90 đã hết hạn. Hủy tự động.'),(554,'TINNHAN',1,12,'2025-06-12 18:00:00','2025-06-12 18:00:00','191','0123456788','Gói DR90 đã hết hạn. Hủy tự động.'),(555,'TINNHAN',1,10,'2025-06-12 21:00:00','2025-06-12 21:00:00','191','0977886655','DR90 gia hạn thất bại (không đủ tiền)'),(556,'TINNHAN',1,10,'2025-06-14 16:46:51','2025-06-14 16:46:51','191','0977886655','Gói DR90 đã hết hạn. Hủy tự động.'),(557,'TINNHAN',1,10,'2025-06-14 16:46:51','2025-06-14 16:46:51','191','0977886655','DR90 gia hạn thất bại (không đủ tiền)'),(558,'TINNHAN',1,6,'2025-06-16 06:02:00','2025-06-16 06:02:00','0912345678','234','5gfdgg'),(559,'TINNHAN',1,6,'2025-06-16 06:04:00','2025-06-16 06:04:00','0912345678','234','gfdgsdgfsr444'),(560,'TINNHAN',1,6,'2025-06-16 06:07:00','2025-06-16 06:07:00','0912345678','012345678','helllofs'),(561,'TINNHAN',1,6,'2025-06-16 06:08:00','2025-06-16 06:08:00','0912345678','234','fsadfasfd'),(562,'DULIEU',1,6,'2025-06-16 06:09:00',NULL,'0912345678',NULL,NULL),(563,'DULIEU',1,6,'2025-06-16 06:10:00',NULL,'0912345678',NULL,NULL),(564,'DULIEU',1,6,'2025-06-16 06:13:00',NULL,'0912345678',NULL,NULL),(565,'DULIEU',1,6,'2025-06-16 06:17:00',NULL,'0912345678',NULL,NULL),(566,'DULIEU',3,6,'2025-06-16 06:21:00',NULL,'0912345678',NULL,NULL),(567,'DULIEU',3,6,'2025-06-16 06:22:00',NULL,'0912345678',NULL,NULL),(568,'DULIEU',3,6,'2025-06-16 06:24:00',NULL,'0912345678',NULL,NULL),(569,'CUOCGOI',6,6,'2025-06-16 07:01:00',NULL,'0912345678','1234567898',NULL),(570,'DULIEU',3,6,'2025-06-16 07:01:00',NULL,'0912345678',NULL,NULL),(571,'CUOCGOI',11,6,'2025-06-16 07:04:00',NULL,'0912345678','0977123456',NULL),(572,'DULIEU',12,6,'2025-06-16 07:04:00',NULL,'0912345678',NULL,NULL),(573,'DULIEU',8,6,'2025-06-16 07:06:00',NULL,'0912345678',NULL,NULL);
/*!40000 ALTER TABLE `usage_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `v_accounts`
--

DROP TABLE IF EXISTS `v_accounts`;
/*!50001 DROP VIEW IF EXISTS `v_accounts`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_accounts` AS SELECT 
 1 AS `id`,
 1 AS `username`,
 1 AS `password`,
 1 AS `is_active`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_contracts`
--

DROP TABLE IF EXISTS `v_contracts`;
/*!50001 DROP VIEW IF EXISTS `v_contracts`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_contracts` AS SELECT 
 1 AS `id`,
 1 AS `title`,
 1 AS `contents`,
 1 AS `start_date`,
 1 AS `end_date`,
 1 AS `is_active`,
 1 AS `subscriber_id`,
 1 AS `created_at`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_countries`
--

DROP TABLE IF EXISTS `v_countries`;
/*!50001 DROP VIEW IF EXISTS `v_countries`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_countries` AS SELECT 
 1 AS `id`,
 1 AS `country_name`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_customers`
--

DROP TABLE IF EXISTS `v_customers`;
/*!50001 DROP VIEW IF EXISTS `v_customers`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_customers` AS SELECT 
 1 AS `id`,
 1 AS `full_name`,
 1 AS `is_active`,
 1 AS `card_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_functions`
--

DROP TABLE IF EXISTS `v_functions`;
/*!50001 DROP VIEW IF EXISTS `v_functions`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_functions` AS SELECT 
 1 AS `id`,
 1 AS `function_name`,
 1 AS `syntax_name`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_networks`
--

DROP TABLE IF EXISTS `v_networks`;
/*!50001 DROP VIEW IF EXISTS `v_networks`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_networks` AS SELECT 
 1 AS `id`,
 1 AS `network_name`,
 1 AS `display_name`,
 1 AS `country_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_payment_details`
--

DROP TABLE IF EXISTS `v_payment_details`;
/*!50001 DROP VIEW IF EXISTS `v_payment_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_payment_details` AS SELECT 
 1 AS `id`,
 1 AS `payment_id`,
 1 AS `free_data`,
 1 AS `free_on_a_call`,
 1 AS `free_offn_a_call`,
 1 AS `free_on_call`,
 1 AS `free_offn_call`,
 1 AS `free_on_sms`,
 1 AS `free_offn_sms`,
 1 AS `on_a_call_cost`,
 1 AS `on_sms_cost`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_payments`
--

DROP TABLE IF EXISTS `v_payments`;
/*!50001 DROP VIEW IF EXISTS `v_payments`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_payments` AS SELECT 
 1 AS `id`,
 1 AS `subscription_id`,
 1 AS `payment_date`,
 1 AS `total_amount`,
 1 AS `payment_method`,
 1 AS `is_paid`,
 1 AS `due_date`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_permission_details`
--

DROP TABLE IF EXISTS `v_permission_details`;
/*!50001 DROP VIEW IF EXISTS `v_permission_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_permission_details` AS SELECT 
 1 AS `role_group_id`,
 1 AS `account_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_plan_details`
--

DROP TABLE IF EXISTS `v_plan_details`;
/*!50001 DROP VIEW IF EXISTS `v_plan_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_plan_details` AS SELECT 
 1 AS `plan_id`,
 1 AS `object_type`,
 1 AS `duration`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_plan_networks`
--

DROP TABLE IF EXISTS `v_plan_networks`;
/*!50001 DROP VIEW IF EXISTS `v_plan_networks`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_plan_networks` AS SELECT 
 1 AS `id`,
 1 AS `network_id`,
 1 AS `plan_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_plans`
--

DROP TABLE IF EXISTS `v_plans`;
/*!50001 DROP VIEW IF EXISTS `v_plans`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_plans` AS SELECT 
 1 AS `id`,
 1 AS `code`,
 1 AS `price`,
 1 AS `description`,
 1 AS `service_id`,
 1 AS `is_active`,
 1 AS `renewal_syntax`,
 1 AS `registration_syntax`,
 1 AS `cancel_syntax`,
 1 AS `free_data`,
 1 AS `free_on_network_a_call`,
 1 AS `free_on_network_call`,
 1 AS `free_on_network_SMS`,
 1 AS `free_off_network_a_call`,
 1 AS `free_off_network_call`,
 1 AS `free_off_network_SMS`,
 1 AS `auto_renew`,
 1 AS `staff_id`,
 1 AS `created_at`,
 1 AS `updated_at`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_role_group_details`
--

DROP TABLE IF EXISTS `v_role_group_details`;
/*!50001 DROP VIEW IF EXISTS `v_role_group_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_role_group_details` AS SELECT 
 1 AS `role_group_id`,
 1 AS `function_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_role_groups`
--

DROP TABLE IF EXISTS `v_role_groups`;
/*!50001 DROP VIEW IF EXISTS `v_role_groups`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_role_groups` AS SELECT 
 1 AS `id`,
 1 AS `role_name`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_services`
--

DROP TABLE IF EXISTS `v_services`;
/*!50001 DROP VIEW IF EXISTS `v_services`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_services` AS SELECT 
 1 AS `id`,
 1 AS `service_name`,
 1 AS `parent_id`,
 1 AS `coverage_area`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_staffs`
--

DROP TABLE IF EXISTS `v_staffs`;
/*!50001 DROP VIEW IF EXISTS `v_staffs`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_staffs` AS SELECT 
 1 AS `id`,
 1 AS `full_name`,
 1 AS `card_id`,
 1 AS `phone`,
 1 AS `email`,
 1 AS `is_active`,
 1 AS `gender`,
 1 AS `birthday`,
 1 AS `account_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_subscribers`
--

DROP TABLE IF EXISTS `v_subscribers`;
/*!50001 DROP VIEW IF EXISTS `v_subscribers`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_subscribers` AS SELECT 
 1 AS `id`,
 1 AS `phone_number`,
 1 AS `main_balance`,
 1 AS `activation_date`,
 1 AS `expiration_date`,
 1 AS `is_active`,
 1 AS `customer_id`,
 1 AS `warning_date`,
 1 AS `account_id`,
 1 AS `subscriber`,
 1 AS `ON_a_call_cost`,
 1 AS `ON_SMS_cost`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_subscriptions`
--

DROP TABLE IF EXISTS `v_subscriptions`;
/*!50001 DROP VIEW IF EXISTS `v_subscriptions`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_subscriptions` AS SELECT 
 1 AS `id`,
 1 AS `plan_id`,
 1 AS `subscriber_id`,
 1 AS `created_at`,
 1 AS `expiration_date`,
 1 AS `renewal_total`,
 1 AS `is_renewal`,
 1 AS `cancel_at`,
 1 AS `activation_date`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_usage_logs`
--

DROP TABLE IF EXISTS `v_usage_logs`;
/*!50001 DROP VIEW IF EXISTS `v_usage_logs`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_usage_logs` AS SELECT 
 1 AS `id`,
 1 AS `type`,
 1 AS `usage_value`,
 1 AS `subscriber_id`,
 1 AS `start_date`,
 1 AS `end_date`,
 1 AS `by_from`,
 1 AS `to`,
 1 AS `contents`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_vouchers`
--

DROP TABLE IF EXISTS `v_vouchers`;
/*!50001 DROP VIEW IF EXISTS `v_vouchers`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_vouchers` AS SELECT 
 1 AS `id`,
 1 AS `code`,
 1 AS `description`,
 1 AS `conandpromo`,
 1 AS `start_date`,
 1 AS `end_date`,
 1 AS `usage_limit`,
 1 AS `remaining_count`,
 1 AS `is_active`,
 1 AS `staff_id`,
 1 AS `packages`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `vouchers`
--

DROP TABLE IF EXISTS `vouchers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vouchers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `description` text,
  `conandpromo` text,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `usage_limit` int NOT NULL,
  `remaining_count` int DEFAULT '0',
  `is_active` tinyint(1) DEFAULT '1',
  `staff_id` int DEFAULT NULL,
  `packages` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `vouchers_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `staffs` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vouchers`
--

LOCK TABLES `vouchers` WRITE;
/*!40000 ALTER TABLE `vouchers` DISABLE KEYS */;
INSERT INTO `vouchers` VALUES (25,'TRASAU_21_500MB','Tặng thêm 500MB dữ liệu khi đăng ký gói trả sau PRE100 vào cuối tháng (áp dụng cho thuê bao trả sau và gia hạn lần đầu).','{\"condition\":{\"plan_id\":[13],\"subscriber\":[\"TRASAU\"],\"created_at\":\"DAY(created_at) BETWEEN 1 AND DAY(LAST_DAY(created_at))\",\"renewal_total\":1},\"promotion\":{\"payments\":{\"total_amount\":{\"operator\":\"*\",\"value\":8}},\"payment_detail\":{\"free_data\":{\"operator\":\"+\",\"value\":6}}}}','2025-06-10','2025-08-01',50,50,1,7,'PRE100'),(26,'SD90ss','Ưu đãi dành cho thuê bao mới đăng ký gói SD90 trong tháng: áp dụng 2 lần trong chu kỳ.','{\"condition\":{\"created_at\":\"DAY(created_at) BETWEEN 1 AND DAY(LAST_DAY(created_at))\",\"plan_id\":[13],\"renewal_total\":0,\"subscriber\":[\"\"]},\"promotion\":{\"payment_detail\":{\"free_data\":null},\"payments\":{\"total_amount\":null}}}','2025-05-14','2025-05-29',2,2,1,7,'SD90'),(27,'SD90ss4','Khuyến mãi tháng: thuê bao mới đăng ký gói SD90 sẽ được nhận ưu đãi đặc biệt.','{\"condition\":{\"created_at\":\"DAY(created_at) BETWEEN 1 AND DAY(LAST_DAY(created_at))\",\"plan_id\":[13],\"renewal_total\":0,\"subscriber\":[\"\"]},\"promotion\":{\"payment_detail\":{\"free_data\":null},\"payments\":{\"total_amount\":null}}}','2025-05-08','2025-05-14',2,2,0,7,'SD90');
/*!40000 ALTER TABLE `vouchers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'mobileservice_n7'
--
/*!50106 SET @save_time_zone= @@TIME_ZONE */ ;
/*!50106 DROP EVENT IF EXISTS `auto_renew_subscriptions_event` */;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8mb4 */ ;;
/*!50003 SET character_set_results = utf8mb4 */ ;;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`root`@`localhost`*/ /*!50106 EVENT `auto_renew_subscriptions_event` ON SCHEDULE EVERY 1 HOUR STARTS '2025-04-21 00:00:00' ON COMPLETION PRESERVE ENABLE DO BEGIN
    CALL Run_AutoRenew_Manual();
END */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
/*!50106 DROP EVENT IF EXISTS `ev_cancel_expired_subscriptions` */;;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8mb4 */ ;;
/*!50003 SET character_set_results = utf8mb4 */ ;;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`root`@`localhost`*/ /*!50106 EVENT `ev_cancel_expired_subscriptions` ON SCHEDULE EVERY 1 HOUR STARTS '2025-04-21 00:00:00' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    CALL sp_cancel_expired_subscriptions();
END */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
/*!50106 DROP EVENT IF EXISTS `ev_warn_and_lock_account` */;;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8mb4 */ ;;
/*!50003 SET character_set_results = utf8mb4 */ ;;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`root`@`localhost`*/ /*!50106 EVENT `ev_warn_and_lock_account` ON SCHEDULE EVERY 1 MINUTE STARTS '2025-04-17 10:27:04' ON COMPLETION NOT PRESERVE ENABLE DO CALL sp_warn_and_lock_accounts() */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;
/*!50106 SET TIME_ZONE= @save_time_zone */ ;

--
-- Dumping routines for database 'mobileservice_n7'
--
/*!50003 DROP PROCEDURE IF EXISTS `AddCountry` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddCountry`(
    IN p_country_name VARCHAR(100)
)
BEGIN
    DECLARE existing_count INT DEFAULT 0;

    START TRANSACTION;

    -- Kiểm tra trùng tên quốc gia
    SELECT COUNT(*) INTO existing_count
    FROM countries
    WHERE country_name = p_country_name;

    IF existing_count > 0 THEN
        ROLLBACK;
        SELECT TRUE AS error, 'Tên quốc gia đã tồn tại' AS message;
    ELSE
        INSERT INTO countries (country_name)
        VALUES (p_country_name);

        IF ROW_COUNT() = 0 THEN
            ROLLBACK;
            SELECT TRUE AS error, 'Không thể thêm quốc gia' AS message;
        ELSE
            COMMIT;
            SELECT TRUE AS success, 'Thêm quốc gia thành công' AS message;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddCustomer` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddCustomer`(IN `p_full_name` VARCHAR(100), IN `p_card_id` VARCHAR(12))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi trong quá trình thêm customer' AS message;
    END;

    START TRANSACTION;

    INSERT INTO customers (
        full_name, is_active, card_id
    )
    VALUES (
        p_full_name, 1, p_card_id
    );

    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS success, 'Không thể thêm customer' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm customer thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddFunction` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddFunction`(
    IN p_function_name VARCHAR(255),
    IN p_syntax_name VARCHAR(255)
)
BEGIN
    START TRANSACTION;

    INSERT INTO functions (
        function_name, syntax_name
    )
    VALUES (
        p_function_name, p_syntax_name
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm function' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm function thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddFunctionsToRoleGroup` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddFunctionsToRoleGroup`(
    IN p_role_group_id INT,
    IN p_function_ids JSON
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE num_functions INT;
    DECLARE v_success BOOLEAN DEFAULT TRUE;
    DECLARE v_message VARCHAR(255);
    DECLARE v_add_success BOOLEAN;
    DECLARE v_add_message VARCHAR(255);
    
    -- Bắt đầu giao dịch
    START TRANSACTION;
    
    -- Lấy số lượng các chức năng cần thêm từ JSON
    SET num_functions = JSON_LENGTH(p_function_ids);
    
    -- Nhãn cho vòng lặp
    loop_start: 
    -- Lặp qua các chức năng và gọi lại AddRoleGroupDetail để thêm vào bảng
    WHILE i < num_functions AND v_success DO
        -- Lấy ID của chức năng tại chỉ số i từ JSON
        SET @function_id = JSON_UNQUOTE(JSON_EXTRACT(p_function_ids, CONCAT('$[', i, ']')));

        -- Gọi lại hàm AddRoleGroupDetail để thêm chức năng vào và nhận kết quả OUT
        CALL AddRoleGroupDetail(p_role_group_id, @function_id, @v_add_success, @v_add_message);

        -- Kiểm tra kết quả trả về từ AddRoleGroupDetail qua OUT parameters
        IF @v_add_success = FALSE THEN
            -- Nếu không thành công, rollback và thoát
            ROLLBACK;
            SET v_success = FALSE;
            SET v_message = @v_add_message;
            SELECT FALSE AS error, v_message AS message;
            LEAVE loop_start; -- Thoát khỏi vòng lặp
        END IF;
        
        -- Tiến hành bước tiếp theo nếu thành công
        SET i = i + 1;
    END WHILE;
    
    -- Kiểm tra thành công hay không
    IF v_success THEN
        COMMIT;
        SET v_message = 'Thêm tất cả role group detail thành công';
        SELECT TRUE AS success, v_message AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddFuncToRoleGroup` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddFuncToRoleGroup`(IN p_role_group_id INT, IN function_ids VARCHAR(255))
BEGIN
    -- Biến để lưu trữ kết quả
    DECLARE function_id INT;
    DECLARE idx INT DEFAULT 1;
    DECLARE total_functions INT;
    DECLARE rows_affected INT DEFAULT 0;

    -- Bắt đầu giao dịch
    START TRANSACTION;

    -- Lấy tổng số chức năng trong chuỗi function_ids
    SET total_functions = LENGTH(function_ids) - LENGTH(REPLACE(function_ids, ',', '')) + 1;

    -- Vòng lặp xử lý từng function_id từ chuỗi function_ids
    WHILE idx <= total_functions DO
        -- Lấy function_id từ chuỗi
        SET function_id = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(function_ids, ',', idx), ',', -1) AS UNSIGNED);

        -- Kiểm tra xem chức năng đã được gán cho nhóm quyền này chưa
        IF NOT EXISTS (
            SELECT 1
            FROM rolegroupdetail
            WHERE role_group_id = p_role_group_id AND function_id = function_id
            LIMIT 1
        ) THEN
            -- Thêm chức năng vào nhóm quyền
            INSERT INTO rolegroupdetail (role_group_id, function_id)
            VALUES (p_role_group_id, function_id);

            -- Tăng số lượng dòng đã thay đổi
            SET rows_affected = rows_affected + 1;
        END IF;

        -- Tăng chỉ số idx để lấy function_id tiếp theo
        SET idx = idx + 1;
    END WHILE;

    -- Kiểm tra nếu không có dòng nào thay đổi thì rollback và trả về lỗi
    IF rows_affected = 0 THEN
        ROLLBACK;
        SELECT 'Không có chức năng nào được thêm vào nhóm quyền này.' AS error;
    ELSE
        -- Nếu có thay đổi, commit giao dịch và trả về thành công
        COMMIT;
        SELECT TRUE AS success;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddNetwork` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddNetwork`(
    IN p_network_name VARCHAR(100),
    IN p_display_name VARCHAR(100),
    IN p_country_id INT
)
BEGIN
    DECLARE existing_count INT DEFAULT 0;

    START TRANSACTION;

    -- Kiểm tra tên mạng đã tồn tại chưa
    SELECT COUNT(*) INTO existing_count
    FROM networks
    WHERE network_name = p_network_name;

    IF existing_count > 0 THEN
        ROLLBACK;
        SELECT TRUE AS error, 'Tên mạng đã tồn tại' AS message;
    ELSE
        INSERT INTO networks (network_name, display_name, country_id)
        VALUES (p_network_name, p_display_name, p_country_id);

        IF ROW_COUNT() = 0 THEN
            ROLLBACK;
            SELECT TRUE AS error, 'Không thể thêm mạng' AS message;
        ELSE
            COMMIT;
            SELECT TRUE AS success, 'Thêm mạng thành công' AS message;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddPayment` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPayment`(
    IN p_subscription_id INT,
    IN p_total_amount DECIMAL(10,2),
    IN p_payment_method VARCHAR(50),
    IN p_is_paid BOOLEAN,
    IN p_due_date DATETIME
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            @p1 = RETURNED_SQLSTATE,
            @p2 = MYSQL_ERRNO,
            @p3 = MESSAGE_TEXT;
        ROLLBACK;
        SELECT 0 AS success, CONCAT('SQLSTATE: ', @p1, ', ERROR: ', @p2, ', MESSAGE: ', @p3) AS message;
    END;

    START TRANSACTION;

    -- Chèn bản ghi vào bảng payments
    INSERT INTO payments (
        subscription_id, payment_date, total_amount,
        payment_method, is_paid, due_date
    ) VALUES (
        p_subscription_id, NOW(), p_total_amount,
        p_payment_method, p_is_paid, p_due_date
    );

    -- Lấy id_payment của bản ghi vừa chèn
    SET @id_payment = LAST_INSERT_ID();

    COMMIT;

    -- Trả về kết quả thành công cùng với id_payment
    SELECT 1 AS success, 'Thêm payment thành công' AS message, @id_payment AS id_payment;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddPaymentDetail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPaymentDetail`(
    IN p_payment_id INT,
    IN p_free_data INT,
    IN p_free_on_a_call INT,
    IN p_free_offn_a_call INT,
    IN p_free_on_call INT,
    IN p_free_offn_call INT,
    IN p_free_on_sms INT,
    IN p_free_offn_sms INT,
    IN p_on_a_call_cost DECIMAL(10,2),
    IN p_on_sms_cost DECIMAL(10,2)
)
BEGIN
    START TRANSACTION;

    INSERT INTO payment_detail (
        payment_id, free_data, free_on_a_call, free_offn_a_call,
        free_on_call, free_offn_call, free_on_sms, free_offn_sms,
        on_a_call_cost, on_sms_cost
    )
    VALUES (
        p_payment_id, p_free_data, p_free_on_a_call, p_free_offn_a_call,
        p_free_on_call, p_free_offn_call, p_free_on_sms, p_free_offn_sms,
        p_on_a_call_cost, p_on_sms_cost
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm payment detail' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm payment detail thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddPermissionDetail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPermissionDetail`(
    IN p_role_group_id INT,
    IN p_account_id INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO permissiondetail (
        role_group_id, account_id
    )
    VALUES (
        p_role_group_id, p_account_id
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm permission detail' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm permission detail thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddPlan` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPlan`(
    IN p_code VARCHAR(50),
    IN p_price FLOAT,
    IN p_description TEXT,
    IN p_service_id INT,
    IN p_is_active BIT,
    IN p_renewal_syntax VARCHAR(255),
    IN p_registration_syntax VARCHAR(255),
    IN p_cancel_syntax VARCHAR(255),
    IN p_free_data INT,
    IN p_free_on_network_a_call INT,
    IN p_free_on_network_call INT,
    IN p_free_on_network_SMS INT,
    IN p_free_off_network_a_call INT,
    IN p_free_off_network_call INT,
    IN p_free_off_network_SMS INT,
    IN p_auto_renew BIT,
    IN p_staff_id INT,
    IN p_maximum_on_network_call INT,
    IN p_ON_SMS_cost FLOAT,
    IN p_ON_a_call_cost FLOAT,
    IN p_object_type VARCHAR(50),
    IN p_duration INT
)
BEGIN
    DECLARE v_error_msg VARCHAR(255);

    -- Tạo bảng tạm để debug
    CREATE TEMPORARY TABLE IF NOT EXISTS debug_log (
        log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        message TEXT
    );

    -- Bắt đầu giao dịch
    START TRANSACTION;

    -- Kiểm tra dữ liệu đầu vào
    IF p_code IS NULL OR TRIM(p_code) = '' THEN
        INSERT INTO debug_log (message) VALUES ('Mã gói cước rỗng');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã gói cước là bắt buộc';
    END IF;

    IF p_price IS NULL OR p_price <= 0 THEN
        INSERT INTO debug_log (message) VALUES ('Giá không hợp lệ');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Giá gói cước phải là số dương';
    END IF;

    IF p_service_id IS NULL THEN
        INSERT INTO debug_log (message) VALUES ('ID Dịch vụ rỗng');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ID Dịch vụ là bắt buộc';
    END IF;

    IF p_object_type NOT IN ('TRATRUOC', 'TRASAU') THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('Hình thức thanh toán không hợp lệ: ', p_object_type));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Hình thức thanh toán phải là TRATRUOC hoặc TRASAU';
    END IF;

    IF p_duration IS NULL OR p_duration <= 0 THEN
        INSERT INTO debug_log (message) VALUES ('Thời hạn không hợp lệ');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Thời hạn phải là số dương';
    END IF;

    -- Chuẩn hóa và kiểm tra mã code trùng lặp
    SET p_code = TRIM(p_code);
    IF EXISTS (SELECT 1 FROM plans WHERE LOWER(code) = LOWER(p_code)) THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('Mã gói cước trùng: ', p_code));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã gói cước đã tồn tại';
    END IF;

    -- Chuẩn hóa và kiểm tra registration_syntax trùng lặp
    IF p_registration_syntax IS NOT NULL THEN
        SET p_registration_syntax = TRIM(p_registration_syntax);
        IF EXISTS (SELECT 1 FROM plans WHERE LOWER(registration_syntax) = LOWER(p_registration_syntax)) THEN
            INSERT INTO debug_log (message) VALUES (CONCAT('Cú pháp đăng ký trùng: ', p_registration_syntax));
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cú pháp đăng ký đã tồn tại';
        END IF;
    END IF;

    -- Chuẩn hóa và kiểm tra renewal_syntax trùng lặp
    IF p_renewal_syntax IS NOT NULL THEN
        SET p_renewal_syntax = TRIM(p_renewal_syntax);
        IF EXISTS (SELECT 1 FROM plans WHERE LOWER(renewal_syntax) = LOWER(p_renewal_syntax)) THEN
            INSERT INTO debug_log (message) VALUES (CONCAT('Cú pháp gia hạn trùng: ', p_renewal_syntax));
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cú pháp gia hạn đã tồn tại';
        END IF;
    END IF;

    -- Chuẩn hóa và kiểm tra cancel_syntax trùng lặp
    IF p_cancel_syntax IS NOT NULL THEN
        SET p_cancel_syntax = TRIM(p_cancel_syntax);
        IF EXISTS (SELECT 1 FROM plans WHERE LOWER(cancel_syntax) = LOWER(p_cancel_syntax)) THEN
            INSERT INTO debug_log (message) VALUES (CONCAT('Cú pháp hủy trùng: ', p_cancel_syntax));
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cú pháp hủy đã tồn tại';
        END IF;
    END IF;

    -- Kiểm tra service_id tồn tại
    IF NOT EXISTS (SELECT 1 FROM services WHERE id = p_service_id) THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('ID Dịch vụ không tồn tại: ', p_service_id));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ID Dịch vụ không tồn tại';
    END IF;

    -- Kiểm tra staff_id tồn tại (nếu không null)
    IF p_staff_id IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM staffs WHERE id = p_staff_id
    ) THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('ID Nhân viên không tồn tại: ', p_staff_id));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ID Nhân viên không tồn tại';
    END IF;

    -- Chèn vào bảng plans
    INSERT INTO plans (
        code, price, description, service_id, is_active,
        renewal_syntax, registration_syntax, cancel_syntax,
        free_data, free_on_network_a_call, free_on_network_call,
        free_on_network_SMS, free_off_network_a_call, free_off_network_call,
        free_off_network_SMS, auto_renew, staff_id,
        maximum_on_network_call, ON_SMS_cost, ON_a_call_cost
    )
    VALUES (
        p_code, p_price, p_description, p_service_id, p_is_active,
        p_renewal_syntax, p_registration_syntax, p_cancel_syntax,
        p_free_data, p_free_on_network_a_call, p_free_on_network_call,
        p_free_on_network_SMS, p_free_off_network_a_call, p_free_off_network_call,
        p_free_off_network_SMS, p_auto_renew, p_staff_id,
        p_maximum_on_network_call, p_ON_SMS_cost, p_ON_a_call_cost
    );

    -- Lấy plan_id vừa chèn
    SET @plan_id = LAST_INSERT_ID();

    -- Chèn vào bảng plan_detail
    INSERT INTO plan_detail (plan_id, object_type, duration)
    VALUES (@plan_id, p_object_type, p_duration);

    COMMIT;

    -- Xóa bảng debug
    DROP TEMPORARY TABLE IF EXISTS debug_log;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddPlanNetwork` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPlanNetwork`(
    IN p_network_id INT,
    IN p_plan_id INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO plan_network (
        network_id, plan_id
    )
    VALUES (
        p_network_id, p_plan_id
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm plan network' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm plan network thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddRoleGroup` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddRoleGroup`(
    IN p_role_name VARCHAR(100)
)
BEGIN
    START TRANSACTION;

    INSERT INTO rolegroup (
        role_name
    )
    VALUES (
        p_role_name
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm role group' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm role group thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddRoleGroupDetail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddRoleGroupDetail`(
    IN p_role_group_id INT,
    IN p_function_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    START TRANSACTION;

    INSERT INTO rolegroupdetail (role_group_id, function_id)
    VALUES (p_role_group_id, p_function_id);
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Không thể thêm role group detail';
    ELSE
        COMMIT;
        SET p_success = TRUE;
        SET p_message = 'Thêm role group detail thành công';
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddService` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddService`(
    IN p_service_name VARCHAR(100),
    IN p_parent_id INT,
    IN p_coverage_area INT
)
BEGIN
    DECLARE existing_count INT DEFAULT 0;

    START TRANSACTION;

    -- Kiểm tra trùng tên dịch vụ
    SELECT COUNT(*) INTO existing_count
    FROM services
    WHERE service_name = p_service_name;

    IF existing_count > 0 THEN
        ROLLBACK;
        SELECT TRUE AS error, 'Tên dịch vụ đã tồn tại' AS message;
    ELSE
        INSERT INTO services (
            service_name, parent_id, coverage_area
        )
        VALUES (
            p_service_name, p_parent_id, p_coverage_area
        );

        IF ROW_COUNT() = 0 THEN
            ROLLBACK;
            SELECT TRUE AS error, 'Không thể thêm service' AS message;
        ELSE
            COMMIT;
            SELECT TRUE AS success, 'Thêm service thành công' AS message;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddStaff` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddStaff`(
    IN p_full_name VARCHAR(100),
    IN p_card_id VARCHAR(50),
    IN p_phone VARCHAR(15),
    IN p_email VARCHAR(100),
    IN p_birthday DATE,
    IN p_gender ENUM('Nam', 'Nữ', 'Khác'),
    IN p_role_name VARCHAR(255),
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255)
)
main_block: BEGIN
    DECLARE v_account_id INT;
    DECLARE v_role_group_id INT;

    -- 1. Kiểm tra trùng tên đăng nhập
    IF EXISTS (SELECT 1 FROM accounts WHERE username = p_username) THEN
        SELECT FALSE AS success, 'Tên đăng nhập đã tồn tại' AS message;
        LEAVE main_block;
    END IF;

    -- 2. Gán role_group_id theo vai trò
    IF p_role_name = 'Quản lý' THEN
        SET v_role_group_id = 1;
    ELSEIF p_role_name = 'Nhân viên' THEN
        SET v_role_group_id = 2;
    ELSE
        SELECT FALSE AS success, 'Vai trò không hợp lệ' AS message;
        LEAVE main_block;
    END IF;

    -- 3. Bắt đầu giao dịch
    START TRANSACTION;

    -- 4. Tạo tài khoản
    INSERT INTO accounts (username, password, is_active)
    VALUES (p_username, p_password, 1);
    SET v_account_id = LAST_INSERT_ID();

    -- 5. Gán quyền
    INSERT INTO permissiondetail (role_group_id, account_id)
    VALUES (v_role_group_id, v_account_id);

    -- 6. Tạo nhân viên
    INSERT INTO staffs (
        full_name, card_id, phone, email, is_active, gender, birthday, account_id
    )
    VALUES (
        p_full_name, p_card_id, p_phone, p_email, 1, p_gender, p_birthday, v_account_id
    );

    -- 7. Kiểm tra thành công
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS success, 'Không thể thêm nhân viên' AS message;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm nhân viên thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddSubscriber` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddSubscriber`(
    IN p_phone_number VARCHAR(15),
    IN p_main_balance DECIMAL(10,2),
    IN p_expiration_date DATE,
    IN p_customer_id INT,
    IN p_ON_a_call_cost FLOAT,
    IN p_ON_SMS_cost FLOAT,
    IN p_subscriber VARCHAR(45)
)
BEGIN
    DECLARE v_account_id INT;
    DECLARE v_subscriber_id INT;
 

    -- Bắt lỗi nếu có sự cố SQL
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        GET DIAGNOSTICS CONDITION 1 @p1 = RETURNED_SQLSTATE, @p2 = MESSAGE_TEXT;
        ROLLBACK;
        SELECT FALSE AS success, CONCAT('Lỗi: ', @p2) AS message;
    END;

    START TRANSACTION;

    -- Tạo account mới, username và password là số điện thoại
    INSERT INTO accounts (username, password, is_active)
    VALUES (p_phone_number, p_phone_number, 1);
    SET v_account_id = LAST_INSERT_ID();

    -- Thêm subscriber với account_id vừa tạo
    INSERT INTO subscribers (
        phone_number,
        main_balance,
        activation_date,
        expiration_date,
        is_active,
        customer_id,
        warning_date,
        subscriber,
        account_id,
        ON_a_call_cost,
        ON_SMS_cost
    ) VALUES (
        p_phone_number,
        p_main_balance,
        NOW(),
        p_expiration_date,
        TRUE,
        p_customer_id,
        NULL,
        p_subscriber,
        v_account_id,
        p_ON_a_call_cost,
        p_ON_SMS_cost
    );

    -- Lưu lại subscriber_id vừa tạo
    SET v_subscriber_id = LAST_INSERT_ID();

    
    COMMIT;

    -- Trả về kết quả
    SELECT TRUE AS success, 'Thêm thuê bao thành công, đã tạo tài khoản ' AS message;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddSubscription` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddSubscription`(
    IN p_plan_id INT,
    IN p_subscriber_id INT,
    IN p_created_at DATETIME,
    IN p_expiration_date DATETIME,
    IN p_renewal_total INT,
    IN p_is_renewal BOOLEAN,
    IN p_cancel_at DATETIME,
    IN p_activation_date DATETIME
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi trong quá trình thêm subscription' AS message;
    END;

    START TRANSACTION;

    INSERT INTO subscriptions (
        plan_id, subscriber_id, created_at, expiration_date, 
        renewal_total, is_renewal, cancel_at, activation_date
    )
    VALUES (
        p_plan_id, p_subscriber_id, p_created_at, p_expiration_date, 
        p_renewal_total, p_is_renewal, p_cancel_at, p_activation_date
    );

    -- Kiểm tra số dòng đã bị ảnh hưởng (nếu không có dòng nào bị ảnh hưởng)
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS success, 'Không thể thêm subscription' AS message; 
    ELSE
        -- Commit giao dịch
        COMMIT;

        -- Lấy ID của subscription vừa thêm
        SELECT LAST_INSERT_ID() AS subscription_id, TRUE AS success, 'Thêm subscription thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddUsageLog` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddUsageLog`(
    IN p_type VARCHAR(50),
    IN p_usage_value INT,
    IN p_subscriber_id INT,
    IN p_start_date DATETIME,
    IN p_end_date DATETIME,
    IN p_by_from VARCHAR(10),
    IN p_to VARCHAR(10),
    IN p_contents VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT JSON_OBJECT('error', 'Database error occurred') AS result;
    END;

    INSERT INTO usage_logs (type, usage_value, subscriber_id, start_date, end_date, by_from, `to`, contents)
    VALUES (p_type, p_usage_value, p_subscriber_id, p_start_date, p_end_date, p_by_from, p_to, p_contents);

    SELECT JSON_OBJECT('success', TRUE) AS result;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddUsageLogWithPromotions` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddUsageLogWithPromotions`(
    IN p_type VARCHAR(20),
    IN p_usage_value float,
    IN p_subscriber_id INT,
    IN p_start_date DATETIME,
    IN p_end_date DATETIME,
    IN p_by_from VARCHAR(20),
    IN p_to VARCHAR(20),
    IN p_contents TEXT,
    IN p_promotions_json JSON
)
BEGIN
    DECLARE done INT DEFAULT 0;

    -- Biến từ JSON
    DECLARE cur_payment_id INT;
    DECLARE cur_free_data FLOAT;
    DECLARE cur_free_ON_a_call FLOAT;
    DECLARE cur_free_ON_call FLOAT;
    DECLARE cur_free_OffN_a_call FLOAT;
    DECLARE cur_free_OffN_call FLOAT;
    DECLARE cur_free_ON_SMS FLOAT;
    DECLARE cur_free_OffN_SMS INT;
    DECLARE cur_ON_a_call_cost DECIMAL(10,2);
    DECLARE cur_ON_SMS_cost DECIMAL(10,2);
    DECLARE cur_code VARCHAR(50);
    DECLARE cur_expiration_date DATETIME;

    -- Cursor đọc JSON
    DECLARE promo_cursor CURSOR FOR
        SELECT *
        FROM JSON_TABLE(
            p_promotions_json,
            '$[*]' COLUMNS (
                payment_id INT PATH '$.payment_id',
                free_data FLOAT PATH '$.free_data',
                free_ON_a_call FLOAT PATH '$.free_ON_a_call',
                free_ON_call FLOAT PATH '$.free_ON_call',
                free_OffN_a_call FLOAT PATH '$.free_OffN_a_call',
                free_OffN_call FLOAT PATH '$.free_OffN_call',
                free_ON_SMS FLOAT PATH '$.free_ON_SMS',
                free_OffN_SMS INT PATH '$.free_OffN_SMS',
                ON_a_call_cost DECIMAL(10,2) PATH '$.ON_a_call_cost',
                ON_SMS_cost DECIMAL(10,2) PATH '$.ON_SMS_cost',
                code VARCHAR(50) PATH '$.code',
                expiration_date DATETIME PATH '$.expiration_date'
            )
        ) AS jt;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi SQL trong khi xử lý usage hoặc cập nhật ưu đãi' AS message;
    END;

    START TRANSACTION;

    -- Ghi usage_log
    INSERT INTO usage_logs (
        type, usage_value, subscriber_id, start_date, end_date, by_from, `to`, contents
    )
    VALUES (
        p_type, p_usage_value, p_subscriber_id, p_start_date, p_end_date, p_by_from, p_to, p_contents
    );

    -- Duyệt JSON cập nhật payment_detail
    OPEN promo_cursor;
    update_loop: LOOP
        FETCH promo_cursor INTO 
            cur_payment_id,
            cur_free_data,
            cur_free_ON_a_call,
            cur_free_ON_call,
            cur_free_OffN_a_call,
            cur_free_OffN_call,
            cur_free_ON_SMS,
            cur_free_OffN_SMS,
            cur_ON_a_call_cost,
            cur_ON_SMS_cost,
            cur_code,
            cur_expiration_date;

        IF done THEN
            LEAVE update_loop;
        END IF;

        UPDATE payment_detail
        SET 
            free_data = IFNULL(cur_free_data, free_data),
            free_ON_a_call = IFNULL(cur_free_ON_a_call, free_ON_a_call),
            free_ON_call = IFNULL(cur_free_ON_call, free_ON_call),
            free_OffN_a_call = IFNULL(cur_free_OffN_a_call, free_OffN_a_call),
            free_OffN_call = IFNULL(cur_free_OffN_call, free_OffN_call),
            free_ON_SMS = IFNULL(cur_free_ON_SMS, free_ON_SMS),
            free_OffN_SMS = IFNULL(cur_free_OffN_SMS, free_OffN_SMS),
            ON_a_call_cost = IFNULL(cur_ON_a_call_cost, ON_a_call_cost),
            ON_SMS_cost = IFNULL(cur_ON_SMS_cost, ON_SMS_cost)
        WHERE payment_id = cur_payment_id;

        UPDATE payments
        SET 
            payment_date = NOW(),
            due_date = cur_expiration_date
        WHERE id = cur_payment_id;
    END LOOP;
    CLOSE promo_cursor;

    COMMIT;

    SELECT TRUE AS success, 'Đã ghi usage log và cập nhật toàn bộ ưu đãi thành công' AS message;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `AddVoucher` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddVoucher`(
    IN p_code VARCHAR(50),
    IN p_description TEXT,
    IN p_conandpromo TEXT,
    IN p_start_date DATETIME,
    IN p_end_date DATETIME,
    IN p_usage_limit INT,
    IN p_remaining_count INT,
    IN p_is_active BOOLEAN,
    IN p_staff_id INT,
    IN p_packages VARCHAR(255)
)
BEGIN
    START TRANSACTION;
    
    INSERT INTO vouchers (
        code, description, conandpromo, start_date, end_date, 
        usage_limit, remaining_count, is_active, staff_id, packages
    )
    VALUES (
        p_code, p_description, p_conandpromo, p_start_date, p_end_date,
        p_usage_limit, p_remaining_count, p_is_active, p_staff_id, p_packages
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm voucher' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm voucher thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CreateAccount` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateAccount`(
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
  DECLARE v_existing_account INT;
  DECLARE v_subscriber_id INT;
  DECLARE v_new_account_id INT;

  -- Nếu có lỗi thì rollback
  DECLARE EXIT HANDLER FOR SQLEXCEPTION 
  BEGIN
      ROLLBACK;
      SELECT FALSE AS success, 'Không thể thêm tài khoản' AS message;
  END;

  -- Bọc toàn bộ logic trong một block có nhãn
  proc_block: BEGIN

      -- Kiểm tra username đã tồn tại
      SELECT COUNT(*) INTO v_existing_account
      FROM accounts
      WHERE username = p_username;

      IF v_existing_account > 0 THEN
          SELECT FALSE AS success, 'Tên đăng nhập đã tồn tại' AS message;
          LEAVE proc_block;
      END IF;

      -- Kiểm tra username có trùng phone_number trong subscribers
      SELECT id INTO v_subscriber_id
      FROM subscribers
      WHERE phone_number = p_username
      LIMIT 1;

      IF v_subscriber_id IS NULL THEN
          SELECT FALSE AS success, 'Không tìm thấy số điện thoại tương ứng trong subscribers' AS message;
          LEAVE proc_block;
      END IF;

      -- Thực hiện tạo account + cập nhật subscriber
      START TRANSACTION;

      INSERT INTO accounts (username, password, is_active)
      VALUES (p_username, p_password, 1);

      SET v_new_account_id = LAST_INSERT_ID();

      UPDATE subscribers
      SET account_id = v_new_account_id
      WHERE id = v_subscriber_id;

      COMMIT;

      SELECT TRUE AS success, 'Thêm tài khoản thành công' AS message, v_new_account_id AS new_id;

  END proc_block;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CreateContract` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateContract`(
    IN p_title VARCHAR(255),
    IN p_contents TEXT,
    IN p_start_date DATE,
    IN p_subscriber_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm hợp đồng' AS message;
    END;

    START TRANSACTION;

    -- Vô hiệu hóa các hợp đồng cũ cùng subscriber
    UPDATE contracts
    SET is_active = 0
    WHERE subscriber_id = p_subscriber_id;

    -- Thêm hợp đồng mới
    INSERT INTO contracts (title, contents, start_date, is_active, subscriber_id, created_at)
    VALUES (p_title, p_contents, p_start_date, 1, p_subscriber_id, NOW());

    COMMIT;

    SELECT TRUE AS success, 'Thêm hợp đồng thành công' AS message, LAST_INSERT_ID() AS new_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CreateFullPaymentTransaction` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateFullPaymentTransaction`(
    IN p_plan_code VARCHAR(50),
    IN p_subscriber_id INT,
    IN p_payment_method VARCHAR(50)
)
proc: BEGIN
    DECLARE v_plan_id INT;
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_is_renewal BOOLEAN;
    DECLARE v_duration INT;
    DECLARE v_subscriber_type VARCHAR(50);
    DECLARE v_created_at DATETIME;
    DECLARE v_activation_date DATETIME;
    DECLARE v_expiration_date DATETIME;
    DECLARE v_subscription_id INT;
    DECLARE v_payment_id INT;
    DECLARE v_current_balance DECIMAL(10,2);
    DECLARE v_is_paid BOOLEAN;
    DECLARE v_due_date DATETIME;
    DECLARE v_not_found INT DEFAULT 0;

    -- HANDLERS
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT FALSE AS error, 'Có lỗi SQL xảy ra trong quá trình xử lý' AS message;
    END;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_not_found = 1;

    START TRANSACTION;

    -- 1. Lấy thông tin gói cước
    SET v_not_found = 0;
    SELECT id, price, auto_renew INTO v_plan_id, v_price, v_is_renewal
    FROM plans
    WHERE code = p_plan_code;
    IF v_not_found = 1 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Gói cước không tồn tại' AS message;
        LEAVE proc;
    END IF;

    -- 2. Lấy loại thuê bao và số dư
    SET v_not_found = 0;
    SELECT subscriber, main_balance INTO v_subscriber_type, v_current_balance
    FROM subscribers
    WHERE id = p_subscriber_id;
    IF v_not_found = 1 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Thuê bao không tồn tại' AS message;
        LEAVE proc;
    END IF;

    -- 3. Xác định trạng thái thanh toán
    SET v_is_paid = IF(v_subscriber_type = 'TRASAU', FALSE, TRUE);

    -- 4. Lấy thời hạn duration
    SET v_not_found = 0;
    SELECT duration INTO v_duration
    FROM plan_detail
    WHERE plan_id = v_plan_id AND object_type = v_subscriber_type;
    IF v_not_found = 1 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy thời hạn phù hợp cho thuê bao' AS message;
        LEAVE proc;
    END IF;

    SET v_created_at = NOW();
    SET v_activation_date = NOW();

    -- 5. Tính expiration_date
    IF v_subscriber_type = 'TRATRUOC' THEN
        IF v_duration < 1 THEN
            SET v_expiration_date = DATE_FORMAT(DATE_ADD(v_activation_date, INTERVAL ROUND(v_duration * 24) HOUR), '%Y-%m-%d %H:00:00');
        ELSE
            SET v_expiration_date = DATE_FORMAT(DATE_ADD(DATE(v_activation_date), INTERVAL v_duration DAY), '%Y-%m-%d 00:00:00');
        END IF;
    ELSE -- TRASAU
        IF v_duration < 1 THEN
            SET v_expiration_date = DATE_ADD(v_activation_date, INTERVAL ROUND(v_duration * 24) HOUR);
        ELSEIF v_duration >= 1 AND v_duration <= 27 THEN
            SET v_expiration_date = DATE_FORMAT(DATE_ADD(DATE(v_activation_date), INTERVAL 1 DAY), '%Y-%m-%d 00:00:00');
        ELSE
            -- Lấy ngày đầu tháng sau của activation_date + v_duration ngày
            SET v_expiration_date := STR_TO_DATE(
    DATE_FORMAT(DATE_ADD(LAST_DAY(v_activation_date), INTERVAL ROUND(plan_duration / 30) - 1  MONTH), '%Y-%m-01 00:00:00'),
    '%Y-%m-%d %H:%i:%s'
);

        END IF;
    END IF;

    -- 6. Tính due_date
    IF v_subscriber_type = 'TRASAU' THEN
        SET v_due_date = DATE_FORMAT(DATE_ADD(LAST_DAY(NOW()), INTERVAL 1 DAY), '%Y-%m-01 00:00:00');
    ELSE
        SET v_due_date = NOW();
    END IF;

    -- 7. Thêm subscription
    INSERT INTO subscriptions (
        plan_id, subscriber_id, expiration_date, renewal_total,
        is_renewal, created_at, activation_date
    )
    VALUES (
        v_plan_id, p_subscriber_id, v_expiration_date, v_price,
        v_is_renewal, v_created_at, v_activation_date
    );
    SET v_subscription_id = LAST_INSERT_ID();

    -- 8. Thêm payment
    INSERT INTO payments (
        subscription_id, total_amount, payment_method,
        is_paid, due_date, payment_date
    )
    VALUES (
        v_subscription_id, v_price, p_payment_method,
        v_is_paid, v_due_date, NOW()
    );
    SET v_payment_id = LAST_INSERT_ID();

    -- 9. Thêm payment_detail
    INSERT INTO payment_detail (
        payment_id, free_data, free_ON_a_call, free_OffN_a_call,
        free_ON_call, free_OffN_call, free_ON_SMS, free_OffN_SMS,
        ON_a_call_cost, ON_SMS_cost
    )
    SELECT
        v_payment_id,
        free_data, free_on_network_a_call, free_off_network_a_call,
        free_on_network_call, free_off_network_call,
        free_on_network_SMS, free_off_network_SMS,
        ON_a_call_cost, ON_SMS_cost
    FROM plans
    WHERE id = v_plan_id
    LIMIT 1;

    COMMIT;

    SELECT TRUE AS success, 'Tạo gói, thanh toán và trừ tiền thành công' AS message,
           v_subscription_id AS subscription_id,
           v_payment_id AS payment_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `create_account_from_phone` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_account_from_phone`(IN p_phone VARCHAR(20))
BEGIN
    DECLARE account_id INT;
    
    INSERT INTO accounts(username, password)
    VALUES (p_phone, p_phone); -- 
    
    SET account_id = LAST_INSERT_ID();

    SELECT account_id AS id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteAccount` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteAccount`(
    IN p_account_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT 'Lỗi: Không thể xóa tài khoản' AS error;
    END;

    START TRANSACTION;

    UPDATE accounts
    SET is_active = 0
    WHERE id = p_account_id;

    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT 'Lỗi: Không thể xóa tài khoản' AS error;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Xóa tài khoản thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteContract` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteContract`(
    IN p_contract_id INT
)
BEGIN
    DECLARE v_subscriber_id INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi: Không thể xóa hợp đồng' AS message;
    END;

    START TRANSACTION;

    -- 1. Tìm subscriber_id từ hợp đồng
    SELECT subscriber_id INTO v_subscriber_id
    FROM contracts
    WHERE id = p_contract_id;

    -- 2. Cập nhật hợp đồng -> is_active = 0 và end_date = now()
    UPDATE contracts
    SET is_active = 0, end_date = NOW()
    WHERE id = p_contract_id;

    -- 3. Nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy hợp đồng để xóa' AS message;
    ELSE
        -- 4. Khóa account tương ứng
        UPDATE accounts 
        SET is_active = 0
        WHERE id = (
            SELECT account_id FROM subscribers WHERE id = v_subscriber_id
        );

        COMMIT;
        SELECT TRUE AS success, 'Xóa hợp đồng và khóa account thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteCountry` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteCountry`(
    IN p_country_id INT
)
BEGIN
    DECLARE used_count INT DEFAULT 0;

    START TRANSACTION;

    -- Kiểm tra xem có mạng nào đang dùng country này không
    SELECT COUNT(*) INTO used_count
    FROM networks
    WHERE country_id = p_country_id;

    IF used_count > 0 THEN
        ROLLBACK;
        SELECT TRUE AS error, 'Không thể xóa. Quốc gia đang được sử dụng trong bảng networks' AS message;
    ELSE
        DELETE FROM countries
        WHERE id = p_country_id;

        IF ROW_COUNT() = 0 THEN
            ROLLBACK;
            SELECT TRUE AS error, 'Không tìm thấy quốc gia để xóa' AS message;
        ELSE
            COMMIT;
            SELECT TRUE AS success, 'Xóa quốc gia thành công' AS message;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteCustomer` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteCustomer`(
    IN p_customer_id INT
)
BEGIN
    START TRANSACTION;

    -- Khóa customer
    UPDATE customers
    SET is_active = 0
    WHERE id = p_customer_id;

    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy customer để xóa' AS message; 
    ELSE
        -- Khóa tất cả subscriber của customer đó
        UPDATE subscribers
        SET is_active = 0
        WHERE customer_id = p_customer_id;

        COMMIT;
        SELECT TRUE AS success, 'Khóa customer và toàn bộ subscriber thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteNetwork` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteNetwork`(
    IN p_id INT
)
BEGIN
    DECLARE plan_count INT DEFAULT 0;

    START TRANSACTION;

    -- Kiểm tra tồn tại trong plan_network
    SELECT COUNT(*) INTO plan_count
    FROM plan_network
    WHERE network_id = p_id;

    IF plan_count > 0 THEN
        ROLLBACK;
        SELECT FALSE AS success, 'Không thể xóa mạng vì đang được sử dụng trong gói cước' AS message;
    ELSE
        DELETE FROM networks
        WHERE id = p_id;

        IF ROW_COUNT() = 0 THEN
            ROLLBACK;
            SELECT FALSE AS success, 'Không tìm thấy mạng để xóa' AS message;
        ELSE
            COMMIT;
            SELECT TRUE AS success, 'Xóa mạng thành công' AS message;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteService` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteService`(
  IN in_service_id INT
)
BEGIN
  DECLARE cnt INT DEFAULT 0;

  -- 1) Kiểm tra có bản ghi nào trong plans tham chiếu tới service này không
  SELECT COUNT(*) INTO cnt
  FROM plans
  WHERE service_id = in_service_id;

  IF cnt > 0 THEN
    -- Nếu có tham chiếu, trả về FALSE và message
    SELECT 
      FALSE AS success,
      CONCAT(
        'Không thể xóa service_id=', in_service_id,
        ' vì đang được sử dụng trong bảng plans (', cnt, ' bản ghi).'
      ) AS message;
  ELSE
    -- Nếu không, thực hiện xóa
    DELETE FROM services
    WHERE id = in_service_id;

    -- 2) Kiểm tra kết quả xóa
    IF ROW_COUNT() = 0 THEN
      -- Không tìm thấy ID để xóa
      SELECT 
        FALSE AS success,
        CONCAT('Không tìm thấy service_id=', in_service_id, ' để xóa.') AS message;
    ELSE
      -- Xóa thành công
      SELECT TRUE AS success;
    END IF;
  END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteStaff` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteStaff`(IN p_staff_id INT)
BEGIN
    DECLARE v_account_id INT DEFAULT NULL;

    START TRANSACTION;

    -- Lấy account_id từ staff
    SELECT account_id INTO v_account_id
    FROM staffs
    WHERE id = p_staff_id;

    -- Nếu không tìm thấy thì rollback và trả về lỗi
    IF v_account_id IS NULL THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy nhân viên' AS message;
    ELSE
        -- Cập nhật is_active của staffs
        UPDATE staffs
        SET is_active = 0
        WHERE id = p_staff_id;

        -- Cập nhật is_active của accounts
        UPDATE accounts
        SET is_active = 0
        WHERE id = v_account_id;

        COMMIT;
        SELECT TRUE AS success, 'Đã khóa nhân viên thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteSubscriber` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteSubscriber`(
    IN p_subscriber_id INT
)
BEGIN
    DECLARE v_account_id INT;

    START TRANSACTION;

    -- Cập nhật trạng thái is_active của subscriber
    UPDATE subscribers
    SET is_active = 0
    WHERE id = p_subscriber_id;

    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy subscriber để xóa' AS message; 
    ELSE
        -- Lấy account_id của subscriber
        SELECT account_id INTO v_account_id
        FROM subscribers
        WHERE id = p_subscriber_id;

        -- Cập nhật trạng thái is_active của account
        UPDATE accounts
        SET is_active = 0
        WHERE id = v_account_id;

        COMMIT;
        SELECT TRUE AS success, 'Xóa subscriber thành công và đã cập nhật account' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteSubscription` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteSubscription`(

    IN p_id INT

)
BEGIN

    DECLARE v_subscriber_id INT;

    DECLARE v_subscriber_type VARCHAR(20);

    DECLARE v_is_renew INT;

    DECLARE v_service_id INT;



    DECLARE EXIT HANDLER FOR SQLEXCEPTION 

    BEGIN

        ROLLBACK;

        SELECT FALSE AS success, 'Lỗi trong quá trình hủy subscription' AS message;

    END;



    START TRANSACTION;



    -- Lấy service_id của subscription

    SELECT p.service_id

    INTO v_service_id

    FROM subscriptions s

    JOIN plans p ON s.plan_id = p.id

    WHERE s.id = p_id;



    IF v_service_id = 2 THEN

        -- Trường hợp cần kiểm tra loại thuê bao

        SELECT s.subscriber_id, sb.subscriber, s.renewal_total

        INTO v_subscriber_id, v_subscriber_type, v_is_renew

        FROM subscriptions s

        JOIN subscribers sb ON s.subscriber_id = sb.id

        WHERE s.id = p_id;



        IF v_subscriber_type = 'TRATRUOC' THEN

            -- Cho phép hủy nếu là trả trước

            UPDATE subscriptions

            SET cancel_at = NOW()

            WHERE id = p_id;



            IF ROW_COUNT() = 0 THEN

                ROLLBACK;

                SELECT FALSE AS success, 'Không tìm thấy hoặc không cập nhật subscription' AS message;

            ELSE

                COMMIT;

                SELECT TRUE AS success, 'Hủy gia hạn thành công' AS message;

            END IF;



        ELSEIF v_subscriber_type = 'TRASAU' THEN

            -- Chỉ cho phép hủy nếu số lần gia hạn >= 12

            IF v_is_renew >= 12 THEN

                UPDATE subscriptions

                SET cancel_at = NOW()

                WHERE id = p_id;



                IF ROW_COUNT() = 0 THEN

                    ROLLBACK;

                    SELECT FALSE AS success, 'Không tìm thấy hoặc không cập nhật subscription' AS message;

                ELSE

                    COMMIT;

                    SELECT TRUE AS success, 'Hủy gia hạn thành công cho thuê bao trả sau đủ điều kiện' AS message;

                END IF;

            ELSE

                ROLLBACK;

                SELECT FALSE AS success, 'Bạn không thể hủy gói cước. Phải sử dụng đủ 12 tháng' AS message;

            END IF;



        ELSE

            -- Trường hợp loại thuê bao không xác định

            ROLLBACK;

            SELECT FALSE AS success, 'Loại thuê bao không hợp lệ' AS message;

        END IF;



    ELSE

        -- Trường hợp không cần kiểm tra, chỉ cập nhật

        UPDATE subscriptions

        SET cancel_at = NOW()

        WHERE id = p_id;



        IF ROW_COUNT() = 0 THEN

            ROLLBACK;

            SELECT FALSE AS success, 'Không tìm thấy hoặc không cập nhật subscription' AS message;

        ELSE

            COMMIT;

            SELECT TRUE AS success, 'Hủy gói cước thành công ' AS message;

        END IF;

    END IF;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DeleteVoucher` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteVoucher`(
    IN p_voucher_id INT
)
BEGIN
   

    START TRANSACTION;

    UPDATE vouchers
    SET is_active = 0
    WHERE id = p_voucher_id;

    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy voucher để xóa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Xóa voucher thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetAccountById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAccountById`(
    IN p_account_id int
)
BEGIN
    DECLARE account_count INT;

    -- Kiểm tra tài khoản có tồn tại không
    SELECT COUNT(*) INTO account_count FROM accounts WHERE id = p_account_id;

    IF account_count = 0 THEN
        SELECT FALSE AS error, 'Không tìm thấy tài khoản' AS message;
    ELSE
        SELECT id, username, password, is_active 
        FROM accounts 
        WHERE id = p_account_id;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetActiveServiceIdBySubscriber` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetActiveServiceIdBySubscriber`(IN subscriber_id INT)
BEGIN
    SELECT 
        p.service_id,
        s.id
    FROM 
        plans p
    JOIN 
        subscriptions s ON p.id = s.plan_id
    WHERE 
		s.cancel_at IS NULL 
        AND s.subscriber_id = subscriber_id  -- Lọc theo subscriber_id
        AND s.expiration_date > NOW()  -- Chỉ lấy các gói cước còn hạn
	AND s.is_renewal = TRUE

    ORDER BY 
        s.expiration_date DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetActiveSubscriptionDetailsBySubscriber` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetActiveSubscriptionDetailsBySubscriber`(IN subscriber_id INT)
BEGIN

    SELECT 

        s.id AS subscription_id, 

        p.id as plan_id,

        p.code AS plan_code, 

        pd.free_data, 

        s.cancel_at,

        s.expiration_date 

    FROM 

        subscriptions s

    JOIN 

        plans p ON s.plan_id = p.id

    JOIN 

        payments pay ON s.id = pay.subscription_id

    JOIN 

        payment_detail pd ON pay.id = pd.payment_id

    WHERE 

        s.subscriber_id = subscriber_id

        AND s.expiration_date > NOW()

        AND pay.is_paid = TRUE
        AND s.cancel_at is NULL

    ORDER BY 

        s.expiration_date DESC;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetAllPlans` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAllPlans`()
BEGIN
    SELECT 
        p.id,
        p.code,
        p.price,
        p.description,
        p.service_id,
        p.is_active,
        p.renewal_syntax,
        p.registration_syntax,
        p.cancel_syntax,
        p.free_data,
        p.free_on_network_a_call,
        p.free_on_network_call,
        p.free_on_network_SMS,
        p.free_off_network_a_call,
        p.free_off_network_call,
        p.free_off_network_SMS,
        p.auto_renew,
        p.staff_id,
        p.maximum_on_network_call,
        p.ON_SMS_cost,
        p.ON_a_call_cost,
        pd.object_type,
        pd.duration
    FROM plans p
    LEFT JOIN plan_detail pd ON p.id = pd.plan_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetContractById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetContractById`(
    IN p_contract_id INT
)
BEGIN
    DECLARE contract_count INT;

    -- Kiểm tra hợp đồng có tồn tại không
    -- SELECT COUNT(*) INTO contract_count
    -- FROM contracts
    -- WHERE id = p_contract_id AND is_active = 1;

    -- IF contract_count = 0 THEN
       -- SELECT FALSE AS error, 'Không tìm thấy hợp đồng' AS message;
    -- ELSE
        SELECT id, title, contents, start_date, end_date, is_active, subscriber_id, created_at
        FROM contracts
        WHERE id = p_contract_id;
    -- END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetCountryById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCountryById`(
    IN p_id INT
)
BEGIN
    SELECT 
        id, country_name
    FROM 
        countries
    WHERE 
        id = p_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetCustomerById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCustomerById`(
    IN p_customer_id INT
)
BEGIN
    SELECT 
        id, full_name, is_active, card_id
    FROM customers
    WHERE id = p_customer_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetFunctionById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetFunctionById`(
    IN p_function_id INT
)
BEGIN
    SELECT 
        id, function_name, syntax_name
    FROM functions
    WHERE id = p_function_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetNetworkById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetNetworkById`(
    IN p_id INT
)
BEGIN
    SELECT *
    FROM networks
    WHERE id = p_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetPaymentDetailById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPaymentDetailById`(
    IN p_payment_detail_id INT
)
BEGIN
    SELECT 
        id, payment_id, free_data, free_on_a_call, free_offn_a_call,
        free_on_call, free_offn_call, free_on_sms, free_offn_sms,
        on_a_call_cost, on_sms_cost
    FROM payment_detail
    WHERE id = p_payment_detail_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetPlanById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPlanById`(
    IN p_plan_id INT
)
BEGIN
    SELECT 
        p.id,
        p.code,
        p.price,
        p.description,
        p.service_id,
        p.is_active,
        p.renewal_syntax,
        p.registration_syntax,
        p.cancel_syntax,
        p.free_data,
        p.free_on_network_a_call,
        p.free_on_network_call,
        p.free_on_network_SMS,
        p.free_off_network_a_call,
        p.free_off_network_call,
        p.free_off_network_SMS,
        p.auto_renew,
        p.staff_id,
        p.maximum_on_network_call,
        p.ON_SMS_cost,
        p.ON_a_call_cost,
        pd.object_type,
        pd.duration
    FROM plans p
    LEFT JOIN plan_detail pd ON p.id = pd.plan_id
    WHERE p.id = p_plan_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetPlanDetailById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPlanDetailById`(
    IN p_plan_detail_id INT
)
BEGIN
    SELECT 
         plan_id, object_type, duration
    FROM plan_detail
    WHERE plan_id = p_plan_detail_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetPlanNetworkById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPlanNetworkById`(
    IN p_plan_network_id INT
)
BEGIN
    SELECT 
        id, network_id, plan_id
    FROM plan_network
    WHERE id = p_plan_network_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetRoleGroupById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetRoleGroupById`(
    IN p_role_group_id INT
)
BEGIN
    SELECT 
        id, role_name
    FROM rolegroup
    WHERE id = p_role_group_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetRoleGroupDetailByRoleGroupId` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetRoleGroupDetailByRoleGroupId`(
    IN p_role_group_id INT
)
BEGIN
    SELECT 
        role_group_id, function_id
    FROM rolegroupdetail
    WHERE role_group_id = p_role_group_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetRoleGroupFunctionsAndAvailableFunctions` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetRoleGroupFunctionsAndAvailableFunctions`(role_group_id INT)
BEGIN
    -- Lấy tất cả các chức năng đã được gán cho nhóm quyền
    SELECT f.id, f.function_name
    FROM functions f
    INNER JOIN rolegroupdetail rgd ON f.id = rgd.function_id
    WHERE rgd.role_group_id = role_group_id;

    -- Lấy tất cả các chức năng chưa được gán cho nhóm quyền
    SELECT f.id, f.function_name
    FROM functions f
    LEFT JOIN rolegroupdetail rgd ON f.id = rgd.function_id AND rgd.role_group_id = role_group_id
    WHERE rgd.function_id IS NULL;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetServiceById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetServiceById`(
    IN p_service_id INT
)
BEGIN
    SELECT 
        id, service_name, parent_id, coverage_area
    FROM services
    WHERE id = p_service_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetStaffByAccountId` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetStaffByAccountId`(
    IN p_account_id INT
)
BEGIN
    SELECT 
        id, full_name, card_id, phone, email, is_active, gender, birthday
    FROM staffs
    WHERE account_id = p_account_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetStaffById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetStaffById`(
    IN p_staff_id INT
)
BEGIN
    SELECT 
        id, full_name, card_id, phone, email, is_active, gender, birthday, account_id
    FROM staffs
    WHERE id = p_staff_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetStaffsByRoleGroupId` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetStaffsByRoleGroupId`(IN role_group_id INT)
BEGIN
    SELECT 
        s.id AS staff_id,
        s.full_name,
        s.card_id,
        s.phone,
        s.email,
        s.gender,
        s.birthday,
        a.username AS account_username,
        s.account_id AS account_id
    FROM 
        staffs s
    JOIN permissiondetail pd ON s.account_id = pd.account_id
    JOIN accounts a ON s.account_id = a.id
    WHERE 
        pd.role_group_id = role_group_id AND s.is_active = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetSubscriberById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetSubscriberById`(
    IN p_subscriber_id INT
)
BEGIN
    SELECT 
        id, phone_number, main_balance, activation_date, expiration_date, 
        is_active, customer_id, warning_date
    FROM subscribers
    WHERE id = p_subscriber_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetSubscriptionById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetSubscriptionById`(
    IN p_subscription_id INT
)
BEGIN
    SELECT 
        id, plan_id, subscriber_id, created_at, expiration_date, renewal_total, 
        is_renewal, cancel_at, activation_date
    FROM subscriptions
    WHERE id = p_subscription_id ;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetUsageLogById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetUsageLogById`(IN p_id INT)
BEGIN
    SELECT id, type, usage_value, subscriber_id, start_date, end_date, by_from, `to`, contents
    FROM usage_logs
    WHERE id = p_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetUsageLogBySubscriberId` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetUsageLogBySubscriberId`(IN subscriber_id INT)
BEGIN

    SELECT id, type, usage_value, subscriber_id, start_date, end_date, by_from, `to`, contents

    FROM usage_logs

    WHERE subscriber_id = subscriber_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetVoucherById` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetVoucherById`(
    IN p_voucher_id INT
)
BEGIN
    SELECT 
        id, code, description, conandpromo, start_date, end_date, 
        usage_limit, remaining_count, is_active, staff_id, packages
    FROM vouchers
    WHERE id = p_voucher_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `LockPlan` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `LockPlan`(
    IN p_plan_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Lỗi hệ thống khi khóa gói cước';
    END;

    -- Kiểm tra gói cước tồn tại
    IF NOT EXISTS (SELECT 1 FROM plans WHERE id = p_plan_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Gói cước không tồn tại';
    END IF;

    -- Kiểm tra gói cước đã bị khóa chưa
    IF EXISTS (SELECT 1 FROM plans WHERE id = p_plan_id AND is_active = 0) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Gói cước đã bị khóa';
    END IF;

    -- Khóa gói cước
    UPDATE plans
    SET is_active = 0, updated_at = NOW()
    WHERE id = p_plan_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `RemoveFunctionFromRoleGroup` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `RemoveFunctionFromRoleGroup`(
    IN p_role_group_id INT,
    IN p_function_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    -- Thực hiện xóa chức năng khỏi nhóm quyền
    DELETE FROM rolegroupdetail
    WHERE role_group_id = p_role_group_id
    AND function_id = p_function_id;

    -- Kiểm tra số lượng bản ghi bị xóa
    IF ROW_COUNT() > 0 THEN
        -- Trả về kết quả thành công
        SET p_success = TRUE;
        SET p_message = 'Chức năng đã được xóa thành công';
    ELSE
        -- Nếu không có bản ghi nào bị xóa, trả về lỗi
        SET p_success = FALSE;
        SET p_message = 'Lỗi: Chức năng không tìm thấy trong nhóm quyền';
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `Run_AutoRenew_Manual` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `Run_AutoRenew_Manual`()
BEGIN
   DECLARE done INT DEFAULT FALSE;
   DECLARE sub_id INT;
   DECLARE plan_id INT;
   DECLARE subscriber_id INT;
   DECLARE plan_price DECIMAL(10,2);
   DECLARE plan_duration INT;
   DECLARE subscriber_balance DECIMAL(10,2);
   DECLARE subscriber_type VARCHAR(45);
   DECLARE phone_number VARCHAR(15);
   DECLARE plan_code VARCHAR(50);
   DECLARE plan_desc TEXT;
   DECLARE free_data INT;
   DECLARE free_on_a_call INT;
   DECLARE free_on_call INT;
   DECLARE free_on_sms INT;
   DECLARE free_off_a_call INT;
   DECLARE free_off_call INT;
   DECLARE free_off_sms INT;
   DECLARE max_on_call INT;
   DECLARE on_sms_cost DECIMAL(10,0);
   DECLARE on_a_call_cost DECIMAL(10,0);
   DECLARE unpaid_total DECIMAL(10,2) DEFAULT 0;
   DECLARE v_last_log_time DATETIME;
   DECLARE v_activation_date DATETIME;
   DECLARE v_new_expiration DATETIME;
   DECLARE v_due_date DATETIME;

   DECLARE cur CURSOR FOR
     SELECT s.id, s.plan_id, s.subscriber_id
     FROM subscriptions s
     JOIN subscribers sub ON sub.id = s.subscriber_id
     WHERE sub.is_active = TRUE
       AND s.cancel_at IS NULL
       AND s.expiration_date <= NOW()
       AND s.is_renewal = 1;

   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

   OPEN cur;

   read_loop: LOOP
     FETCH cur INTO sub_id, plan_id, subscriber_id;
     IF done THEN
       LEAVE read_loop;
     END IF;

SELECT 
    sub.main_balance, sub.subscriber, sub.phone_number
INTO subscriber_balance , subscriber_type , phone_number FROM
    subscribers sub
WHERE
    sub.id = subscriber_id;

SELECT 
    p.price,
    p.code,
    p.description,
    p.free_data,
    p.free_on_network_a_call,
    p.free_on_network_call,
    p.free_on_network_SMS,
    p.free_off_network_a_call,
    p.free_off_network_call,
    p.free_off_network_SMS,
    p.maximum_on_network_call,
    p.ON_SMS_cost,
    p.ON_a_call_cost
INTO plan_price , plan_code , plan_desc , free_data , free_on_a_call , free_on_call , free_on_sms , free_off_a_call , free_off_call , free_off_sms , max_on_call , on_sms_cost , on_a_call_cost FROM
    plans p
WHERE
    p.id = plan_id;

SELECT 
    activation_date
INTO v_activation_date FROM
    subscriptions
WHERE
    id = sub_id;

SELECT 
    pd.duration
INTO plan_duration FROM
    plan_detail pd
WHERE
    pd.plan_id = plan_id
        AND pd.object_type = subscriber_type
LIMIT 1;

     IF subscriber_type = 'TRASAU' THEN
       SELECT IFNULL(SUM(total_amount), 0) INTO unpaid_total
       FROM payments
       WHERE subscription_id = sub_id AND is_paid = 0;

       IF unpaid_total > 0 THEN
         IF subscriber_balance >= unpaid_total THEN
           UPDATE payments
           SET is_paid = 1, payment_date = NOW()
           WHERE subscription_id = sub_id AND is_paid = 0;

UPDATE subscribers 
SET 
    main_balance = main_balance - unpaid_total
WHERE
    id = subscriber_id;

           INSERT INTO usage_logs (type, usage_value, subscriber_id, start_date, end_date, `by_from`, `to`, contents)
           VALUES ('TINNHAN', 1, subscriber_id, NOW(), NOW(), '191', phone_number,
                   CONCAT(plan_code, ' đã thanh toán nợ cước ', unpaid_total));
         ELSE
           INSERT INTO usage_logs (type, usage_value, subscriber_id, start_date, end_date, `by_from`, `to`, contents)
           VALUES ('TINNHAN', 1, subscriber_id, NOW(), NOW(), '191', phone_number,
                   CONCAT(plan_code, ' chưa thanh toán nợ (', unpaid_total, '). Không thể gia hạn.'));
           ITERATE read_loop;
         END IF;
       END IF;
     END IF;

     IF subscriber_balance >= plan_price OR subscriber_type = 'TRASAU' THEN
	--  Tính expiration mới từ activation_date (áp dụng logic đã chuẩn hóa)
IF subscriber_type = 'TRATRUOC' THEN
    IF plan_duration < 1 THEN
        SET v_new_expiration := STR_TO_DATE(
            DATE_FORMAT(DATE_ADD(v_activation_date, INTERVAL ROUND(plan_duration * 24) HOUR), '%Y-%m-%d %H:00:00'),
            '%Y-%m-%d %H:%i:%s'
        );
    ELSE
        SET v_new_expiration := STR_TO_DATE(
            DATE_FORMAT(DATE_ADD(DATE(v_activation_date), INTERVAL plan_duration DAY), '%Y-%m-%d 00:00:00'),
            '%Y-%m-%d %H:%i:%s'
        );
    END IF;
ELSE -- TRASAU
    IF plan_duration < 1 THEN
        SET v_new_expiration := STR_TO_DATE(
            DATE_FORMAT(DATE_ADD(v_activation_date, INTERVAL ROUND(plan_duration * 24) HOUR), '%Y-%m-%d %H:00:00'),
            '%Y-%m-%d %H:%i:%s'
        );
    ELSEIF plan_duration >= 1 AND plan_duration <= 27 THEN
        SET v_new_expiration := STR_TO_DATE(
            DATE_FORMAT(DATE_ADD(DATE(v_activation_date), INTERVAL 1 DAY), '%Y-%m-%d 00:00:00'),
            '%Y-%m-%d %H:%i:%s'
        );
    ELSE
        SET v_new_expiration := STR_TO_DATE(
    DATE_FORMAT(DATE_ADD(LAST_DAY(v_activation_date), INTERVAL ROUND(plan_duration / 30) -1 MONTH), '%Y-%m-01 00:00:00'),
    '%Y-%m-%d %H:%i:%s'
);

    END IF;
END IF;

--  Tính due_date chuẩn
IF subscriber_type = 'TRASAU' THEN
    SET v_due_date := STR_TO_DATE(
        DATE_FORMAT(DATE_ADD(LAST_DAY(NOW()), INTERVAL 1 DAY), '%Y-%m-01 00:00:00'),
        '%Y-%m-%d %H:%i:%s'
    );
ELSE
    SET v_due_date := NOW();
END IF;


       UPDATE subscriptions
       SET 
         renewal_total = renewal_total + 1,
         activation_date = NOW(),
         expiration_date = v_new_expiration
       WHERE id = sub_id;

       INSERT INTO usage_logs (type, usage_value, subscriber_id, start_date, end_date, `by_from`, `to`, contents)
       VALUES ('TINNHAN', 1, subscriber_id, NOW(), NOW(), '191', phone_number,
               CONCAT(plan_code, ' gia hạn thành công'));

       INSERT INTO payments (
         subscription_id, total_amount, payment_method, is_paid, payment_date, due_date
       )
       VALUES (
         sub_id, plan_price, 'main_balance',
         IF(subscriber_type = 'TRASAU', 0, 1),
         NOW(), v_due_date
       );

       INSERT INTO payment_detail (
         payment_id,
         free_data,
         free_ON_a_call,
         free_OffN_a_call,
         free_ON_call,
         free_OffN_call,
         free_ON_SMS,
         free_OffN_SMS,
         ON_a_call_cost,
         ON_SMS_cost
       )
       VALUES (
         LAST_INSERT_ID(),
         free_data,
         free_on_a_call,
         free_off_a_call,
         free_on_call,
         free_off_call,
         free_on_sms,
         free_off_sms,
         on_a_call_cost,
         on_sms_cost
       );

       IF subscriber_type = 'TRATRUOC' THEN
         UPDATE subscribers
         SET main_balance = main_balance - plan_price
         WHERE id = subscriber_id;
       END IF;

     ELSE
       IF subscriber_type = 'TRATRUOC' OR unpaid_total = 0 THEN
         SELECT MAX(start_date)
         INTO v_last_log_time
         FROM usage_logs
         WHERE subscriber_id = subscriber_id
           AND contents LIKE CONCAT('%', plan_code, ' gia hạn thất bại%');

         IF v_last_log_time IS NULL OR TIMESTAMPDIFF(MINUTE, v_last_log_time, NOW()) >= 240 THEN
           INSERT INTO usage_logs (type, usage_value, subscriber_id, start_date, end_date, `by_from`, `to`, contents)
           VALUES ('TINNHAN', 1, subscriber_id, NOW(), NOW(), '191', phone_number,
                   CONCAT(plan_code, ' gia hạn thất bại (không đủ tiền)'));
         END IF;
       END IF;
     END IF;

   END LOOP;

   CLOSE cur;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SearchPlans` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `SearchPlans`(
    IN p_code VARCHAR(50),
    IN p_price FLOAT,
    IN p_is_active BIT,
    IN p_object_type VARCHAR(50)
)
BEGIN
    SELECT 
        p.id,
        p.code,
        p.price,
        p.description,
        p.service_id,
        p.is_active,
        p.renewal_syntax,
        p.registration_syntax,
        p.cancel_syntax,
        p.free_data,
        p.free_on_network_a_call,
        p.free_on_network_call,
        p.free_on_network_SMS,
        p.free_off_network_a_call,
        p.free_off_network_call,
        p.free_off_network_SMS,
        p.auto_renew,
        p.staff_id,
        p.maximum_on_network_call,
        p.ON_SMS_cost,
        p.ON_a_call_cost,
        pd.object_type,
        pd.duration
    FROM plans p
    LEFT JOIN plan_detail pd ON p.id = pd.plan_id
    WHERE 
        (p_code IS NULL OR p.code LIKE CONCAT('%', p_code, '%'))
        AND (p_price IS NULL OR ABS(p.price - p_price) < 0.01) -- So sánh gần đúng
        AND (p_is_active IS NULL OR p.is_active = p_is_active)
        AND (p_object_type IS NULL OR pd.object_type = p_object_type);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SearchStaffs` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `SearchStaffs`(
    IN p_full_name VARCHAR(100),
    IN p_account_id VARCHAR(50),
    IN p_gender VARCHAR(10),
    IN p_is_active INT,
    IN p_role_name VARCHAR(50)
)
BEGIN
    SELECT s.*, rg.role_name
    FROM staffs s
    JOIN accounts a ON s.account_id = a.id
    JOIN permissiondetail pd ON a.id = pd.account_id
    JOIN rolegroup rg ON pd.role_group_id = rg.id
    WHERE 
        (p_full_name IS NULL OR s.full_name LIKE CONCAT('%', p_full_name, '%')) AND
        (p_account_id IS NULL OR s.account_id LIKE CONCAT('%', p_account_id, '%')) AND
        (p_gender IS NULL OR s.gender = p_gender) AND
        (p_is_active IS NULL OR s.is_active = p_is_active) AND
        (p_role_name IS NULL OR rg.role_name = p_role_name);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SearchUsageLogs` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `SearchUsageLogs`(
    IN p_type VARCHAR(50),
    IN p_subscriber_id INT,
    IN p_start_date DATETIME
)
BEGIN
    SELECT id, type, usage_value, subscriber_id, start_date, end_date, by_from, `to`, contents
    FROM usage_logs
    WHERE type = p_type
        AND subscriber_id = p_subscriber_id
        AND (p_start_date IS NULL OR DATE(start_date) = DATE(p_start_date));
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_accounts_update` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_accounts_update`(
    IN p_staff_id INT,
    IN p_password VARCHAR(255)
)
BEGIN
    DECLARE acc_count INT DEFAULT 0;
    DECLARE v_account_id INT;

    -- Lấy account_id từ bảng staff
    SELECT account_id INTO v_account_id
    FROM staffs
    WHERE id = p_staff_id;

    -- Kiểm tra account_id có tồn tại không
    IF v_account_id IS NULL THEN
        SELECT 0 AS success, 'Không tìm thấy tài khoản cho nhân viên với ID đã cho' AS message;
    ELSE
        SELECT COUNT(*) INTO acc_count FROM accounts WHERE id = v_account_id;

        IF acc_count = 0 THEN
            SELECT 0 AS success, 'Tài khoản không tồn tại' AS message;
        ELSE
            UPDATE accounts
            SET password = p_password
            WHERE id = v_account_id;

            SELECT 1 AS success, 'Cập nhật mật khẩu thành công' AS message;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_accounts_update_password_by_username` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_accounts_update_password_by_username`(
        IN p_username VARCHAR(255),
        IN p_new_password VARCHAR(255)
    )
BEGIN
        UPDATE accounts
        SET password = p_new_password
        WHERE username = p_username;
    END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_account_check_login` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_account_check_login`(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255),
    OUT p_status INT,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_account_id INT;
    DECLARE v_is_active TINYINT;

    -- Reset trạng thái mặc định
    SET p_status = 0;
    SET p_message = 'Tài khoản không tồn tại hoặc mật khẩu sai';

    -- Kiểm tra thông tin tài khoản
    SELECT id, is_active INTO v_account_id, v_is_active
    FROM accounts
    WHERE username = p_username AND password = p_password
    LIMIT 1;

    -- Nếu tìm được tài khoản
    IF v_account_id IS NOT NULL THEN
        IF v_is_active = 0 THEN
            SET p_status = 0;
            SET p_message = 'Tài khoản đã bị vô hiệu hóa';
        ELSE
            SET p_status = 1;
            SET p_message = 'Đăng nhập thành công';

            -- Ưu tiên lấy thông tin từ subscribers nếu có
            IF EXISTS (
                SELECT 1 FROM subscribers WHERE account_id = v_account_id
            ) THEN
                SELECT
                    'subscriber' AS role_type,
                    s.id AS subscriber_id,
                    c.full_name AS customer_name,
                    s.phone_number,
                    s.main_balance,
                    s.subscriber AS subscriber_type,
                    s.account_id
                FROM subscribers s
                JOIN customers c ON s.customer_id = c.id
                WHERE s.account_id = v_account_id
                LIMIT 1;
            ELSE
                -- Nếu không phải subscriber, kiểm tra trong staffs
                SELECT
                    'staff' AS role_type,
                    st.id AS staff_id,
                    st.full_name,
                    st.email,
                    st.phone,
                    st.gender,
                    st.account_id
                FROM staffs st
                WHERE st.account_id = v_account_id
                LIMIT 1;
            END IF;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_add_multiple_permissiondetails_from_csv` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_add_multiple_permissiondetails_from_csv`(
    IN p_role_group_id INT,
    IN p_account_ids TEXT
)
BEGIN
    DECLARE v_account_id INT;
    DECLARE v_comma_index INT;

    -- Bắt lỗi nếu có vấn đề
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Đã xảy ra lỗi khi thêm permission detail' AS message;
    END;

    START TRANSACTION;

    label_loop: LOOP
        SET v_comma_index = LOCATE(',', p_account_ids);

        IF v_comma_index > 0 THEN
            SET v_account_id = CAST(SUBSTRING(p_account_ids, 1, v_comma_index - 1) AS UNSIGNED);
            SET p_account_ids = SUBSTRING(p_account_ids, v_comma_index + 1);
        ELSE
            SET v_account_id = CAST(p_account_ids AS UNSIGNED);
            SET p_account_ids = NULL;
        END IF;

        INSERT IGNORE INTO permissiondetail (role_group_id, account_id)
        VALUES (p_role_group_id, v_account_id);

        IF p_account_ids IS NULL OR p_account_ids = '' THEN
            LEAVE label_loop;
        END IF;
    END LOOP;

    COMMIT;
    SELECT TRUE AS success, 'Đã thêm các account vào permissiondetail' AS message;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_apply_voucher_to_plan` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_apply_voucher_to_plan`(
    IN p_plan_code VARCHAR(50),
    IN p_subscriber_id INT
)
BEGIN
    DECLARE v_plan_id INT;
    DECLARE v_renewal_total INT;
    DECLARE v_subscriber_type VARCHAR(50);
    DECLARE v_activation_day INT;

    DECLARE v_total_amount DECIMAL(10,2) DEFAULT 0;
    DECLARE v_bonus_data INT DEFAULT 0;
    DECLARE v_discount_percent DECIMAL(5,2) DEFAULT 0;

    -- Lấy ID plan
    SELECT id INTO v_plan_id FROM plans WHERE code = p_plan_code;

    -- Lấy renewal_total, ngày đăng ký và loại thuê bao
    SELECT s.renewal_total, DAY(s.activation_date), sub.subscriber
    INTO v_renewal_total, v_activation_day, v_subscriber_type
    FROM subscriptions s
    JOIN subscribers sub ON sub.id = s.subscriber_id
    WHERE s.plan_id = v_plan_id AND s.subscriber_id = p_subscriber_id
    ORDER BY s.id DESC
    LIMIT 1;

    -- Kiểm tra khuyến mãi tặng 500MB nếu ST5K và renewal_total = 2
    IF p_plan_code = 'ST5K' AND v_renewal_total = 2 THEN
        SET v_bonus_data = v_bonus_data + 500;
    END IF;

    -- Kiểm tra khuyến mãi giảm 50% nếu TRASAU và ngày đăng ký từ 21-31 và gói SD90
    IF v_subscriber_type = 'TRASAU' AND v_activation_day BETWEEN 21 AND 31 AND p_plan_code = 'SD90' THEN
        SET v_discount_percent = 0.5;
    END IF;

    -- Lấy giá gói gốc
    SELECT price INTO v_total_amount FROM plans WHERE id = v_plan_id;

    -- Áp dụng giảm giá nếu có
    IF v_discount_percent > 0 THEN
        SET v_total_amount = v_total_amount * v_discount_percent;
    END IF;

    -- Trả kết quả
    SELECT 
        v_plan_id AS plan_id,
        v_total_amount AS final_price,
        v_bonus_data AS free_data_bonus,
        v_discount_percent AS discount_applied;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_auto_increment_usage_value` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_auto_increment_usage_value`()
BEGIN
    UPDATE usage_logs
    SET usage_value = usage_value + 1
    WHERE end_date IS NULL
      AND (type = 'CUOCGOI' OR type = 'DULIEU')
      AND start_date <= NOW()
      AND id >0; -- id là PRIMARY KEY;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_cancel_expired_subscriptions` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_cancel_expired_subscriptions`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_sub_id INT;
    DECLARE v_subscriber_id INT;
    DECLARE v_plan_id INT;
    DECLARE v_plan_code VARCHAR(50);
    DECLARE v_phone VARCHAR(15);
	
    -- Cursor để duyệt qua các subscription hết hạn
    DECLARE cur CURSOR FOR
        SELECT s.id, s.subscriber_id, s.plan_id, p.code, sub.phone_number
        FROM subscriptions s
        JOIN plans p ON s.plan_id = p.id
        JOIN subscribers sub ON sub.id = s.subscriber_id
        WHERE s.cancel_at IS NULL
          AND s.expiration_date <= DATE_SUB(NOW(), INTERVAL 1 DAY);
		
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_sub_id, v_subscriber_id, v_plan_id, v_plan_code, v_phone;
        IF done THEN
            LEAVE read_loop;
        END IF;
	
        -- Hủy gói
        UPDATE subscriptions
        SET cancel_at = NOW()
        WHERE id = v_sub_id;

        -- Ghi log hủy gói
        INSERT INTO usage_logs (
            type, usage_value, subscriber_id,
            start_date, end_date, `by_from`, `to`, contents
        ) VALUES (
            'TINNHAN', 1, v_subscriber_id,
            NOW(), NOW(), '191', v_phone,
            CONCAT('Gói ', v_plan_code, ' đã hết hạn. Hủy tự động.')
        );
        SELECT "DONE";
    END LOOP;

    CLOSE cur;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_check_and_consume_pending_usage` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_check_and_consume_pending_usage`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_id INT;
    DECLARE v_type VARCHAR(50);
    DECLARE v_by_from VARCHAR(15);
    DECLARE v_to VARCHAR(15);
    DECLARE v_start DATETIME;
    DECLARE v_end DATETIME;
    DECLARE v_usage_value INT;

    DECLARE cur CURSOR FOR
        SELECT id, type, usage_value, by_from, `to`, start_date, end_date
        FROM usage_logs
        WHERE usage_value > 0;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_id, v_type, v_usage_value, v_by_from, v_to, v_start, v_end;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Gọi xử lý trừ vào payment_detail
        CALL sp_consume_resources_from_usage_log(
            v_id, v_type, v_usage_value, v_by_from, v_to, v_start, v_end
        );

        
    END LOOP;

    CLOSE cur;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_check_subscriber_phone` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_check_subscriber_phone`(
    IN p_phone_number VARCHAR(20)
)
BEGIN
    DECLARE is_subscriber BOOLEAN DEFAULT FALSE;

    -- Kiểm tra xem số điện thoại có tồn tại trong bảng subscribers không
    IF EXISTS (
        SELECT 1
        FROM subscribers
        WHERE phone_number = p_phone_number
    ) THEN
        SET is_subscriber = TRUE;
    END IF;

    -- Trả về kết quả
    SELECT is_subscriber AS is_subscriber;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_check_voucher_effects` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_check_voucher_effects`(IN p_subscription_id INT)
BEGIN
    DECLARE v_subscriber_id INT;
    DECLARE v_plan_id INT;
    DECLARE v_renewal_total INT;
    DECLARE v_created_at DATETIME;
    DECLARE v_subscriber_type VARCHAR(20);
    DECLARE v_plan_price DECIMAL(10,2);
    DECLARE v_plan_free_data DECIMAL(10,0);

    DECLARE v_code VARCHAR(50);
    DECLARE v_conandpromo JSON;

    DECLARE v_discount DECIMAL(10,2);
    DECLARE v_bonus_data DECIMAL(10,0);

    DECLARE done INT DEFAULT FALSE;

    DECLARE cur CURSOR FOR 
        SELECT code, conandpromo
        FROM vouchers
        WHERE is_active = 1 
            AND start_date <= CURDATE() 
            AND end_date >= CURDATE() 
            AND remaining_count < usage_limit;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Lấy thông tin subscription, subscriber, plan
    SELECT s.plan_id, s.subscriber_id, s.renewal_total, s.created_at, sub.subscriber
    INTO v_plan_id, v_subscriber_id, v_renewal_total, v_created_at, v_subscriber_type
    FROM subscriptions s
    JOIN subscribers sub ON s.subscriber_id = sub.id
    WHERE s.id = p_subscription_id;

    SELECT price, free_data
    INTO v_plan_price, v_plan_free_data
    FROM plans
    WHERE id = v_plan_id;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_code, v_conandpromo;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Kiểm tra điều kiện JSON
        IF 
           (JSON_CONTAINS(JSON_EXTRACT(v_conandpromo, '$.condition.plan_id'), CAST(v_plan_id AS JSON)) OR JSON_EXTRACT(v_conandpromo, '$.condition.plan_id') IS NULL)
           AND (JSON_CONTAINS(JSON_EXTRACT(v_conandpromo, '$.condition.subscriber'), JSON_QUOTE(v_subscriber_type)) OR JSON_EXTRACT(v_conandpromo, '$.condition.subscriber') IS NULL)
           AND (JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.condition.renewal_total')) = v_renewal_total OR JSON_EXTRACT(v_conandpromo, '$.condition.renewal_total') IS NULL)
           AND (
                JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.condition.created_at')) IS NULL OR
                (DAY(v_created_at) BETWEEN 21 AND DAY(LAST_DAY(v_created_at)))
           )
        THEN
            -- Mặc định giữ nguyên
            SET v_discount = v_plan_price;
            SET v_bonus_data = v_plan_free_data;

            -- Xử lý giảm giá
            IF JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.operator') IS NOT NULL AND
               JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.value') IS NOT NULL THEN

                IF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.operator')) = '*' THEN
                    SET v_discount = v_plan_price * CAST(JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.value')) AS DECIMAL(10,2));
                ELSEIF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.operator')) = '-' THEN
                    SET v_discount = v_plan_price - CAST(JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.value')) AS DECIMAL(10,2));
                END IF;
            END IF;

            -- Xử lý tăng dữ liệu
            IF JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.operator') IS NOT NULL AND
               JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.value') IS NOT NULL THEN

                IF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.operator')) = '+' THEN
                    SET v_bonus_data = v_plan_free_data + CAST(JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.value')) AS DECIMAL(10,0));
                ELSEIF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.operator')) = '*' THEN
                    SET v_bonus_data = v_plan_free_data * CAST(JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.value')) AS DECIMAL(10,0));
                END IF;
            END IF;

            -- Xuất kết quả
            SELECT 
                v_code AS voucher_code,
                v_discount AS total_amount_after_voucher,
                v_bonus_data AS free_data_after_voucher;
        END IF;

    END LOOP;

    CLOSE cur;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_check_voucher_effects1` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_check_voucher_effects1`(
    IN p_subscription_id INT,
    OUT p_voucher_code VARCHAR(50),
    OUT p_discount DECIMAL(10,2),
    OUT p_bonus_data DECIMAL(10,0)
)
BEGIN
    DECLARE v_subscriber_id INT;
    DECLARE v_plan_id INT;
    DECLARE v_renewal_total INT;
    DECLARE v_created_at DATETIME;
    DECLARE v_subscriber_type VARCHAR(20);
    DECLARE v_plan_price DECIMAL(10,2);
    DECLARE v_plan_free_data DECIMAL(10,0);

    DECLARE v_code VARCHAR(50);
    DECLARE v_conandpromo JSON;

    DECLARE done INT DEFAULT FALSE;
    DECLARE voucher_found BOOLEAN DEFAULT FALSE;

    DECLARE cur CURSOR FOR 
        SELECT code, conandpromo
        FROM vouchers
        WHERE is_active = 1 
            AND start_date <= CURDATE() 
            AND end_date >= CURDATE() 
            AND remaining_count > 0;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Lấy dữ liệu đầu vào
    SELECT s.plan_id, s.subscriber_id, s.renewal_total, s.created_at, sub.subscriber
    INTO v_plan_id, v_subscriber_id, v_renewal_total, v_created_at, v_subscriber_type
    FROM subscriptions s
    JOIN subscribers sub ON s.subscriber_id = sub.id
    WHERE s.id = p_subscription_id;

    SELECT price, free_data
    INTO v_plan_price, v_plan_free_data
    FROM plans
    WHERE id = v_plan_id;

    -- Gán mặc định nếu không có voucher nào được áp dụng
    SET p_voucher_code = NULL;
    SET p_discount = v_plan_price;
    SET p_bonus_data = v_plan_free_data;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_code, v_conandpromo;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Kiểm tra điều kiện
        IF 
           (JSON_CONTAINS(JSON_EXTRACT(v_conandpromo, '$.condition.plan_id'), CAST(v_plan_id AS JSON)) OR JSON_EXTRACT(v_conandpromo, '$.condition.plan_id') IS NULL)
           AND (JSON_CONTAINS(JSON_EXTRACT(v_conandpromo, '$.condition.subscriber'), JSON_QUOTE(v_subscriber_type)) OR JSON_EXTRACT(v_conandpromo, '$.condition.subscriber') IS NULL)
           AND (JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.condition.renewal_total')) = v_renewal_total OR JSON_EXTRACT(v_conandpromo, '$.condition.renewal_total') IS NULL)
           AND (
                JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.condition.created_at')) IS NULL OR
                (DAY(v_created_at) BETWEEN 21 AND DAY(LAST_DAY(v_created_at)))
           )
        THEN
            -- Áp dụng ưu đãi
            SET p_voucher_code = v_code;

            -- Tính giảm giá
            IF JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.operator') IS NOT NULL AND
               JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.value') IS NOT NULL THEN

                IF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.operator')) = '*' THEN
                    SET p_discount = v_plan_price * CAST(JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.value')) AS DECIMAL(10,2));
                ELSEIF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.operator')) = '-' THEN
                    SET p_discount = v_plan_price - CAST(JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payments.total_amount.value')) AS DECIMAL(10,2));
                ELSE
                    SET p_discount = v_plan_price;
                END IF;
            ELSE
                SET p_discount = v_plan_price;
            END IF;

            -- Tính bonus data
            IF JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.operator') IS NOT NULL AND
               JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.value') IS NOT NULL THEN

                IF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.operator')) = '+' THEN
                    SET p_bonus_data = v_plan_free_data + CAST(JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.value')) AS DECIMAL(10,0));
                ELSEIF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.operator')) = '*' THEN
                    SET p_bonus_data = v_plan_free_data * CAST(JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.payment_detail.free_data.value')) AS DECIMAL(10,0));
                ELSE
                    SET p_bonus_data = v_plan_free_data;
                END IF;
            ELSE
                SET p_bonus_data = v_plan_free_data;
            END IF;

            -- Giảm số lượng còn lại của voucher
            UPDATE vouchers
            SET remaining_count = remaining_count - 1
            WHERE code = v_code;

            LEAVE read_loop; -- chỉ lấy voucher đầu tiên hợp lệ
        END IF;

    END LOOP;

    CLOSE cur;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_consume_resources_from_usage_log` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_consume_resources_from_usage_log`(
    IN p_usage_log_id INT,
    IN p_type VARCHAR(50),
    IN p_usage_value INT,
    IN p_by_from VARCHAR(15),
    IN p_to VARCHAR(15),
    IN p_start DATETIME,
    IN p_end DATETIME
)
BEGIN
    DECLARE v_remaining INT DEFAULT p_usage_value;
    DECLARE v_subscriber_id INT;
    DECLARE v_payment_id INT;
    DECLARE v_is_internal BOOLEAN DEFAULT NULL;
    DECLARE v_to_exists BOOLEAN DEFAULT FALSE;
    DECLARE v_deduct INT DEFAULT 0;
    DECLARE v_service_id INT;
    DECLARE done INT DEFAULT FALSE;

    DECLARE cur CURSOR FOR
        SELECT p.id, pl.service_id
        FROM subscriptions s
        JOIN subscribers sub ON s.subscriber_id = sub.id
        JOIN plans pl ON s.plan_id = pl.id
        JOIN (
            SELECT subscription_id, MAX(payment_date) AS latest_date
            FROM payments
            GROUP BY subscription_id
        ) latest ON latest.subscription_id = s.id
        JOIN payments p ON p.subscription_id = s.id AND p.payment_date = latest.latest_date
        WHERE sub.phone_number = p_by_from
          AND s.expiration_date >= NOW()
        ORDER BY 
            CASE WHEN pl.service_id = 1 THEN 0 ELSE 1 END,
            p.payment_date ASC;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    proc_block: BEGIN

        IF p_type IN ('CUOCGOI', 'TINNHAN') THEN
            SELECT id INTO v_subscriber_id
            FROM subscribers
            WHERE phone_number = p_by_from
            LIMIT 1;

            IF EXISTS (
                SELECT 1 FROM usage_logs
                WHERE id = p_usage_log_id AND subscriber_id != v_subscriber_id
            ) THEN
                SELECT 'by_from không đúng với subscriber_id trong usage_logs' AS error_message;
                LEAVE proc_block;
            END IF;

            SELECT COUNT(*) > 0 INTO v_to_exists
            FROM subscribers
            WHERE phone_number = p_to;

            SET v_is_internal = v_to_exists;
            SELECT CONCAT('Kiểm tra nội mạng: ', IF(v_is_internal, 'Nội mạng', 'Ngoại mạng')) AS internal_check;
        END IF;

        OPEN cur;
        read_loop: LOOP
            FETCH cur INTO v_payment_id, v_service_id;
            IF done THEN
                LEAVE read_loop;
            END IF;

            IF v_remaining <= 0 THEN
                LEAVE read_loop;
            END IF;

            SELECT CONCAT('Đang xử lý payment_id: ', v_payment_id, ', service_id: ', v_service_id) AS processing_info;

            SET v_deduct = 0;

            -- === DULIEU ===
            IF p_type = 'DULIEU' THEN
                SELECT LEAST(free_data, v_remaining) INTO v_deduct
                FROM payment_detail
                WHERE payment_id = v_payment_id AND free_data > 0
                LIMIT 1;

                IF v_deduct > 0 THEN
                    UPDATE payment_detail
                    SET free_data = free_data - v_deduct
                    WHERE payment_id = v_payment_id;

                    SET v_remaining = v_remaining - v_deduct;

                    SELECT 'DULIEU' AS type_used, v_deduct AS deducted, v_remaining AS remaining;
                END IF;

            -- === CUOCGOI ===
            ELSEIF p_type = 'CUOCGOI' THEN
                IF v_is_internal THEN
                    SELECT LEAST(free_ON_call, v_remaining) INTO v_deduct
                    FROM payment_detail
                    WHERE payment_id = v_payment_id AND free_ON_call > 0
                    LIMIT 1;

                    IF v_deduct > 0 THEN
                        UPDATE payment_detail
                        SET free_ON_call = free_ON_call - v_deduct
                            -- free_ON_call = GREATEST(0, free_ON_call - v_deduct)
                        WHERE payment_id = v_payment_id;

                        SET v_remaining = v_remaining - v_deduct;
                        SELECT 'CUOCGOI (nội mạng)' AS type_used, v_deduct AS deducted, v_remaining AS remaining;
                    END IF;
                ELSE
                    SELECT LEAST(free_OffN_call, v_remaining) INTO v_deduct
                    FROM payment_detail
                    WHERE payment_id = v_payment_id AND free_OffN_call > 0
                    LIMIT 1;

                    IF v_deduct > 0 THEN
                        UPDATE payment_detail
                        SET free_OffN_call = free_OffN_call - v_deduct
                            -- free_OffN_call = GREATEST(0, free_OffN_call - v_deduct)
                        WHERE payment_id = v_payment_id;

                        SET v_remaining = v_remaining - v_deduct;
                        SELECT 'CUOCGOI (ngoại mạng)' AS type_used, v_deduct AS deducted, v_remaining AS remaining;
                    END IF;
                END IF;

            -- === TINNHAN ===
            ELSEIF p_type = 'TINNHAN' THEN
                IF v_is_internal THEN
                    SELECT 1 INTO v_deduct
                    FROM payment_detail
                    WHERE payment_id = v_payment_id AND free_ON_SMS > 0
                    LIMIT 1;

                    IF v_deduct > 0 THEN
                        UPDATE payment_detail
                        SET free_ON_SMS = free_ON_SMS - 1
                        WHERE payment_id = v_payment_id;

                        SET v_remaining = v_remaining - 1;
                        SELECT 'TINNHAN (nội mạng)' AS type_used, 1 AS deducted, v_remaining AS remaining;
                    END IF;
                ELSE
                    SELECT 1 INTO v_deduct
                    FROM payment_detail
                    WHERE payment_id = v_payment_id AND free_OffN_SMS > 0
                    LIMIT 1;

                    IF v_deduct > 0 THEN
                        UPDATE payment_detail
                        SET free_OffN_SMS = free_OffN_SMS - 1
                        WHERE payment_id = v_payment_id;

                        SET v_remaining = v_remaining - 1;
                        SELECT 'TINNHAN (ngoại mạng)' AS type_used, 1 AS deducted, v_remaining AS remaining;
                    END IF;
                END IF;
            END IF;
        END LOOP;
        CLOSE cur;

        UPDATE usage_logs
        SET usage_value = v_remaining
        WHERE id = p_usage_log_id;

        IF v_remaining > 0 THEN
            SELECT CONCAT('Không còn đủ ưu đãi. Đóng usage log ID: ', p_usage_log_id) AS log_closure;
            UPDATE usage_logs
            SET end_date = NOW()
            WHERE id = p_usage_log_id AND end_date IS NULL;
        ELSE
            SELECT 'Đã trừ hết ưu đãi thành công!' AS success;
        END IF;

    END proc_block;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_applied_voucher_promotions` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_applied_voucher_promotions`(
    IN p_plan_code VARCHAR(50),
    IN p_renewal_total INT
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_conandpromo TEXT;
    DECLARE v_free_data INT DEFAULT 0;
    DECLARE v_free_ON_SMS INT DEFAULT 0;
    DECLARE v_bonus_field VARCHAR(100);
    DECLARE v_bonus_value DECIMAL(10,2);
    DECLARE v_operator VARCHAR(5);

    DECLARE cur CURSOR FOR
        SELECT conandpromo
        FROM vouchers
        WHERE is_active = 1
          AND start_date <= CURDATE()
          AND end_date >= CURDATE();

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Giả lập kết quả ban đầu
    SET v_free_data = 0;
    SET v_free_ON_SMS = 0;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_conandpromo;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Kiểm tra điều kiện bằng JSON_EXTRACT
        IF JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.conditions[0].field')) = 'renewal_total'
           AND JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.conditions[0].value')) = p_renewal_total
           AND JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.conditions[1].field')) = 'code'
           AND JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.conditions[1].value')) = p_plan_code THEN

            -- Đọc action
            SET v_bonus_field = JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.field'));
            SET v_operator = JSON_UNQUOTE(JSON_EXTRACT(v_conandpromo, '$.promotion.operator'));
            SET v_bonus_value = JSON_EXTRACT(v_conandpromo, '$.promotion.value');

            -- Cộng giá trị vào trường phù hợp
            IF v_bonus_field = 'free_data' AND v_operator = '+=' THEN
                SET v_free_data = v_free_data + v_bonus_value;
            ELSEIF v_bonus_field = 'free_ON_SMS' AND v_operator = '+=' THEN
                SET v_free_ON_SMS = v_free_ON_SMS + v_bonus_value;
            END IF;
        END IF;
    END LOOP;
    CLOSE cur;

    -- Trả về kết quả
    SELECT 
        v_free_data AS bonus_free_data,
        v_free_ON_SMS AS bonus_free_ON_SMS;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_functions_by_rolegroup_id` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_functions_by_rolegroup_id`(

    IN p_rolegroup_id INT

)
BEGIN

    SELECT 

        f.id,

        f.function_name,

        f.syntax_name

    FROM rolegroupdetail rgd

    JOIN functions f ON rgd.function_id = f.id

    WHERE rgd.role_group_id = p_rolegroup_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_latest_promotions_by_service_group` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_latest_promotions_by_service_group`(IN p_subscriber_id INT)
BEGIN
    -- Nhóm A: service_id = 1
    SELECT 
    sb.cancel_at ,
        p.id AS plan_id,
        s.id AS service_id,
        sb.id AS subscription_id,
        sb.expiration_date,
        p.code,
        pay.id AS payment_id,
        pd.*
    FROM subscriptions sb
    JOIN plans p ON sb.plan_id = p.id
    JOIN services s ON p.service_id = s.id
    JOIN payments pay ON pay.subscription_id = sb.id
    JOIN payment_detail pd ON pd.payment_id = pay.id
    WHERE s.id = 2
      AND sb.subscriber_id = p_subscriber_id
      AND sb.expiration_date >= now()
    ORDER BY sb.activation_date DESC
    LIMIT 1;

    -- Nhóm B: service_id ≠ 1
    SELECT 
		sb.cancel_at ,
        p.id AS plan_id,
        s.id AS service_id,
        sb.id AS subscription_id,
        p.code,
        sb.expiration_date,
        pay.id AS payment_id,
        pd.*
    FROM subscriptions sb
    JOIN plans p ON sb.plan_id = p.id
    JOIN services s ON p.service_id = s.id
    JOIN payments pay ON pay.subscription_id = sb.id 
    JOIN payment_detail pd ON pd.payment_id = pay.id
    WHERE s.id <> 2
      AND sb.subscriber_id = p_subscriber_id
      AND sb.expiration_date >= now()
    ORDER BY sb.activation_date DESC
    LIMIT 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_plan_by_subscription_id` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_plan_by_subscription_id`(
    IN p_subscription_id INT
)
BEGIN
    SELECT 
        p.id AS plan_id,
        p.code AS plan_code,
        p.price,
        p.description,
        p.service_id,
        p.free_data,
        p.free_on_network_a_call,
        p.free_off_network_a_call,
        p.free_on_network_call,
        p.free_off_network_call,
        p.free_on_network_SMS,
        p.free_off_network_SMS,
        p.auto_renew,
        p.ON_a_call_cost,
        p.ON_SMS_cost
    FROM subscriptions s
    JOIN plans p ON s.plan_id = p.id
    WHERE s.id = p_subscription_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_staffs_not_in_role_group` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_staffs_not_in_role_group`(
    IN p_role_group_id INT
)
BEGIN
    SELECT s.id, s.full_name, s.email, s.phone, s.account_id
    FROM staffs s
    WHERE s.account_id IS NOT NULL
      AND s.account_id NOT IN (
          SELECT pd.account_id
          FROM permissiondetail pd
          WHERE pd.role_group_id = p_role_group_id
      );
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_user_info_with_roles` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_get_user_info_with_roles`(

    IN p_username VARCHAR(50),

    IN p_password VARCHAR(255)

)
BEGIN -- Nếu là nhân viên (staff)

IF EXISTS (

    SELECT 1

    FROM accounts a

        JOIN staffs s ON s.account_id = a.id

    WHERE a.username = p_username

        AND a.password = p_password

        AND a.is_active = 1

) THEN

SELECT a.id AS account_id,

    s.id as staff_id,

    a.username,

    s.full_name,

    s.card_id,

    s.phone,

    s.email,

    s.gender,

    s.birthday,

    rg.id AS role_id,

    rg.role_name

FROM accounts a

    JOIN staffs s ON s.account_id = a.id

    LEFT JOIN permissiondetail pd ON pd.account_id = a.id

    LEFT JOIN rolegroup rg ON rg.id = pd.role_group_id

WHERE a.username = p_username

    AND a.password = p_password

    AND a.is_active = 1;

-- Nếu không phải nhân viên → kiểm tra subscriber

ELSEIF EXISTS (

    SELECT 1

    FROM accounts a

        JOIN subscribers sub ON sub.account_id = a.id

    WHERE a.username = p_username

        AND a.password = p_password

        AND a.is_active = 1

) THEN

SELECT a.id AS account_id,

    a.username,

    c.full_name AS full_name,

    c.card_id AS card_id,

    sub.phone_number AS phone,

    sub.id as subscriber_id,

    NULL AS email,

    NULL AS gender,

    NULL AS birthday,

    rg.id AS role_id,
    sub.subscriber,

    rg.role_name

FROM accounts a

    JOIN subscribers sub ON sub.account_id = a.id

    LEFT JOIN customers c ON c.id = sub.customer_id

    LEFT JOIN permissiondetail pd ON pd.account_id = a.id

    LEFT JOIN rolegroup rg ON rg.id = pd.role_group_id

WHERE a.username = p_username

    AND a.password = p_password

    AND a.is_active = 1;

ELSE -- Không tìm thấy

SELECT 'Invalid username or password' AS message;

END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_remove_permission_detail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_remove_permission_detail`(
    IN p_role_group_id INT,
    IN p_account_id INT
)
BEGIN
    DELETE FROM permissiondetail
    WHERE role_group_id = p_role_group_id AND account_id = p_account_id;

    IF ROW_COUNT() > 0 THEN
        SELECT TRUE AS success, 'Xóa nhân viên khỏi nhóm quyền thành công' AS message;
    ELSE
        SELECT FALSE AS error, 'Không tìm thấy bản ghi để xóa' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_revenue_report_by_date_range` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_revenue_report_by_date_range`(
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_plan_code VARCHAR(50),
    IN p_service_id INT
)
BEGIN
    SELECT 
        DATE(p.payment_date) AS payment_day,
        COUNT(p.id) AS total_payments,
        SUM(p.total_amount) AS total_revenue,
        COUNT(DISTINCT s.subscriber_id) AS unique_subscribers,
        pl.code AS plan_code,
        pl.service_id AS service_id
    FROM payments p
    JOIN subscriptions s ON p.subscription_id = s.id
    JOIN plans pl ON s.plan_id = pl.id
    WHERE p.payment_date BETWEEN p_start_date AND p_end_date
      AND p.is_paid = 1
      AND (p_plan_code IS NULL OR pl.code = p_plan_code)
      AND (p_service_id IS NULL OR pl.service_id = p_service_id)
    GROUP BY DATE(p.payment_date), pl.code, pl.service_id
    ORDER BY payment_day ASC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_role_group_detail_add_multiple` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_role_group_detail_add_multiple`(
    IN p_role_group_id INT,
    IN p_function_ids JSON
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE num_functions INT;
    DECLARE v_success BOOLEAN DEFAULT TRUE;
    DECLARE v_message VARCHAR(255);
    DECLARE v_add_success BOOLEAN;
    DECLARE v_add_message VARCHAR(255);
    
    -- Bắt đầu giao dịch
    START TRANSACTION;
    
    -- Lấy số lượng các chức năng cần thêm từ JSON
    SET num_functions = JSON_LENGTH(p_function_ids);
    
    -- Nhãn cho vòng lặp
    loop_start: 
    -- Lặp qua các chức năng và gọi lại AddRoleGroupDetail để thêm vào bảng
    WHILE i < num_functions AND v_success DO
        -- Lấy ID của chức năng tại chỉ số i từ JSON
        SET @function_id = JSON_UNQUOTE(JSON_EXTRACT(p_function_ids, CONCAT('$[', i, ']')));

        -- Gọi lại hàm AddRoleGroupDetail để thêm chức năng vào và nhận kết quả OUT
        CALL AddRoleGroupDetail(p_role_group_id, @function_id, @v_add_success, @v_add_message);

        -- Kiểm tra kết quả trả về từ AddRoleGroupDetail qua OUT parameters
        IF @v_add_success = FALSE THEN
            -- Nếu không thành công, rollback và thoát
            ROLLBACK;
            SET v_success = FALSE;
            SET v_message = @v_add_message;
            SELECT FALSE AS error, v_message AS message;
            LEAVE loop_start; -- Thoát khỏi vòng lặp
        END IF;
        
        -- Tiến hành bước tiếp theo nếu thành công
        SET i = i + 1;
    END WHILE;
    
    -- Kiểm tra thành công hay không
    IF v_success THEN
        COMMIT;
        SET v_message = 'Thêm tất cả role group detail thành công';
        SELECT TRUE AS success, v_message AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_staff_update_contact` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_staff_update_contact`(
    IN p_id INT,
    IN p_email VARCHAR(255),
    IN p_phone VARCHAR(20)
)
BEGIN
    -- Kiểm tra trùng email
    IF EXISTS (
        SELECT 1 FROM staffs 
        WHERE email = p_email AND id != p_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Email đã được sử dụng bởi nhân viên khác';
    END IF;

    -- Kiểm tra trùng số điện thoại
    IF EXISTS (
        SELECT 1 FROM staffs 
        WHERE phone = p_phone AND id != p_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Số điện thoại đã được sử dụng bởi nhân viên khác';
    END IF;

    -- Nếu không có trùng, thực hiện cập nhật
    UPDATE staffs
    SET 
        email = p_email,
        phone = p_phone
    WHERE id = p_id;

    -- Trả về kết quả thành công
    SELECT 1 AS success, 'Cập nhật thành công' AS message;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_subscriber_get_by_account_id` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_subscriber_get_by_account_id`(
    IN p_account_id INT
)
BEGIN
    SELECT 
        s.id AS subscriber_id,
        s.phone_number,
        s.main_balance,
        s.activation_date,
        s.expiration_date,
        s.is_active,
        s.subscriber,
        s.account_id,
        c.full_name AS customer_name
    FROM subscribers s
    LEFT JOIN customers c ON s.customer_id = c.id
    WHERE s.account_id = p_account_id
    LIMIT 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_warn_and_lock_accounts` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_warn_and_lock_accounts`()
BEGIN

    DECLARE done INT DEFAULT FALSE;

    DECLARE v_subscriber_id INT;

    DECLARE v_account_id INT;

    DECLARE v_phone VARCHAR(20);



    DECLARE cur CURSOR FOR

        SELECT s.id, a.id, s.phone_number

        FROM subscribers s

        JOIN subscriptions sub ON sub.subscriber_id = s.id

        JOIN payments p ON sub.id = p.subscription_id

        JOIN accounts a ON a.id = s.account_id

        WHERE s.warning_date IS NULL

          AND p.is_paid = FALSE

          AND DATE_ADD(p.due_date, INTERVAL 10 DAY) <= NOW();



    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;



    START TRANSACTION;



    OPEN cur;



    read_loop: LOOP

        FETCH cur INTO v_subscriber_id, v_account_id, v_phone;

        IF done THEN

            LEAVE read_loop;

        END IF;



        -- Cập nhật trạng thái

        UPDATE subscribers SET warning_date = NOW(), is_active = FALSE WHERE id = v_subscriber_id;

        UPDATE accounts SET is_active = FALSE WHERE id = v_account_id;



        -- Ghi log cảnh báo

        INSERT INTO usage_logs (

            type, usage_value, subscriber_id, start_date, end_date, `by_from`, `to`, contents

        ) VALUES (

            'TINNHAN', 1, v_subscriber_id,

            NOW(), NOW(), '191', v_phone,

            CONCAT('Thuê bao ', v_phone, ' bị khóa tài khoản do chậm thanh toán quá 10 ngày.')

        );

    END LOOP;



    CLOSE cur;



    COMMIT;



    SELECT TRUE AS success, 'Đã cập nhật trạng thái và ghi log cảnh báo thành công.' AS message;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateAccount` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateAccount`(
    IN p_account_id INT,
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi: Không thể cập nhật tài khoản' AS message;
    END;

    START TRANSACTION;

    UPDATE accounts
    SET username = p_username, passwork = p_password
    WHERE id = p_account_id;

    -- Kiểm tra số dòng bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy tài khoản để cập nhật' AS message;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Cập nhật tài khoản thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateContract` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateContract`(
    IN p_contract_id INT,
    IN p_is_active BIT
    -- IN p_title VARCHAR(255),
  --   IN p_contents TEXT,
  --   IN p_start_date DATE,
   --  IN p_end_date DATE
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi: Không thể cập nhật hợp đồng' AS message;
    END;

    START TRANSACTION;

    UPDATE contracts
    SET is_active = p_is_active,
        -- contents = p_contents,
        -- start_date = p_start_date,
		end_date = now()
    WHERE id = p_contract_id;

    -- Kiểm tra số dòng bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy hợp đồng để cập nhật' AS message;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Cập nhật hợp đồng thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateCustomer` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateCustomer`(
    IN p_customer_id INT,
    IN p_full_name VARCHAR(255),
    IN p_is_active BOOLEAN,
    IN p_card_id VARCHAR(12)
)
BEGIN
    START TRANSACTION;

    UPDATE customers
    SET 
        full_name = p_full_name,
        is_active = p_is_active,
        card_id = p_card_id
    WHERE id = p_customer_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy customer để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa customer thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateFunction` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateFunction`(
    IN p_function_id INT,
    IN p_function_name VARCHAR(255),
    IN p_syntax_name VARCHAR(255)
)
BEGIN
    START TRANSACTION;

    UPDATE functions
    SET 
        function_name = p_function_name,
        syntax_name = p_syntax_name
    WHERE id = p_function_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy function để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa function thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateNetwork` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateNetwork`(
    IN p_id INT,
    IN p_display_name VARCHAR(100),
    IN p_country_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE networks
    SET 
        display_name = p_display_name,
        country_id = p_country_id
    WHERE id = p_id;

    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS success, 'Không thể cập nhật mạng (ID không tồn tại hoặc không thay đổi gì)' AS message;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Cập nhật mạng thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdatePlan` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdatePlan`(
    IN p_plan_id INT,
    IN p_code VARCHAR(50),
    IN p_price FLOAT,
    IN p_description TEXT,
    IN p_service_id INT,
    IN p_is_active BIT,
    IN p_renewal_syntax VARCHAR(255),
    IN p_registration_syntax VARCHAR(255),
    IN p_cancel_syntax VARCHAR(255),
    IN p_free_data INT,
    IN p_free_on_network_a_call INT,
    IN p_free_on_network_call INT,
    IN p_free_on_network_SMS INT,
    IN p_free_off_network_a_call INT,
    IN p_free_off_network_call INT,
    IN p_free_off_network_SMS INT,
    IN p_auto_renew BIT,
    IN p_staff_id INT,
    IN p_maximum_on_network_call INT,
    IN p_ON_SMS_cost FLOAT,
    IN p_ON_a_call_cost FLOAT,
    IN p_object_type VARCHAR(50),
    IN p_duration INT
)
BEGIN
    DECLARE v_current_code VARCHAR(50);
    DECLARE v_current_registration_syntax VARCHAR(255);
    DECLARE v_current_renewal_syntax VARCHAR(255);
    DECLARE v_current_cancel_syntax VARCHAR(255);

    -- Tạo bảng tạm để debug
    CREATE TEMPORARY TABLE IF NOT EXISTS debug_log (
        log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        message TEXT
    );

    -- Bắt đầu giao dịch
    START TRANSACTION;

    -- Kiểm tra plan_id tồn tại
    IF NOT EXISTS (SELECT 1 FROM plans WHERE id = p_plan_id) THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('Gói cước không tồn tại: ', p_plan_id));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Gói cước không tồn tại';
    END IF;

    -- Kiểm tra dữ liệu đầu vào
    IF p_code IS NULL OR TRIM(p_code) = '' THEN
        INSERT INTO debug_log (message) VALUES ('Mã gói cước rỗng');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã gói cước là bắt buộc';
    END IF;

    IF p_price IS NULL OR p_price <= 0 THEN
        INSERT INTO debug_log (message) VALUES ('Giá không hợp lệ');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Giá gói cước phải là số dương';
    END IF;

    IF p_service_id IS NULL THEN
        INSERT INTO debug_log (message) VALUES ('ID Dịch vụ rỗng');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ID Dịch vụ là bắt buộc';
    END IF;

    IF p_object_type NOT IN ('TRATRUOC', 'TRASAU') THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('Hình thức thanh toán không hợp lệ: ', p_object_type));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Hình thức thanh toán phải là TRATRUOC hoặc TRASAU';
    END IF;

    IF p_duration IS NULL OR p_duration <= 0 THEN
        INSERT INTO debug_log (message) VALUES ('Thời hạn không hợp lệ');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Thời hạn phải là số dương';
    END IF;

    -- Lấy giá trị hiện tại để so sánh
    SELECT code, registration_syntax, renewal_syntax, cancel_syntax
    INTO v_current_code, v_current_registration_syntax, v_current_renewal_syntax, v_current_cancel_syntax
    FROM plans
    WHERE id = p_plan_id;

    -- Chuẩn hóa và kiểm tra mã code trùng lặp
    SET p_code = TRIM(p_code);
    IF LOWER(p_code) != LOWER(v_current_code) AND EXISTS (
        SELECT 1 FROM plans WHERE LOWER(code) = LOWER(p_code) AND id != p_plan_id
    ) THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('Mã gói cước trùng: ', p_code));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mã gói cước đã tồn tại';
    END IF;

    -- Chuẩn hóa và kiểm tra registration_syntax trùng lặp
    IF p_registration_syntax IS NOT NULL AND LOWER(p_registration_syntax) != LOWER(v_current_registration_syntax) THEN
        SET p_registration_syntax = TRIM(p_registration_syntax);
        IF EXISTS (SELECT 1 FROM plans WHERE LOWER(registration_syntax) = LOWER(p_registration_syntax) AND id != p_plan_id) THEN
            INSERT INTO debug_log (message) VALUES (CONCAT('Cú pháp đăng ký trùng: ', p_registration_syntax));
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cú pháp đăng ký đã tồn tại';
        END IF;
    END IF;

    -- Chuẩn hóa và kiểm tra renewal_syntax trùng lặp
    IF p_renewal_syntax IS NOT NULL AND LOWER(p_renewal_syntax) != LOWER(v_current_renewal_syntax) THEN
        SET p_renewal_syntax = TRIM(p_renewal_syntax);
        IF EXISTS (SELECT 1 FROM plans WHERE LOWER(renewal_syntax) = LOWER(p_renewal_syntax) AND id != p_plan_id) THEN
            INSERT INTO debug_log (message) VALUES (CONCAT('Cú pháp gia hạn trùng: ', p_renewal_syntax));
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cú pháp gia hạn đã tồn tại';
        END IF;
    END IF;

    -- Chuẩn hóa và kiểm tra cancel_syntax trùng lặp
    IF p_cancel_syntax IS NOT NULL AND LOWER(p_cancel_syntax) != LOWER(v_current_cancel_syntax) THEN
        SET p_cancel_syntax = TRIM(p_cancel_syntax);
        IF EXISTS (SELECT 1 FROM plans WHERE LOWER(cancel_syntax) = LOWER(p_cancel_syntax) AND id != p_plan_id) THEN
            INSERT INTO debug_log (message) VALUES (CONCAT('Cú pháp hủy trùng: ', p_cancel_syntax));
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cú pháp hủy đã tồn tại';
        END IF;
    END IF;

    -- Kiểm tra service_id tồn tại
    IF NOT EXISTS (SELECT 1 FROM services WHERE id = p_service_id) THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('ID Dịch vụ không tồn tại: ', p_service_id));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ID Dịch vụ không tồn tại';
    END IF;

    -- Kiểm tra staff_id tồn tại (nếu không null)
    IF p_staff_id IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM staffs WHERE id = p_staff_id
    ) THEN
        INSERT INTO debug_log (message) VALUES (CONCAT('ID Nhân viên không tồn tại: ', p_staff_id));
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ID Nhân viên không tồn tại';
    END IF;

    -- Cập nhật bảng plans
    UPDATE plans
    SET 
        code = p_code,
        price = p_price,
        description = p_description,
        service_id = p_service_id,
        is_active = p_is_active,
        renewal_syntax = p_renewal_syntax,
        registration_syntax = p_registration_syntax,
        cancel_syntax = p_cancel_syntax,
        free_data = p_free_data,
        free_on_network_a_call = p_free_on_network_a_call,
        free_on_network_call = p_free_on_network_call,
        free_on_network_SMS = p_free_on_network_SMS,
        free_off_network_a_call = p_free_off_network_a_call,
        free_off_network_call = p_free_off_network_call,
        free_off_network_SMS = p_free_off_network_SMS,
        auto_renew = p_auto_renew,
        staff_id = p_staff_id,
        maximum_on_network_call = p_maximum_on_network_call,
        ON_SMS_cost = p_ON_SMS_cost,
        ON_a_call_cost = p_ON_a_call_cost,
        updated_at = NOW()
    WHERE id = p_plan_id;

    -- Cập nhật hoặc chèn vào plan_detail
    IF EXISTS (SELECT 1 FROM plan_detail WHERE plan_id = p_plan_id) THEN
        UPDATE plan_detail
        SET 
            object_type = p_object_type,
            duration = p_duration
        WHERE plan_id = p_plan_id;
    ELSE
        INSERT INTO plan_detail (plan_id, object_type, duration)
        VALUES (p_plan_id, p_object_type, p_duration);
    END IF;

    COMMIT;

    -- Xóa bảng debug
    DROP TEMPORARY TABLE IF EXISTS debug_log;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdatePlanDetail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdatePlanDetail`(
    IN p_plan_detail_id INT,
    IN p_plan_id INT,
    IN p_object_type VARCHAR(50),
    IN p_duration INT
)
BEGIN
    START TRANSACTION;

    UPDATE plan_detail
    SET 
        plan_id = p_plan_id,
        object_type = p_object_type,
        duration = p_duration
    WHERE id = p_plan_detail_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy plan detail để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa plan detail thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdatePlanNetwork` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdatePlanNetwork`(
    IN p_plan_network_id INT,
    IN p_network_id INT,
    IN p_plan_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE plan_network
    SET 
        network_id = p_network_id,
        plan_id = p_plan_id
    WHERE id = p_plan_network_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy plan network để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa plan network thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateRoleGroup` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateRoleGroup`(
    IN p_role_group_id INT,
    IN p_role_name VARCHAR(100)
)
BEGIN
    START TRANSACTION;

    UPDATE rolegroup
    SET 
        role_name = p_role_name
    WHERE id = p_role_group_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy role group để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa role group thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateRoleGroupDetail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateRoleGroupDetail`(
    IN p_role_group_id INT,
    IN p_function_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE rolegroupdetail
    SET 
        function_id = p_function_id
    WHERE role_group_id = p_role_group_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy role group detail để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa role group detail thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateService` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateService`(
    IN p_service_id INT,
    IN p_parent_id INT,
    IN p_coverage_area INT
)
BEGIN
    START TRANSACTION;

    UPDATE services
    SET 
        parent_id = p_parent_id,
        coverage_area = p_coverage_area
    WHERE id = p_service_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT TRUE AS error, 'Không tìm thấy service để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa service thành công' AS message;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateStaff` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateStaff`(
    IN p_staff_id INT,
    IN p_full_name VARCHAR(100),
    IN p_phone VARCHAR(15),
    IN p_email VARCHAR(100),
    IN p_gender ENUM('Nam', 'Nữ', 'Khác'),
    IN p_birthday DATE,
    IN p_role_name VARCHAR(50),
    IN p_password VARCHAR(255)
)
BEGIN
    proc_end: BEGIN
        DECLARE v_account_id INT;
        DECLARE v_role_group_id INT;
        DECLARE v_count_email INT;
        DECLARE v_count_phone INT;
        DECLARE v_error_message TEXT DEFAULT NULL;

        -- Bắt lỗi và rollback khi có exception
        DECLARE EXIT HANDLER FOR SQLEXCEPTION
        BEGIN
            ROLLBACK;
            SELECT 'Đã xảy ra lỗi trong quá trình cập nhật' AS error;
        END;

        START TRANSACTION;

        -- Lấy account_id từ bảng staffs
        SELECT account_id INTO v_account_id
        FROM staffs
        WHERE id = p_staff_id;

        IF v_account_id IS NULL THEN
            SET v_error_message = 'Không tìm thấy tài khoản của nhân viên này';
            ROLLBACK;
            SELECT v_error_message AS error;
            LEAVE proc_end;
        END IF;

        -- Kiểm tra trùng email (ngoại trừ bản ghi hiện tại)
        SELECT COUNT(*) INTO v_count_email
        FROM staffs
        WHERE email = p_email AND id != p_staff_id;

        IF v_count_email > 0 THEN
            SET v_error_message = 'Email đã tồn tại trong hệ thống';
            ROLLBACK;
            SELECT v_error_message AS error;
            LEAVE proc_end;
        END IF;

        -- Kiểm tra trùng số điện thoại (ngoại trừ bản ghi hiện tại)
        SELECT COUNT(*) INTO v_count_phone
        FROM staffs
        WHERE phone = p_phone AND id != p_staff_id;

        IF v_count_phone > 0 THEN
            SET v_error_message = 'Số điện thoại đã tồn tại trong hệ thống';
            ROLLBACK;
            SELECT v_error_message AS error;
            LEAVE proc_end;
        END IF;

        -- Cập nhật bảng staffs
        UPDATE staffs
        SET
            full_name = p_full_name,
            phone = p_phone,
            email = p_email,
            gender = p_gender,
            birthday = p_birthday
        WHERE id = p_staff_id;

        -- Cập nhật mật khẩu nếu có truyền vào
        IF p_password IS NOT NULL AND LENGTH(TRIM(p_password)) > 0 THEN
            UPDATE accounts
            SET password = p_password
            WHERE id = v_account_id;
        END IF;

        -- Xác định role_group_id
        IF p_role_name = 'Quản lý' THEN
            SET v_role_group_id = 1;
        ELSEIF p_role_name = 'Nhân viên' THEN
            SET v_role_group_id = 2;
        ELSE
            SET v_error_message = 'Vai trò không hợp lệ';
            ROLLBACK;
            SELECT v_error_message AS error;
            LEAVE proc_end;
        END IF;

        -- Xóa quyền cũ, thêm quyền mới
        DELETE FROM permissiondetail
        WHERE account_id = v_account_id;

        INSERT INTO permissiondetail (account_id, role_group_id)
        VALUES (v_account_id, v_role_group_id);

        COMMIT;

        -- Trả kết quả thành công
        SELECT NULL AS error;

    END proc_end;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateSubscriber` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateSubscriber`(
    IN p_id INT,
    IN p_phone_number VARCHAR(15),
    IN p_main_balance DECIMAL(10,2),
    IN p_expiration_date DATE,
    IN p_is_active BOOLEAN,
    IN p_warning_date DATE,
    IN p_subscriber VARCHAR(20),
    IN p_customer_id INT,
    IN p_account_id INT,
    IN p_ON_a_call_cost DECIMAL(10,2),
    IN p_ON_SMS_cost DECIMAL(10,2)
)
BEGIN
    DECLARE v_old_is_active BOOLEAN;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi trong quá trình cập nhật thuê bao' AS message;
    END;

    START TRANSACTION;

    -- Lấy trạng thái cũ của thuê bao
    SELECT is_active INTO v_old_is_active
    FROM subscribers
    WHERE id = p_id;

    -- Cập nhật thuê bao
    UPDATE subscribers
    SET
        phone_number = p_phone_number,
        main_balance = p_main_balance,
        expiration_date = p_expiration_date,
        is_active = p_is_active,
        warning_date = p_warning_date,
        subscriber = p_subscriber,
        customer_id = p_customer_id,
        account_id = p_account_id,
        ON_a_call_cost = p_ON_a_call_cost,
        ON_SMS_cost = p_ON_SMS_cost
    WHERE id = p_id;

    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS success, 'Không tìm thấy thuê bao hoặc không có gì thay đổi' AS message;
    ELSE
        -- Nếu trạng thái is_active thay đổi thì cập nhật account
        IF v_old_is_active <> p_is_active THEN
            UPDATE accounts
            SET is_active = p_is_active
            WHERE id = p_account_id;
        END IF;

        COMMIT;
        SELECT TRUE AS success, 'Cập nhật thuê bao thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateSubscription` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateSubscription`(
    IN p_id INT,
    IN p_created_at DATETIME,
    IN p_expiration_date DATETIME,
    IN p_renewal_total INT,
    IN p_is_renewal BOOLEAN,
    IN p_cancel_at DATETIME,
    IN p_activation_date DATETIME
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi trong quá trình cập nhật subscription' AS message;
    END;

    START TRANSACTION;

    UPDATE subscriptions
    SET 
        created_at = p_created_at,
        expiration_date = p_expiration_date,
        renewal_total = p_renewal_total,
        is_renewal = p_is_renewal,
        cancel_at = p_cancel_at,
        activation_date = p_activation_date
    WHERE id = p_id;

    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS success, 'Không tìm thấy hoặc không cập nhật subscription' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Cập nhật subscription thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateSubscriptionStatus` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateSubscriptionStatus`(
    IN p_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi trong quá trình cập nhật subscription' AS message;
    END;

    START TRANSACTION;

    UPDATE subscriptions
    SET 
        expiration_date = NOW(),
        cancel_at = NOW(),
        is_renewal = FALSE
    WHERE id = p_id;

    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS success, 'Không tìm thấy hoặc không cập nhật subscription' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Cập nhật subscription thành công' AS message;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateVoucher` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateVoucher`(
    IN p_voucher_id INT,
    IN p_code VARCHAR(50),
    IN p_description TEXT,
    IN p_conandpromo TEXT,
    IN p_start_date DATETIME,
    IN p_end_date DATETIME,
    IN p_is_active BOOLEAN,
    IN p_packages VARCHAR(255)
)
BEGIN
    DECLARE v_code VARCHAR(50);
    DECLARE v_description TEXT;
    DECLARE v_conandpromo TEXT;
    DECLARE v_start_date DATETIME;
    DECLARE v_end_date DATETIME;
    DECLARE v_is_active BOOLEAN;
    DECLARE v_packages VARCHAR(255);

    -- Lấy dữ liệu hiện tại của voucher
    SELECT code, description, conandpromo, start_date, end_date, is_active, packages
    INTO v_code, v_description, v_conandpromo, v_start_date, v_end_date, v_is_active, v_packages
    FROM vouchers
    WHERE id = p_voucher_id;

    -- So sánh toàn bộ dữ liệu
    IF v_code = p_code AND
       v_description <=> p_description AND
       v_conandpromo <=> p_conandpromo AND
       v_start_date <=> p_start_date AND
       v_end_date <=> p_end_date AND
       v_is_active = p_is_active AND
       v_packages <=> p_packages THEN

        -- Dữ liệu giống hệt, không cập nhật
        SELECT FALSE AS error, 'Không có gì để thay đổi' AS message;

    ELSE
        -- Thực hiện cập nhật nếu có sự thay đổi
        START TRANSACTION;

        UPDATE vouchers
        SET 
            code = p_code,
            description = p_description,
            conandpromo = p_conandpromo,
            start_date = p_start_date,
            end_date = p_end_date,
            is_active = p_is_active,
            packages = p_packages
        WHERE id = p_voucher_id;

        IF ROW_COUNT() = 0 THEN
            ROLLBACK;
            SELECT FALSE AS error, 'Không sửa thành công' AS message;
        ELSE
            COMMIT;
            SELECT TRUE AS success, 'Sửa voucher thành công' AS message;
        END IF;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `v_accounts`
--

/*!50001 DROP VIEW IF EXISTS `v_accounts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_accounts` AS select `accounts`.`id` AS `id`,`accounts`.`username` AS `username`,`accounts`.`password` AS `password`,`accounts`.`is_active` AS `is_active` from `accounts` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_contracts`
--

/*!50001 DROP VIEW IF EXISTS `v_contracts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_contracts` AS select `contracts`.`id` AS `id`,`contracts`.`title` AS `title`,`contracts`.`contents` AS `contents`,`contracts`.`start_date` AS `start_date`,`contracts`.`end_date` AS `end_date`,`contracts`.`is_active` AS `is_active`,`contracts`.`subscriber_id` AS `subscriber_id`,`contracts`.`created_at` AS `created_at` from `contracts` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_countries`
--

/*!50001 DROP VIEW IF EXISTS `v_countries`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_countries` AS select `countries`.`id` AS `id`,`countries`.`country_name` AS `country_name` from `countries` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_customers`
--

/*!50001 DROP VIEW IF EXISTS `v_customers`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_customers` AS select `customers`.`id` AS `id`,`customers`.`full_name` AS `full_name`,`customers`.`is_active` AS `is_active`,`customers`.`card_id` AS `card_id` from `customers` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_functions`
--

/*!50001 DROP VIEW IF EXISTS `v_functions`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_functions` AS select `functions`.`id` AS `id`,`functions`.`function_name` AS `function_name`,`functions`.`syntax_name` AS `syntax_name` from `functions` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_networks`
--

/*!50001 DROP VIEW IF EXISTS `v_networks`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_networks` AS select `networks`.`id` AS `id`,`networks`.`network_name` AS `network_name`,`networks`.`display_name` AS `display_name`,`networks`.`country_id` AS `country_id` from `networks` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_payment_details`
--

/*!50001 DROP VIEW IF EXISTS `v_payment_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_payment_details` AS select `payment_detail`.`id` AS `id`,`payment_detail`.`payment_id` AS `payment_id`,`payment_detail`.`free_data` AS `free_data`,`payment_detail`.`free_ON_a_call` AS `free_on_a_call`,`payment_detail`.`free_OffN_a_call` AS `free_offn_a_call`,`payment_detail`.`free_ON_call` AS `free_on_call`,`payment_detail`.`free_OffN_call` AS `free_offn_call`,`payment_detail`.`free_ON_SMS` AS `free_on_sms`,`payment_detail`.`free_OffN_SMS` AS `free_offn_sms`,`payment_detail`.`ON_a_call_cost` AS `on_a_call_cost`,`payment_detail`.`ON_SMS_cost` AS `on_sms_cost` from `payment_detail` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_payments`
--

/*!50001 DROP VIEW IF EXISTS `v_payments`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_payments` AS select `payments`.`id` AS `id`,`payments`.`subscription_id` AS `subscription_id`,`payments`.`payment_date` AS `payment_date`,`payments`.`total_amount` AS `total_amount`,`payments`.`payment_method` AS `payment_method`,`payments`.`is_paid` AS `is_paid`,`payments`.`due_date` AS `due_date` from `payments` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_permission_details`
--

/*!50001 DROP VIEW IF EXISTS `v_permission_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_permission_details` AS select `permissiondetail`.`role_group_id` AS `role_group_id`,`permissiondetail`.`account_id` AS `account_id` from `permissiondetail` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_plan_details`
--

/*!50001 DROP VIEW IF EXISTS `v_plan_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_plan_details` AS select `plan_detail`.`plan_id` AS `plan_id`,`plan_detail`.`object_type` AS `object_type`,`plan_detail`.`duration` AS `duration` from `plan_detail` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_plan_networks`
--

/*!50001 DROP VIEW IF EXISTS `v_plan_networks`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_plan_networks` AS select `plan_network`.`id` AS `id`,`plan_network`.`network_id` AS `network_id`,`plan_network`.`plan_id` AS `plan_id` from `plan_network` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_plans`
--

/*!50001 DROP VIEW IF EXISTS `v_plans`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_plans` AS select `plans`.`id` AS `id`,`plans`.`code` AS `code`,`plans`.`price` AS `price`,`plans`.`description` AS `description`,`plans`.`service_id` AS `service_id`,`plans`.`is_active` AS `is_active`,`plans`.`renewal_syntax` AS `renewal_syntax`,`plans`.`registration_syntax` AS `registration_syntax`,`plans`.`cancel_syntax` AS `cancel_syntax`,`plans`.`free_data` AS `free_data`,`plans`.`free_on_network_a_call` AS `free_on_network_a_call`,`plans`.`free_on_network_call` AS `free_on_network_call`,`plans`.`free_on_network_SMS` AS `free_on_network_SMS`,`plans`.`free_off_network_a_call` AS `free_off_network_a_call`,`plans`.`free_off_network_call` AS `free_off_network_call`,`plans`.`free_off_network_SMS` AS `free_off_network_SMS`,`plans`.`auto_renew` AS `auto_renew`,`plans`.`staff_id` AS `staff_id`,`plans`.`created_at` AS `created_at`,`plans`.`updated_at` AS `updated_at` from `plans` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_role_group_details`
--

/*!50001 DROP VIEW IF EXISTS `v_role_group_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_role_group_details` AS select `rolegroupdetail`.`role_group_id` AS `role_group_id`,`rolegroupdetail`.`function_id` AS `function_id` from `rolegroupdetail` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_role_groups`
--

/*!50001 DROP VIEW IF EXISTS `v_role_groups`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_role_groups` AS select `rolegroup`.`id` AS `id`,`rolegroup`.`role_name` AS `role_name` from `rolegroup` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_services`
--

/*!50001 DROP VIEW IF EXISTS `v_services`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_services` AS select `services`.`id` AS `id`,`services`.`service_name` AS `service_name`,`services`.`parent_id` AS `parent_id`,`services`.`coverage_area` AS `coverage_area` from `services` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_staffs`
--

/*!50001 DROP VIEW IF EXISTS `v_staffs`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_staffs` AS select `staffs`.`id` AS `id`,`staffs`.`full_name` AS `full_name`,`staffs`.`card_id` AS `card_id`,`staffs`.`phone` AS `phone`,`staffs`.`email` AS `email`,`staffs`.`is_active` AS `is_active`,`staffs`.`gender` AS `gender`,`staffs`.`birthday` AS `birthday`,`staffs`.`account_id` AS `account_id` from `staffs` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_subscribers`
--

/*!50001 DROP VIEW IF EXISTS `v_subscribers`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_subscribers` AS select `subscribers`.`id` AS `id`,`subscribers`.`phone_number` AS `phone_number`,`subscribers`.`main_balance` AS `main_balance`,`subscribers`.`activation_date` AS `activation_date`,`subscribers`.`expiration_date` AS `expiration_date`,`subscribers`.`is_active` AS `is_active`,`subscribers`.`customer_id` AS `customer_id`,`subscribers`.`warning_date` AS `warning_date`,`subscribers`.`account_id` AS `account_id`,`subscribers`.`subscriber` AS `subscriber`,`subscribers`.`ON_a_call_cost` AS `ON_a_call_cost`,`subscribers`.`ON_SMS_cost` AS `ON_SMS_cost` from `subscribers` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_subscriptions`
--

/*!50001 DROP VIEW IF EXISTS `v_subscriptions`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_subscriptions` AS select `subscriptions`.`id` AS `id`,`subscriptions`.`plan_id` AS `plan_id`,`subscriptions`.`subscriber_id` AS `subscriber_id`,`subscriptions`.`created_at` AS `created_at`,`subscriptions`.`expiration_date` AS `expiration_date`,`subscriptions`.`renewal_total` AS `renewal_total`,`subscriptions`.`is_renewal` AS `is_renewal`,`subscriptions`.`cancel_at` AS `cancel_at`,`subscriptions`.`activation_date` AS `activation_date` from `subscriptions` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_usage_logs`
--

/*!50001 DROP VIEW IF EXISTS `v_usage_logs`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_usage_logs` AS select `usage_logs`.`id` AS `id`,`usage_logs`.`type` AS `type`,`usage_logs`.`usage_value` AS `usage_value`,`usage_logs`.`subscriber_id` AS `subscriber_id`,`usage_logs`.`start_date` AS `start_date`,`usage_logs`.`end_date` AS `end_date`,`usage_logs`.`by_from` AS `by_from`,`usage_logs`.`to` AS `to`,`usage_logs`.`contents` AS `contents` from `usage_logs` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_vouchers`
--

/*!50001 DROP VIEW IF EXISTS `v_vouchers`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_vouchers` AS select `vouchers`.`id` AS `id`,`vouchers`.`code` AS `code`,`vouchers`.`description` AS `description`,`vouchers`.`conandpromo` AS `conandpromo`,`vouchers`.`start_date` AS `start_date`,`vouchers`.`end_date` AS `end_date`,`vouchers`.`usage_limit` AS `usage_limit`,`vouchers`.`remaining_count` AS `remaining_count`,`vouchers`.`is_active` AS `is_active`,`vouchers`.`staff_id` AS `staff_id`,`vouchers`.`packages` AS `packages` from `vouchers` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-16 14:40:23
