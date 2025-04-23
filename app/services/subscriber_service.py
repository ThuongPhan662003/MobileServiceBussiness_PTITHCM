from datetime import datetime

from app.repositories.subscriber_repository import SubscriberRepository
from app.models.subscriber import Subscriber
from decimal import Decimal


class SubscriberService:
    @staticmethod
    def get_all_subscribers():
        return SubscriberRepository.get_all()

    @staticmethod
    def get_subscriber_by_id(subscriber_id):
        return SubscriberRepository.get_by_id(subscriber_id)

    @staticmethod
    def get_by_account_id(account_id: int):
        return SubscriberRepository.get_by_account_id(account_id)

    @staticmethod
    def create_subscriber(data: dict):
        try:
            # Chuyển đổi các giá trị từ input thành kiểu phù hợp
            phone_number = data.get("phone_number")
            main_balance = Decimal(data.get("main_balance", 0))  # Chuyển thành Decimal
            activation_date_str = data.get("activation_date")
            expiration_date_str = data.get("expiration_date")
            is_active = str(data.get("is_active", "true")).lower() == "true"
            customer_id = int(data.get("customer_id") )
            warning_date_str = data.get("warning_date")
            is_messaged = str(data.get("is_messaged", "true")).lower() == "true"
            activation_date = datetime.strptime(activation_date_str, "%Y-%m-%d").date() if activation_date_str else None
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date() if expiration_date_str else None
            warning_date = datetime.strptime(warning_date_str, "%Y-%m-%d") if warning_date_str else None

            subscriber = Subscriber(
                phone_number=phone_number,
                main_balance=main_balance,
                activation_date=activation_date,
                expiration_date=expiration_date,
                is_active=is_active,  # Đảm bảo là 1 hoặc 0
                customer_id=customer_id,  # customer_id có thể là NULL
                warning_date=warning_date,
                is_messaged=is_messaged,  # Đảm bảo là 1 hoặc 0
            )

            # Chèn vào cơ sở dữ liệu
            result = SubscriberRepository.insert(subscriber)

            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            print(f"Lỗi: {e}")
            return {"error": str(e)}

    @staticmethod
    def update_subscriber(subscriber_id, data: dict):
        try:
            phone_number = data.get("phone_number")
            main_balance = Decimal(data.get("main_balance", 0))  # Chuyển thành Decimal
            activation_date_str = data.get("activation_date")
            expiration_date_str = data.get("expiration_date")
            is_active = str(data.get("is_active", "true")).lower() == "true"
            customer_id = int(data.get("customer_id"))
            warning_date_str = data.get("warning_date")
            is_messaged = str(data.get("is_messaged", "true")).lower() == "true"
            activation_date = datetime.strptime(activation_date_str, "%Y-%m-%d").date() if activation_date_str else None
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date() if expiration_date_str else None
            warning_date = datetime.strptime(warning_date_str, "%Y-%m-%d") if warning_date_str else None

            subscriber = Subscriber(
                phone_number=phone_number,
                main_balance=main_balance,
                activation_date=activation_date,
                expiration_date=expiration_date,
                is_active=is_active,  # Đảm bảo là 1 hoặc 0
                customer_id=customer_id,  # customer_id có thể là NULL
                warning_date=warning_date,
                is_messaged=is_messaged,  # Đảm bảo là 1 hoặc 0
            )

            result = SubscriberRepository.update(subscriber_id, subscriber)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_subscriber(subscriber_id):
        try:
            result = SubscriberRepository.delete(subscriber_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
