use mobileservice_n7;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddCustomer`(
    IN p_full_name VARCHAR(255),
    IN p_is_active BOOLEAN,
    IN p_account_id INT,
    IN p_card_id VARCHAR(20)
)
BEGIN
    START TRANSACTION;

    INSERT INTO customers (
        full_name, is_active, account_id, card_id
    )
    VALUES (
        p_full_name, p_is_active, p_account_id, p_card_id
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm customer' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm customer thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddNetwork`(
    IN p_network_name VARCHAR(255),
    IN p_display_name VARCHAR(255),
    IN p_country_id INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO networks (
        network_name, display_name, country_id
    )
    VALUES (
        p_network_name, p_display_name, p_country_id
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm network' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm network thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPayment`(
    IN p_subscription_id INT,
    IN p_payment_date DATE,
    IN p_total_amount DECIMAL(10,2),
    IN p_payment_method VARCHAR(50),
    IN p_is_paid BOOLEAN,
    IN p_due_date DATE
)
BEGIN
    START TRANSACTION;

    INSERT INTO payments (
        subscription_id, payment_date, total_amount, payment_method, 
        is_paid, due_date
    )
    VALUES (
        p_subscription_id, p_payment_date, p_total_amount, p_payment_method, 
        p_is_paid, p_due_date
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm payment' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm payment thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPlan`(
    IN p_code VARCHAR(50),
    IN p_price DECIMAL(10,2),
    IN p_description TEXT,
    IN p_service_id INT,
    IN p_is_active BOOLEAN,
    IN p_renewal_syntax TEXT,
    IN p_registration_syntax TEXT,
    IN p_cancel_syntax TEXT,
    IN p_free_data DECIMAL(10,2),
    IN p_free_on_network_a_call INT,
    IN p_free_on_network_call INT,
    IN p_free_on_network_SMS INT,
    IN p_free_off_network_a_call INT,
    IN p_free_off_network_call INT,
    IN p_free_off_network_SMS INT,
    IN p_auto_renew BOOLEAN,
    IN p_staff_id INT
)
BEGIN
    START TRANSACTION;
    
    INSERT INTO plans (
        code, price, description, service_id, is_active, renewal_syntax, 
        registration_syntax, cancel_syntax, free_data, free_on_network_a_call, 
        free_on_network_call, free_on_network_SMS, free_off_network_a_call, 
        free_off_network_call, free_off_network_SMS, auto_renew, staff_id, 
        created_at, updated_at
    )
    VALUES (
        p_code, p_price, p_description, p_service_id, p_is_active, p_renewal_syntax,
        p_registration_syntax, p_cancel_syntax, p_free_data, p_free_on_network_a_call,
        p_free_on_network_call, p_free_on_network_SMS, p_free_off_network_a_call,
        p_free_off_network_call, p_free_off_network_SMS, p_auto_renew, p_staff_id,
        NOW(), NOW()
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm plan' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm plan thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddPlanDetail`(
    IN p_plan_id INT,
    IN p_object_type VARCHAR(50),
    IN p_duration INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO plan_detail (
        plan_id, object_type, duration
    )
    VALUES (
        p_plan_id, p_object_type, p_duration
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm plan detail' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm plan detail thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddRoleGroupDetail`(
    IN p_role_group_id INT,
    IN p_function_id INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO rolegroupdetail (
        role_group_id, function_id
    )
    VALUES (
        p_role_group_id, p_function_id
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm role group detail' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm role group detail thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddService`(
    IN p_service_name VARCHAR(100),
    IN p_parent_id INT,
    IN p_coverage_area INT,
    IN p_servicescol TEXT
)
BEGIN
    START TRANSACTION;

    INSERT INTO services (
        service_name, parent_id, coverage_area, servicescol
    )
    VALUES (
        p_service_name, p_parent_id, p_coverage_area, p_servicescol
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm service' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm service thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddStaff`(
    IN p_full_name VARCHAR(100),
    IN p_card_id VARCHAR(50),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_is_active BOOLEAN,
    IN p_gender VARCHAR(10),
    IN p_birthday DATE,
    IN p_account_id INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO staffs (
        full_name, card_id, phone, email, is_active, gender, birthday, account_id
    )
    VALUES (
        p_full_name, p_card_id, p_phone, p_email, p_is_active, p_gender, p_birthday, p_account_id
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm staff' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm staff thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddSubscriber`(
    IN p_phone_number VARCHAR(20),
    IN p_main_balance DECIMAL(10,2),
    IN p_activation_date DATETIME,
    IN p_expiration_date DATETIME,
    IN p_is_active BOOLEAN,
    IN p_customer_id INT,
    IN p_warning_date DATETIME,
    IN p_is_messaged BOOLEAN
)
BEGIN
    START TRANSACTION;
    
    INSERT INTO subscribers (
        phone_number, main_balance, activation_date, expiration_date, 
        is_active, customer_id, warning_date, is_messaged
    )
    VALUES (
        p_phone_number, p_main_balance, p_activation_date, p_expiration_date,
        p_is_active, p_customer_id, p_warning_date, p_is_messaged
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm subscriber' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm subscriber thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddSubscription`(
    IN p_plan_id INT,
    IN p_subscriber_id INT,
    IN p_created_at DATETIME,
    IN p_expiration_date DATETIME,
    IN p_renewal_total DECIMAL(10,2),
    IN p_is_renewal BOOLEAN,
    IN p_cancel_at DATETIME,
    IN p_activation_date DATETIME
)
BEGIN
    START TRANSACTION;

    INSERT INTO subscriptions (
        plan_id, subscriber_id, created_at, expiration_date, renewal_total, 
        is_renewal, cancel_at, activation_date
    )
    VALUES (
        p_plan_id, p_subscriber_id, p_created_at, p_expiration_date, p_renewal_total,
        p_is_renewal, p_cancel_at, p_activation_date
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm subscription' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm subscription thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `AddUsageLog`(
    IN p_type VARCHAR(50),
    IN p_usage_value DECIMAL(10,2),
    IN p_subscriber_id INT,
    IN p_start_date DATETIME,
    IN p_end_date DATETIME
)
BEGIN
    START TRANSACTION;

    INSERT INTO usage_logs (
        type, usage_value, subscriber_id, start_date, end_date
    )
    VALUES (
        p_type, p_usage_value, p_subscriber_id, p_start_date, p_end_date
    );
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm usage log' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Thêm usage log thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateAccount`(
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm tài khoản' AS message;
    END;

    START TRANSACTION;

    INSERT INTO accounts (username, passwork, is_active)
    VALUES (p_username, p_password, 1);

    COMMIT;

    SELECT TRUE AS success, 'Thêm tài khoản thành công' AS message, LAST_INSERT_ID() AS new_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateContract`(
    IN p_title VARCHAR(255),
    IN p_contents TEXT,
    IN p_subscriber VARCHAR(255),
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_subscriber_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thêm hợp đồng' AS message;
    END;

    START TRANSACTION;

    INSERT INTO contracts (title, contents, subscriber, start_date, end_date, is_active, subscriber_id, created_at)
    VALUES (p_title, p_contents, p_subscriber, p_start_date, p_end_date, 1, p_subscriber_id, NOW());

    COMMIT;

    SELECT TRUE AS success, 'Thêm hợp đồng thành công' AS message, LAST_INSERT_ID() AS new_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `CreateCountry`(
    IN p_country_name VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS error, 'Không thể thê quốc gia' AS message;
    END;

    START TRANSACTION;

    INSERT INTO countries (country_name)
    VALUES (p_country_name);

    COMMIT;

    SELECT TRUE AS success, 'Thêm quốc gia thành công' AS message, LAST_INSERT_ID() AS new_id;
END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteContract`(
    IN p_contract_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi: Không thể xóa hợp đồng' AS message;
    END;

    START TRANSACTION;

    UPDATE contracts
    SET is_active = 0
    WHERE id = p_contract_id;

    -- Kiểm tra số dòng bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy hợp đồng để xóa' AS message;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Xóa hợp đồng thành công' AS message;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteCountry`(
    IN p_country_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi: Không thể xóa quốc gia' AS message;
    END;

    START TRANSACTION;

    DELETE FROM countries
    WHERE id = p_country_id;

    -- Kiểm tra số dòng bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy quốc gia để xóa' AS message;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Xóa quốc gia thành công' AS message;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteCustomer`(
    IN p_customer_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE customers
    SET is_active = 0
    WHERE id = p_customer_id;

    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy customer để xóa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Xóa customer thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeletePlan`(
    IN p_plan_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE plans
    SET is_active = 0
    WHERE id = p_plan_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy plan để xóa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Xóa plan thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteStaff`(
    IN p_staff_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE staffs
    SET is_active = 0
    WHERE id = p_staff_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy staff để xóa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Xóa staff thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteSubscriber`(
    IN p_subscriber_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE subscribers
    SET is_active = 0
    WHERE id = p_subscriber_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy subscriber để xóa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Xóa subscriber thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAccountById`(
    IN p_account_id INT
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
END$$
DELIMITER ;


CREATE VIEW v_accounts AS
SELECT 
id, username, password, is_active 
FROM accounts;


CREATE VIEW v_contracts AS
    SELECT id, title, contents, subscriber, start_date, end_date, is_active, subscriber_id, created_at
    FROM contracts
    WHERE is_active = 1;

CREATE VIEW v_countries AS
    SELECT id, country_name FROM countries;

CREATE VIEW v_customers AS
    SELECT 
        id, full_name, is_active, account_id, card_id
    FROM customers;

CREATE VIEW v_functions AS
    SELECT 
        id, function_name, syntax_name
    FROM functions;


CREATE VIEW v_networks AS
    SELECT 
        id, network_name, display_name, country_id
    FROM networks;

CREATE VIEW v_payment_details AS
    SELECT 
        id, payment_id, free_data, free_on_a_call, free_offn_a_call,
        free_on_call, free_offn_call, free_on_sms, free_offn_sms,
        on_a_call_cost, on_sms_cost
    FROM payment_detail;


CREATE VIEW v_payments AS
SELECT 
    id, subscription_id, payment_date, total_amount, payment_method, 
    is_paid, due_date
FROM payments;


CREATE VIEW  v_permission_details AS
    SELECT 
        role_group_id, account_id
    FROM permissiondetail;

CREATE VIEW v_plan_details AS
    SELECT 
        plan_id, object_type, duration
    FROM plan_detail;

CREATE VIEW v_plan_networks AS
    SELECT 
        network_id, plan_id
    FROM plan_network;

CREATE VIEW v_plans AS
    SELECT 
        id, code, price, description, service_id, is_active, renewal_syntax, 
        registration_syntax, cancel_syntax, free_data, free_on_network_a_call, 
        free_on_network_call, free_on_network_SMS, free_off_network_a_call, 
        free_off_network_call, free_off_network_SMS, auto_renew, staff_id, 
        created_at, updated_at
    FROM plans;

CREATE VIEW v_role_group_details AS
    SELECT 
        role_group_id, function_id
    FROM rolegroupdetail;

CREATE VIEW v_role_groups AS
    SELECT 
        id, role_name
    FROM rolegroup;


CREATE VIEW v_services AS
    SELECT 
        id, service_name, parent_id, coverage_area, servicescol
    FROM services;

CREATE VIEW v_staffs AS
    SELECT 
        id, full_name, card_id, phone, email, is_active, gender, birthday, account_id
    FROM staffs;

CREATE VIEW  v_subscribers AS
    SELECT 
        id, phone_number, main_balance, activation_date, expiration_date, 
        is_active, customer_id, warning_date, is_messaged
    FROM subscribers;

CREATE VIEW  v_subscriptions AS
    SELECT 
        id, plan_id, subscriber_id, created_at, expiration_date, renewal_total, 
        is_renewal, cancel_at, activation_date
    FROM subscriptions;

CREATE VIEW  v_usage_logs AS
    SELECT 
        id, type, usage_value, subscriber_id, start_date, end_date
    FROM usage_logs;



CREATE VIEW v_vouchers AS
    SELECT 
        id, code, description, conandpromo, start_date, end_date, 
        usage_limit, remaining_count, is_active, staff_id, packages
    FROM vouchers;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetContractById`(
    IN p_contract_id INT
)
BEGIN
    DECLARE contract_count INT;

    -- Kiểm tra hợp đồng có tồn tại không
    SELECT COUNT(*) INTO contract_count
    FROM contracts
    WHERE id = p_contract_id AND is_active = 1;

    IF contract_count = 0 THEN
       SELECT FALSE AS error, 'Không tìm thấy hợp đồng' AS message;
    ELSE
        SELECT id, title, contents, subscriber, start_date, end_date, is_active, subscriber_id, created_at
        FROM contracts
        WHERE id = p_contract_id;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCountryById`(
    IN p_country_id INT
)
BEGIN
    DECLARE country_count INT;

    -- Kiểm tra quốc gia có tồn tại không
    SELECT COUNT(*) INTO country_count
    FROM countries
    WHERE id = p_country_id;

    IF country_count = 0 THEN
        SELECT FALSE AS error, 'Không tìm thấy quốc gia' AS message;
    ELSE
        SELECT id, country_name
        FROM countries
        WHERE id = p_country_id;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCustomerById`(
    IN p_customer_id INT
)
BEGIN
    SELECT 
        id, full_name, is_active, account_id, card_id
    FROM customers
    WHERE id = p_customer_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetFunctionById`(
    IN p_function_id INT
)
BEGIN
    SELECT 
        id, function_name, syntax_name
    FROM functions
    WHERE id = p_function_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetNetworkById`(
    IN p_network_id INT
)
BEGIN
    SELECT 
        id, network_name, display_name, country_id
    FROM networks
    WHERE id = p_network_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPaymentById`(
    IN p_payment_id INT
)
BEGIN
    SELECT 
        id, subscription_id, payment_date, total_amount, payment_method, 
        is_paid, due_date
    FROM payments
    WHERE id = p_payment_id;
END$$
DELIMITER ;

DELIMITER $$
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
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPermissionDetailById`(
    IN p_permission_detail_id INT
)
BEGIN
    SELECT 
        id, role_group_id, account_id
    FROM permissiondetail
    WHERE id = p_permission_detail_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPlanById`(
    IN p_plan_id INT
)
BEGIN
    SELECT 
        id, code, price, description, service_id, is_active, renewal_syntax, 
        registration_syntax, cancel_syntax, free_data, free_on_network_a_call, 
        free_on_network_call, free_on_network_SMS, free_off_network_a_call, 
        free_off_network_call, free_off_network_SMS, auto_renew, staff_id, 
        created_at, updated_at
    FROM plans
    WHERE id = p_plan_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPlanDetailById`(
    IN p_plan_detail_id INT
)
BEGIN
    SELECT 
        id, plan_id, object_type, duration
    FROM plan_detail
    WHERE id = p_plan_detail_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPlanNetworkById`(
    IN p_plan_network_id INT
)
BEGIN
    SELECT 
        id, network_id, plan_id
    FROM plan_network
    WHERE id = p_plan_network_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetRoleGroupById`(
    IN p_role_group_id INT
)
BEGIN
    SELECT 
        id, role_name
    FROM rolegroup
    WHERE id = p_role_group_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetRoleGroupDetailByRoleGroupId`(
    IN p_role_group_id INT
)
BEGIN
    SELECT 
        role_group_id, function_id
    FROM rolegroupdetail
    WHERE role_group_id = p_role_group_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetServiceById`(
    IN p_service_id INT
)
BEGIN
    SELECT 
        id, service_name, parent_id, coverage_area, servicescol
    FROM services
    WHERE id = p_service_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetStaffById`(
    IN p_staff_id INT
)
BEGIN
    SELECT 
        id, full_name, card_id, phone, email, is_active, gender, birthday, account_id
    FROM staffs
    WHERE id = p_staff_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetSubscriberById`(
    IN p_subscriber_id INT
)
BEGIN
    SELECT 
        id, phone_number, main_balance, activation_date, expiration_date, 
        is_active, customer_id, warning_date, is_messaged
    FROM subscribers
    WHERE id = p_subscriber_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetSubscriptionById`(
    IN p_subscription_id INT
)
BEGIN
    SELECT 
        id, plan_id, subscriber_id, created_at, expiration_date, renewal_total, 
        is_renewal, cancel_at, activation_date
    FROM subscriptions
    WHERE id = p_subscription_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetUsageLogById`(
    IN p_usage_log_id INT
)
BEGIN
    SELECT 
        id, type, usage_value, subscriber_id, start_date, end_date
    FROM usage_logs
    WHERE id = p_usage_log_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetVoucherById`(
    IN p_voucher_id INT
)
BEGIN
    SELECT 
        id, code, description, conandpromo, start_date, end_date, 
        usage_limit, remaining_count, is_active, staff_id, packages
    FROM vouchers
    WHERE id = p_voucher_id;
END$$
DELIMITER ;

DELIMITER $$
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
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateContract`(
    IN p_contract_id INT,
    IN p_title VARCHAR(255),
    IN p_contents TEXT,
    IN p_subscriber VARCHAR(255),
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi: Không thể cập nhật hợp đồng' AS message;
    END;

    START TRANSACTION;

    UPDATE contracts
    SET title = p_title,
        contents = p_contents,
        subscriber = p_subscriber,
        start_date = p_start_date,
        end_date = p_end_date
    WHERE id = p_contract_id;

    -- Kiểm tra số dòng bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy hợp đồng để cập nhật' AS message;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Cập nhật hợp đồng thành công' AS message;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateCountry`(
    IN p_country_id INT,
    IN p_country_name VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        SELECT FALSE AS success, 'Lỗi: Không thể cập nhật quốc gia' AS message;
    END;

    START TRANSACTION;

    UPDATE countries
    SET country_name = p_country_name
    WHERE id = p_country_id;

    -- Kiểm tra số dòng bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy quốc gia để cập nhât' AS message;
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Cập nhật quốc gia thành công' AS message;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateCustomer`(
    IN p_customer_id INT,
    IN p_full_name VARCHAR(255),
    IN p_is_active BOOLEAN,
    IN p_account_id INT,
    IN p_card_id VARCHAR(20)
)
BEGIN
    START TRANSACTION;

    UPDATE customers
    SET 
        full_name = p_full_name,
        is_active = p_is_active,
        account_id = p_account_id,
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

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateNetwork`(
    IN p_network_id INT,
    IN p_network_name VARCHAR(255),
    IN p_display_name VARCHAR(255),
    IN p_country_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE networks
    SET 
        network_name = p_network_name,
        display_name = p_display_name,
        country_id = p_country_id
    WHERE id = p_network_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy network để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa network thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdatePayment`(
    IN p_payment_id INT,
    IN p_subscription_id INT,
    IN p_payment_date DATE,
    IN p_total_amount DECIMAL(10,2),
    IN p_payment_method VARCHAR(50),
    IN p_is_paid BOOLEAN,
    IN p_due_date DATE
)
BEGIN
    START TRANSACTION;

    UPDATE payments
    SET 
        subscription_id = p_subscription_id,
        payment_date = p_payment_date,
        total_amount = p_total_amount,
        payment_method = p_payment_method,
        is_paid = p_is_paid,
        due_date = p_due_date
    WHERE id = p_payment_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy payment để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa payment thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdatePaymentDetail`(
    IN p_payment_detail_id INT,
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

    UPDATE payment_detail
    SET 
        payment_id = p_payment_id,
        free_data = p_free_data,
        free_on_a_call = p_free_on_a_call,
        free_offn_a_call = p_free_offn_a_call,
        free_on_call = p_free_on_call,
        free_offn_call = p_free_offn_call,
        free_on_sms = p_free_on_sms,
        free_offn_sms = p_free_offn_sms,
        on_a_call_cost = p_on_a_call_cost,
        on_sms_cost = p_on_sms_cost
    WHERE id = p_payment_detail_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy payment detail để sửa' AS message; 
    ELSE
        COMMIT;
       SELECT TRUE AS success, 'Sửa payment detail thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdatePermissionDetail`(
    IN p_permission_detail_id INT,
    IN p_role_group_id INT,
    IN p_account_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE permissiondetail
    SET 
        role_group_id = p_role_group_id,
        account_id = p_account_id
    WHERE id = p_permission_detail_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy permission detail để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa permission detail thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdatePlan`(
    IN p_plan_id INT,
    IN p_code VARCHAR(50),
    IN p_price DECIMAL(10,2),
    IN p_description TEXT,
    IN p_service_id INT,
    IN p_is_active BOOLEAN,
    IN p_renewal_syntax TEXT,
    IN p_registration_syntax TEXT,
    IN p_cancel_syntax TEXT,
    IN p_free_data DECIMAL(10,2),
    IN p_free_on_network_a_call INT,
    IN p_free_on_network_call INT,
    IN p_free_on_network_SMS INT,
    IN p_free_off_network_a_call INT,
    IN p_free_off_network_call INT,
    IN p_free_off_network_SMS INT,
    IN p_auto_renew BOOLEAN,
    IN p_staff_id INT
)
BEGIN
    START TRANSACTION;

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
        updated_at = NOW()
    WHERE id = p_plan_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy plan để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa plan thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
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

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateService`(
    IN p_service_id INT,
    IN p_service_name VARCHAR(100),
    IN p_parent_id INT,
    IN p_coverage_area INT,
    IN p_servicescol TEXT
)
BEGIN
    START TRANSACTION;

    UPDATE services
    SET 
        service_name = p_service_name,
        parent_id = p_parent_id,
        coverage_area = p_coverage_area,
        servicescol = p_servicescol
    WHERE id = p_service_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy service để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa service thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateStaff`(
    IN p_staff_id INT,
    IN p_full_name VARCHAR(100),
    IN p_card_id VARCHAR(50),
    IN p_phone VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_is_active BOOLEAN,
    IN p_gender VARCHAR(10),
    IN p_birthday DATE,
    IN p_account_id INT
)
BEGIN
    START TRANSACTION;

    UPDATE staffs
    SET 
        full_name = p_full_name,
        card_id = p_card_id,
        phone = p_phone,
        email = p_email,
        is_active = p_is_active,
        gender = p_gender,
        birthday = p_birthday,
        account_id = p_account_id
    WHERE id = p_staff_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy staff để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa staff thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateSubscriber`(
    IN p_subscriber_id INT,
    IN p_phone_number VARCHAR(20),
    IN p_main_balance DECIMAL(10,2),
    IN p_activation_date DATETIME,
    IN p_expiration_date DATETIME,
    IN p_is_active BOOLEAN,
    IN p_customer_id INT,
    IN p_warning_date DATETIME,
    IN p_is_messaged BOOLEAN
)
BEGIN
    START TRANSACTION;

    UPDATE subscribers
    SET 
        phone_number = p_phone_number,
        main_balance = p_main_balance,
        activation_date = p_activation_date,
        expiration_date = p_expiration_date,
        is_active = p_is_active,
        customer_id = p_customer_id,
        warning_date = p_warning_date,
        is_messaged = p_is_messaged
    WHERE id = p_subscriber_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy subscriber để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa subscriber thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateSubscription`(
    IN p_subscription_id INT,
    IN p_plan_id INT,
    IN p_subscriber_id INT,
    IN p_created_at DATETIME,
    IN p_expiration_date DATETIME,
    IN p_renewal_total DECIMAL(10,2),
    IN p_is_renewal BOOLEAN,
    IN p_cancel_at DATETIME,
    IN p_activation_date DATETIME
)
BEGIN
    START TRANSACTION;

    UPDATE subscriptions
    SET 
        plan_id = p_plan_id,
        subscriber_id = p_subscriber_id,
        created_at = p_created_at,
        expiration_date = p_expiration_date,
        renewal_total = p_renewal_total,
        is_renewal = p_is_renewal,
        cancel_at = p_cancel_at,
        activation_date = p_activation_date
    WHERE id = p_subscription_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy subscription để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa subscription thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateUsageLog`(
    IN p_usage_log_id INT,
    IN p_type VARCHAR(50),
    IN p_usage_value DECIMAL(10,2),
    IN p_subscriber_id INT,
    IN p_start_date DATETIME,
    IN p_end_date DATETIME
)
BEGIN
    START TRANSACTION;

    UPDATE usage_logs
    SET 
        type = p_type,
        usage_value = p_usage_value,
        subscriber_id = p_subscriber_id,
        start_date = p_start_date,
        end_date = p_end_date
    WHERE id = p_usage_log_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy usage log để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa usage log thành công' AS message;
    END IF;

END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateVoucher`(
    IN p_voucher_id INT,
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

    UPDATE vouchers
    SET 
        code = p_code,
        description = p_description,
        conandpromo = p_conandpromo,
        start_date = p_start_date,
        end_date = p_end_date,
        usage_limit = p_usage_limit,
        remaining_count = p_remaining_count,
        is_active = p_is_active,
        staff_id = p_staff_id,
        packages = p_packages
    WHERE id = p_voucher_id;
    
    -- Kiểm tra nếu không có dòng nào bị ảnh hưởng
    IF ROW_COUNT() = 0 THEN
        ROLLBACK;
        SELECT FALSE AS error, 'Không tìm thấy voucher để sửa' AS message; 
    ELSE
        COMMIT;
        SELECT TRUE AS success, 'Sửa voucher thành công' AS message;
    END IF;

END$$
DELIMITER ;
