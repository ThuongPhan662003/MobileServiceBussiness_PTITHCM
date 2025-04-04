from app.database import db_instance
from app.models.subscription import Subscription


class SubscriptionRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_subscriptions", fetchall=True)
            subscriptions = []

            for row in result:
                s = Subscription()
                s.id = row.get("id")
                s.plan_id = row.get("plan_id")
                s.subscriber_id = row.get("subscriber_id")
                s.created_at = row.get("created_at")
                s.expiration_date = row.get("expiration_date")
                s.renewal_total = row.get("renewal_total")
                s.is_renewal = row.get("is_renewal")
                s.cancel_at = row.get("cancel_at")
                s.activation_date = row.get("activation_date")
                subscriptions.append(s.to_dict())

            return subscriptions
        except Exception as e:
            print(f"Lỗi khi lấy danh sách subscription: {e}")
            return []

    @staticmethod
    def get_by_id(subscription_id):
        try:
            result = db_instance.execute(
                "CALL GetSubscriptionById(%s)", (subscription_id,), fetchone=True
            )
            if result:
                s = Subscription()
                for key, value in result.items():
                    setattr(s, key, value)
                return s
            return None
        except Exception as e:
            print(f"Lỗi khi lấy subscription theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Subscription):
        try:
            result = db_instance.execute(
                "CALL AddSubscription(%s, %s, %s, %s, %s, %s, %s)",
                (
                    data.plan_id,
                    data.subscriber_id,
                    data.expiration_date,
                    data.renewal_total,
                    data.is_renewal,
                    data.cancel_at,
                    data.activation_date,
                ),
                fetchone=True,
            )

            if result.get("error"):
                print(f"Lỗi khi thêm subscription: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm subscription: {e}")
            return False

    @staticmethod
    def update(subscription_id, data: Subscription):
        try:
            result = db_instance.execute(
                "CALL UpdateSubscription(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    subscription_id,
                    data.plan_id,
                    data.subscriber_id,
                    data.expiration_date,
                    data.renewal_total,
                    data.is_renewal,
                    data.cancel_at,
                    data.activation_date,
                ),
                fetchone=True,
            )

            if result.get("error"):
                print(f"Lỗi khi cập nhật subscription: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật subscription: {e}")
            return False

    @staticmethod
    def delete(subscription_id):
        try:
            result = db_instance.execute(
                "CALL DeleteSubscription(%s)", (subscription_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa subscription: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa subscription: {e}")
            return False
