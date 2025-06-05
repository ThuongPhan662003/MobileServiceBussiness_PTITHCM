import pymysql
from config import Config


def create_procedure():
    drop_sql = "DROP PROCEDURE IF EXISTS sp_accounts_update_password_by_username"

    create_sql = """
    CREATE PROCEDURE sp_accounts_update_password_by_username (
        IN p_username VARCHAR(255),
        IN p_new_password VARCHAR(255)
    )
    BEGIN
        UPDATE accounts
        SET password = p_new_password
        WHERE username = p_username;
    END;
    """  # <-- Lưu ý dấu ; sau END

    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
        with conn.cursor() as cursor:
            cursor.execute(drop_sql)
            cursor.execute(create_sql)  # ✅ Không split, giữ nguyên toàn bộ
        print("✅ Tạo stored procedure thành công.")
    except Exception as e:
        print("❌ Lỗi khi tạo procedure:", e)
    finally:
        conn.close()


create_procedure()
