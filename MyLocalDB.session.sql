-- CREATE DEFINER=`root`@`localhost` PROCEDURE `GetUsageLogBySubscriberId`(IN subscriber_id INT)
-- BEGIN
--     SELECT id, type, usage_value, subscriber_id, start_date, end_date, by_from, `to`, contents
--     FROM usage_logs
--     WHERE id = subscriber_id;
-- END
-- CALL GetUsageLogBySubscriberId(12)
drop PROCEDURE if exists sp_warn_and_lock_accounts;
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
END
