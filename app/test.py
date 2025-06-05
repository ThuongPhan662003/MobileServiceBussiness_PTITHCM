from database import db_instance

# # ✅ INSERT
# insert_result = db_instance.execute(
#     "INSERT INTO test_table (name, value) VALUES (%s, %s)", ("Test 1", 100), commit=True
# )
# print("✅ INSERT thành công")

# # ✅ SELECT ALL
# select_all = db_instance.execute("SELECT * FROM test_table", fetchall=True)
# print(
#     "📄 Dữ liệu test_table:", select_all[0]
# )  # Chỉ cần [0] vì fetchall trả về danh sách kết quả từ nhiều result sets

# # ✅ SELECT ONE
# select_one = db_instance.execute(
#     "SELECT * FROM test_table WHERE name = %s", ("Test 1",), fetchone=True
# )
# print("🔍 Dòng tìm được:", select_one)

# # ✅ UPDATE
# update_result = db_instance.execute(
#     "UPDATE test_table SET value = %s WHERE name = %s", (200, "Test 1"), commit=True
# )
# print("🛠️ Cập nhật thành công")

# # ✅ DELETE
# delete_result = db_instance.execute(
#     "DELETE FROM test_table WHERE name = %s", ("Test 1",), commit=True
# )
# print("🗑️ Xóa thành công")


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
