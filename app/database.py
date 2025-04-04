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

        with self.connection.cursor() as cursor:
            cursor.execute(sql, params or ())

            results = []  # Danh sách lưu tất cả kết quả trả về
            # Nếu không có kết quả và yêu cầu commit, thì thực hiện commit
            if commit:
                self.connection.commit()
            # Lấy kết quả đầu tiên nếu fetchall = True
            if fetchall:
                results.append(cursor.fetchall())

            # Nếu có nhiều kết quả, sử dụng nextset để lấy các kết quả tiếp theo
            while cursor.nextset():  # Tiến tới kết quả tiếp theo
                if fetchall:
                    results.append(cursor.fetchall())

            # Nếu chỉ cần lấy một kết quả duy nhất, sử dụng fetchone
            if fetchone:
                result = cursor.fetchone()
                return result

            # Nếu muốn lấy tất cả kết quả, trả về danh sách results
            if fetchall:
                return results

            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("🔌 Đã đóng kết nối database")


# Tạo instance khi import
db_instance = Database()
