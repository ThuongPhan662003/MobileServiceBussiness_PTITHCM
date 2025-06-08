from datetime import datetime
from decimal import Decimal
from app.database import db_instance
from app.models.subscriber import Subscriber
from app.repositories.account_repository import AccountRepository


class SubscriberRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_subscribers", fetchall=True)
            rows = result[0] if result else []

            subscribers = []

            for row in rows:
                s = Subscriber()
                s.id = int(row.get("id")) if row.get("id") is not None else None
                s.phone_number = row.get("phone_number")
                s.main_balance = (
                    Decimal(row.get("main_balance"))
                    if row.get("main_balance") is not None
                    else Decimal("0.00")
                )
                s.activation_date = row.get("activation_date")
                s.expiration_date = row.get("expiration_date")
                s.account_id = (
                    int(row.get("account_id"))
                    if row.get("account_id") is not None
                    else None
                )
                s.is_active = bool(row.get("is_active"))
                s.customer_id = (
                    int(row.get("customer_id"))
                    if row.get("customer_id") is not None
                    else None
                )
                s.warning_date = row.get("warning_date")
                s.subscriber = row.get("subscriber")
                s.ON_a_call_cost = row.get("ON_a_call_cost")
                s.ON_SMS_cost = row.get("ON_SMS_cost")
                s.subscriber = row.get("subscriber")
                subscribers.append(s.to_dict())

            return subscribers

        except Exception as e:
            print(f"Lỗi khi lấy danh sách subscriber: {e}")
            return []

    @staticmethod
    def get_by_id(subscriber_id):
        try:
            result = db_instance.execute(
                "SELECT * FROM subscribers WHERE id = %s",
                (subscriber_id,),
                fetchone=True,
            )
            if result:
                s = Subscriber()
                s.id = result.get("id")
                s.phone_number = result.get("phone_number")
                s.main_balance = Decimal(result.get("main_balance", 0.0))
                s.activation_date = result.get("activation_date")
                s.expiration_date = result.get("expiration_date")
                s.is_active = result.get("is_active") == 1
                s.customer_id = result.get("customer_id")
                s.warning_date = result.get("warning_date")
                s.subscriber = result.get("subscriber")
                s.account_id = result.get("account_id")
                s.subscriber_type = result.get("subscriber_type")
                s.ON_a_call_cost = result.get("ON_a_call_cost")
                s.ON_SMS_cost = result.get("ON_SMS_cost")
                return s
            else:
                return None
        except Exception as e:
            print(f"Lỗi khi lấy subscriber theo ID: {e}")
            return None

    @staticmethod
    def get_active_service_ids(subscriber_id: int):
        try:
            # Thực thi stored procedure để lấy các service_id mà thuê bao đã đăng ký
            result = db_instance.execute(
                """
                CALL GetActiveServiceIdBySubscriber(%s);
                """,
                (subscriber_id,),
                fetchall=True,
            )

            # Kiểm tra kết quả trả về có dữ liệu hay không
            if result:
                # Trả về kết quả gốc từ database, không cần xử lý thêm
                print(f"Kết quả trả về từ database: {result}")  # In ra kết quả trả về
                return result
            else:
                return (
                    []
                )  # Trả về danh sách rỗng nếu không có gói cước nào được đăng ký

        except Exception as e:
            print(f"Lỗi khi lấy service_id của thuê bao {subscriber_id}: {e}")
            return []  # Trả về danh sách rỗng khi có lỗi xảy ra

    @staticmethod
    def get_by_account_id(account_id: int):
        try:
            result = db_instance.execute(
                "CALL sp_subscriber_get_by_account_id(%s)", (account_id,), fetchone=True
            )
            print("result", result)
            return result
        except Exception as e:
            print(f"Lỗi khi lấy subscriber theo account_id: {e}")
            return None

    @staticmethod
    def create(data: Subscriber):
        try:
            # Chuyển đổi bool subscriber thành chuỗi "TRASAU" hoặc "TRATRUOC"
            subscriber_type = "TRASAU" if data.subscriber else "TRATRUOC"

            result = db_instance.execute(
                "CALL AddSubscriber(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data.phone_number,
                    float(data.main_balance or 0),
                    data.expiration_date,
                    data.customer_id,
                    data.account_id,
                    float(data.ON_a_call_cost or 0),
                    float(data.ON_SMS_cost or 0),
                    subscriber_type,
                ),
                fetchone=True,
                commit=True,
            )

            if result and result.get("error"):
                return result["error"]
            return True

        except Exception as e:
            print(f"❌ Lỗi khi tạo subscriber: {e}")
            return str(e)

    @staticmethod
    def update(subscriber_id, data: Subscriber):
        try:
            result = db_instance.execute(
                """
                CALL UpdateSubscriber(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    subscriber_id,
                    data.phone_number,
                    float(data.main_balance or 0),
                    data.expiration_date,
                    data.is_active,
                    data.warning_date,
                    data.subscriber,  # Tên hiển thị hoặc mã thuê bao
                    data.customer_id,
                    data.account_id,
                    float(data.ON_a_call_cost or 0),
                    float(data.ON_SMS_cost or 0),
                ),
                fetchone=True,
                commit=True,
            )
            if result and not result.get("success"):
                return result.get("message", "Cập nhật thất bại")
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật subscriber: {e}")
            return False

    @staticmethod
    def delete(subscriber_id):
        try:
            result = db_instance.execute(
                "CALL DeleteSubscriber(%s)",
                (subscriber_id,),
                fetchone=True,
                commit=True,
            )
            if result.get("error"):
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xoá subscriber: {e}")
            return False
