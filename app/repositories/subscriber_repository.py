from app.database import db_instance
from app.models.subscriber import Subscriber
from decimal import Decimal


class SubscriberRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_subscribers", fetchall=True)
            subscribers = []

            for row in result:
                s = Subscriber()
                s.id = row.get("id")
                s.phone_number = row.get("phone_number")
                s.main_balance = row.get("main_balance") or Decimal("0.00")
                s.activation_date = row.get("activation_date")
                s.expiration_date = row.get("expiration_date")
                s.is_active = row.get("is_active")
                s.customer_id = row.get("customer_id")
                s.warning_date = row.get("warning_date")
                s.is_messaged = row.get("is_messaged")
                subscribers.append(s.to_dict())

            return subscribers
        except Exception as e:
            print(f"Lỗi khi lấy danh sách subscriber: {e}")
            return []

    @staticmethod
    def get_by_id(subscriber_id):
        try:
            result = db_instance.execute(
                "CALL GetSubscriberById(%s)", (subscriber_id,), fetchone=True
            )
            if result:
                s = Subscriber()
                for key, val in result.items():
                    setattr(s, key, val)
                return s
            return None
        except Exception as e:
            print(f"Lỗi khi lấy subscriber theo ID: {e}")
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
