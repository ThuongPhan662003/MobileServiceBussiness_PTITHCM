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
                s.main_balance = Decimal(row.get("main_balance")) if row.get("main_balance") is not None else Decimal("0.00")
                s.activation_date = row.get("activation_date")
                s.expiration_date = row.get("expiration_date")
                s.account_id = int(row.get("account_id")) if row.get("account_id") is not None else None
                s.is_active = bool(row.get("is_active"))
                s.customer_id = int(row.get("customer_id")) if row.get("customer_id") is not None else None
                s.warning_date = row.get("warning_date")
                s.subscriber_type = row.get("subscriber_type")

                # Xử lý kiểu bytes (bit) cho is_messaged
                is_messaged_raw = row.get("is_messaged")
                if isinstance(is_messaged_raw, bytes):
                    s.is_messaged = bool(int.from_bytes(is_messaged_raw, "little"))
                else:
                    s.is_messaged = bool(is_messaged_raw)

                subscribers.append(s.to_dict())

            return subscribers

        except Exception as e:
            print(f"Lỗi khi lấy danh sách subscriber: {e}")
            return []

    @staticmethod
    def get_by_id(subscriber_id):
        try:
            result = db_instance.execute(
                "SELECT * FROM subscribers WHERE id = %s", (subscriber_id,), fetchone=True
            )
            if result:
                s = Subscriber()
                for key, val in result.items():
                    if key == "main_balance":
                        setattr(s, key, Decimal(val) if val is not None else Decimal("0.00"))
                    elif key in ["is_active", "is_messaged"]:
                        setattr(s, key, bool(val))
                    else:
                        setattr(s, key, val)
                return s
            return None
        except Exception as e:
            print(f"Lỗi khi lấy subscriber theo ID: {e}")
            return None

    @staticmethod
    def create(data: Subscriber):
        try:
            print(data.to_dict())
            result = db_instance.execute(
                "CALL AddSubscriber(%s, %s, %s, %s, %s, %s)",  # SP: AddSubscriber
                (
                    data.phone_number,
                    float(data.main_balance or 0),
                    data.expiration_date,
                    data.subscriber_type,  # Kiểu BOOLEAN: Trả sau = True, Trả trước = False
                    data.customer_id,
                    data.account_id
                ),
                fetchone=True,
                commit=True
            )

            if result.get("error"):
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi tạo subscriber: {e}")
            return str(e)

    @staticmethod
    def update(subscriber_id, data: Subscriber):
        try:
            result = db_instance.execute(
                "CALL UpdateSubscriber(%s, %s, %s, %s, %s, %s, %s, %s, %s)",  # Thêm parameter subscriber_type
                (
                    subscriber_id,
                    data.phone_number,
                    float(data.main_balance or 0),
                    data.expiration_date,
                    data.is_active,
                    data.customer_id,
                    data.warning_date,
                    data.subscriber_type,  # Thêm subscriber_type
                    data.account_id
                ),
                fetchone=True,
                commit=True
            )
            if result.get("error"):
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật subscriber: {e}")
            return False

    @staticmethod
    def delete(subscriber_id):
        try:
            result = db_instance.execute(
                "CALL DeleteSubscriber(%s)", (subscriber_id,), fetchone=True, commit=True
            )
            if result.get("error"):
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xoá subscriber: {e}")
            return False
