import atexit
import pymysql
from config import Config


class Database:
    def __init__(self):
        self.host = Config.DB_HOST
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        self.db_name = Config.DB_NAME
        self.cursor_class = pymysql.cursors.DictCursor
        self.connection = self.connect()  # ✅ Khởi tạo kết nối ban đầu

    def connect(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db_name,
                cursorclass=self.cursor_class,
            )
            print("✅ Kết nối database thành công!")
            return conn
        except Exception as e:
            print("❌ Kết nối database thất bại:", e)
            return None

    def execute(self, sql, params=None, fetchone=False, fetchall=False, commit=False):
        conn = self.connect()
        if not conn:
            raise Exception("Không thể kết nối tới database")

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                print("✅ Đã thực thi truy vấn:", sql)

                if commit:
                    self.commit()
                    print("✅ Đã commit dữ liệu")

                if fetchone:
                    result = cursor.fetchone()
                    while not result and cursor.nextset():
                        result = cursor.fetchone()
                    print("✅ fetchone", result)
                    return result

                if fetchall:
                    results = []
                    results.append(cursor.fetchall())
                    while cursor.nextset():
                        results.append(cursor.fetchall())
                    return results

                return None
        except Exception as e:
            print("❌ Lỗi khi thực thi truy vấn:", repr(e))
            raise

    def close(self):  # ✅ Đóng kết nối khi chương trình kết thúc
        if self.connection:
            try:
                self.connection.close()
                print("🔌 Đã đóng kết nối database")
            except Exception as e:
                print("⚠️ Lỗi khi đóng kết nối:", e)

    def execute_with_connection(self, queries):
        conn = self.connect()
        if not conn:
            raise Exception("Không thể kết nối tới database")
        try:
            with conn.cursor() as cursor:
                return queries(cursor, conn)
        except Exception as e:
            print("❌ Lỗi execute_with_connection:", repr(e))
            raise
        finally:
            try:
                conn.close()
            except:
                pass


# Tạo instance khi import
db_instance = Database()


@atexit.register
def cleanup():
    db_instance.close()





