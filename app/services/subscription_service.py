from datetime import datetime, timedelta

from app.repositories.plan_repository import PlanRepository
from app.repositories.plandetail_repository import PlanDetailRepository
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
    def create_subscription(subscriber_id: int, plan_id: int):
        try:

            created_at = datetime.now()

            # Lấy thông tin gói cước từ repository
            plan = PlanDetailRepository.get_by_id(plan_id)
            if not plan:
                return {"error": "Không tìm thấy gói cước."}

            expiration_date = created_at + timedelta(days=plan.duration)

            # Kiểm tra subscription đã tồn tại chưa
            existing = SubscriptionRepository.get_by_subscriber_and_plan(subscriber_id, plan_id)

            if existing:
                # Cập nhật subscription đã có
                existing.created_at = created_at
                existing.expiration_date = expiration_date
                existing.activation_date = existing.activation_date  # Không thay đổi activation_date
                existing.is_renewal = True
                existing.cancel_at = None
                existing.renewal_total = existing.renewal_total + 1

                result = SubscriptionRepository.update(existing.id, existing)

                if isinstance(result, dict) and result.get("success"):
                    return {"success": True, "updated": True, "subscription_id": existing.id}
                else:
                    return {"error": "Lỗi khi cập nhật subscription."}

            else:
                # Tạo mới subscription
                subscription = Subscription(
                    plan_id=plan_id,
                    subscriber_id=subscriber_id,
                    created_at=created_at,
                    expiration_date=expiration_date,
                    renewal_total=0,
                    is_renewal=True,
                    cancel_at=None,
                    activation_date=created_at,
                )

                result = SubscriptionRepository.insert(subscription)

                if isinstance(result, dict) and result.get("subscription_id"):
                    return {"success": True, "created": True, "subscription_id": result["subscription_id"]}
                else:
                    return {"error": "Lỗi khi tạo subscription."}
        except Exception as e:
            return {"error": str(e)}
    @staticmethod
    def update_subscription(subscription_id, data: dict):
        try:
            subscription = Subscription(
                plan_id=data.get("plan_id"),
                subscriber_id=data.get("subscriber_id"),
                created_at=data.get("created_at"),
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
