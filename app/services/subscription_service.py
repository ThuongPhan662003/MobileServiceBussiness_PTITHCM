from app.repositories.subscription_repository import SubscriptionRepository
from app.models.subscription import Subscription


class SubscriptionService:
    @staticmethod
    def get_all_subscriptions():
        return SubscriptionRepository.get_all()

    @staticmethod
    def get_subscription_by_id(subscription_id):
        return SubscriptionRepository.get_by_id(subscription_id)

    @staticmethod
    def create_subscription(data: dict):
        try:
            subscription = Subscription(
                plan_id=data.get("plan_id"),
                subscriber_id=data.get("subscriber_id"),
                # expiration_date=data.get("expiration_date"),
                # renewal_total=data.get("renewal_total", 0),
                # is_renewal=data.get("is_renewal", True),
                # cancel_at=data.get("cancel_at"),
                # activation_date=data.get("activation_date"),
            )
            result = SubscriptionRepository.insert(subscription)
            if result["subscription_id"]:
                return {"success": True, "subscription_id": result["subscription_id"]}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_subscription(subscription_id, data: dict):
        try:
            subscription = Subscription(
                plan_id=data.get("plan_id"),
                subscriber_id=data.get("subscriber_id"),
                expiration_date=data.get("expiration_date"),
                renewal_total=data.get("renewal_total", 0),
                is_renewal=data.get("is_renewal", True),
                cancel_at=data.get("cancel_at"),
                activation_date=data.get("activation_date"),
            )
            result = SubscriptionRepository.update(subscription_id, subscription)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_subscription(subscription_id):
        try:
            result = SubscriptionRepository.delete(subscription_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
