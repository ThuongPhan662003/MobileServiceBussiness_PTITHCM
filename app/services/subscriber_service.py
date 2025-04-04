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
    def create_subscriber(data: dict):
        try:
            subscriber = Subscriber(
                phone_number=data.get("phone_number"),
                main_balance=Decimal(data.get("main_balance", 0)),
                activation_date=data.get("activation_date"),
                expiration_date=data.get("expiration_date"),
                is_active=data.get("is_active", True),
                customer_id=data.get("customer_id"),
                warning_date=data.get("warning_date"),
                is_messaged=data.get("is_messaged", False),
            )
            result = SubscriberRepository.insert(subscriber)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_subscriber(subscriber_id, data: dict):
        try:
            subscriber = Subscriber(
                phone_number=data.get("phone_number"),
                main_balance=Decimal(data.get("main_balance", 0)),
                activation_date=data.get("activation_date"),
                expiration_date=data.get("expiration_date"),
                is_active=data.get("is_active", True),
                customer_id=data.get("customer_id"),
                warning_date=data.get("warning_date"),
                is_messaged=data.get("is_messaged", False),
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
