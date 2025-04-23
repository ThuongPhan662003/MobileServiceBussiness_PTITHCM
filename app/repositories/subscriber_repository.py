from app.database import db_instance
from app.models.account import Account
from app.models.subscriber import Subscriber
from decimal import Decimal

from app.services.account_service import AccountService
from app.services.customer_service import CustomerService


class SubscriberRepository:
    from decimal import Decimal

    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_subscribers", fetchall=True)
            subscribers = []
            # print(result)
            for row in result[0]:
                s = Subscriber()
                s.id = row.get("id")
                s.phone_number = row.get("phone_number")
                s.main_balance = row.get("main_balance") or Decimal("0.00")
                s.activation_date = row.get("activation_date")
                s.expiration_date = row.get("expiration_date")
                # Ép kiểu bool đúng chuẩn
                acc_result = AccountService.get_account_by_id(row.get("account_id"))
                s.account_id = acc_result
                s.account_id = row.get("account_id")
                s.is_active = bool(row.get("is_active"))
                cus = CustomerService.get_customer_by_id(row.get("customer_id"))
                s.customer_id = cus
                s.warning_date = row.get("warning_date")
                # s.is_messaged = (
                #     bool(int.from_bytes(row.get("is_messaged"), "little"))
                #     if isinstance(row.get("is_messaged"), bytes)
                #     else bool(row.get("is_messaged"))
                # )
                subscribers.append(s.to_dict())

            return subscribers
        except Exception as e:
            print(f"Lỗi khi lấy danh sách subscriber: {e}")
            return []

    @staticmethod
    def get_by_id(subscriber_id):
        try:
            result = db_instance.execute(
                "SELECT * FROM subscribers WHERE id =%s",
                (subscriber_id,),
                fetchone=True,
            )
            from decimal import Decimal

            if result:
                s = Subscriber()
                for key, val in result.items():
                    # Xử lý kiểu dữ liệu đặc biệt
                    if key == "main_balance":
                        setattr(
                            s, key, Decimal(val) if val is not None else Decimal("0.00")
                        )
                    elif key in ["is_active", "is_messaged"]:
                        setattr(s, key, bool(val))
                    else:
                        setattr(s, key, val)
                return s

        except Exception as e:
            print(f"Lỗi khi lấy subscriber theo ID: {e}")
            return None

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
    def insert(data: Subscriber):
        try:
            result = db_instance.execute(
                "CALL AddSubscriber(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data.phone_number,
                    float(data.main_balance or 0),
                    data.activation_date,
                    data.expiration_date,
                    data.is_active,
                    data.customer_id,
                    data.warning_date,
                    data.is_messaged,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm subscriber: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm subscriber: {e}")
            return False

    @staticmethod
    def update(subscriber_id, data: Subscriber):
        try:
            result = db_instance.execute(
                "CALL UpdateSubscriber(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    subscriber_id,
                    data.phone_number,
                    float(data.main_balance or 0),
                    data.activation_date,
                    data.expiration_date,
                    data.is_active,
                    data.customer_id,
                    data.warning_date,
                    data.is_messaged,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật subscriber: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật subscriber: {e}")
            return False

    @staticmethod
    def delete(subscriber_id):
        try:
            result = db_instance.execute(
                "CALL DeleteSubscriber(%s)", (subscriber_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa subscriber: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa subscriber: {e}")
            return False
