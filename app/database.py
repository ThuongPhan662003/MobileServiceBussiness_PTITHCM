import pymysql
from config import Config


class Database:
    def __init__(self):
        self.host = Config.DB_HOST
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        self.db_name = Config.DB_NAME
        self.cursor_class = pymysql.cursors.DictCursor

        # Kết nối ngay khi khởi tạo
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db_name,
                cursorclass=self.cursor_class,
            )
            print("✅ Kết nối database thành công!")
        except Exception as e:
            print("❌ Kết nối database thất bại:", e)
            self.connection = None

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        if self.connection:
            return self.connection.cursor()
        return None

    def execute(self, sql, params=None, fetchone=False, fetchall=False, commit=False):
        if not self.connection:
            raise Exception("Chưa kết nối tới database")

        with self.connection.cursor(self.cursor_class) as cursor:
            cursor.execute(sql, params or ())

            # Nếu có thay đổi dữ liệu (INSERT, UPDATE, DELETE)
            if commit:
                self.connection.commit()
                print("oke commit")

            # Nếu chỉ cần lấy một dòng (fetchone)
            if fetchone:
                result = cursor.fetchone()
                # Nếu có nhiều result sets, tìm result đầu tiên có dữ liệu
                # print("result=", result)
                while not result and cursor.nextset():
                    result = cursor.fetchone()
                print("result=", result)
                return result

            # Nếu muốn lấy tất cả dữ liệu từ tất cả result sets
            if fetchall:
                results = []
                results.append(cursor.fetchall())
                while cursor.nextset():
                    results.append(cursor.fetchall())
                return results

            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("🔌 Đã đóng kết nối database")


# Tạo instance khi import
db_instance = Database()
