from app import create_app
import atexit
from app.database import db_instance

app = create_app()


@atexit.register
def shutdown():
    db_instance.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS test_table (
        id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        value INT DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """

    try:
        db_instance.execute(create_table_sql, commit=True)
        print("✅ Đã tạo bảng test_table thành công (nếu chưa tồn tại)")
    except Exception as e:
        print("❌ Lỗi khi tạo bảng test_table:", str(e))
