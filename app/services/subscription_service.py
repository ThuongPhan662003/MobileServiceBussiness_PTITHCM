from datetime import datetime, timedelta


from app.repositories.plan_repository import PlanRepository
from app.repositories.plandetail_repository import PlanDetailRepository
from app.repositories.subscriber_repository import SubscriberRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.models.subscription import Subscription
from app.services.plan_service import PlanService


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
            subscriber = SubscriberRepository.get_by_id(subscriber_id)

            plans = PlanRepository.get_by_id(plan_id)
            created_at = datetime.now()
            plan = PlanDetailRepository.get_by_id(plan_id)

            if not plan:
                return {"error": "Không tìm thấy gói cước."}

            active_service_ids_set = SubscriberRepository.get_active_service_ids(
                subscriber_id
            )

            active_service_ids_flat = {
                service["service_id"]
                for sublist in active_service_ids_set
                for service in sublist
            }

            print(
                f"Plans Service ID muốn đăng ký: {plans.service_id.id}"
            )  # In service_id của gói cước
            print(f"Active Service IDs đã được xử lý: {active_service_ids_flat}")

            # Kiểm tra gói cước muốn đăng ký
            if plans.service_id.id == 2:
                if 2 in active_service_ids_flat:
                    return {"error": "Bạn đã đăng kí gói cước chính."}

            elif plans.service_id.id in {3, 4, 5, 6}:
                if any(
                    service_id in {3, 4, 5, 6} for service_id in active_service_ids_flat
                ):
                    return {"error": "Bạn đã đăng kí gói cước di động."}
            activation_date = datetime.now()
            if subscriber.subscriber_type == "TRATRUOC":
                if plan.duration < 1:
                    expiration_date = datetime.now() + timedelta(
                        hours=plan.duration * 24
                    )
                else:
                    today = datetime(
                        datetime.now().year, datetime.now().month, datetime.now().day
                    )
                    expiration_date = today + timedelta(days=int(plan.duration))
            else:
                if plan.duration < 1:
                    expiration_date = datetime.now() + timedelta(
                        hours=plan.duration * 24
                    )
                elif 1 <= plan.duration <= 30:
                    today = datetime.now().replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                    expiration_date = today + timedelta(days=int(plan.duration))
                else:
                    now = datetime.now()
                    months_to_add = int(plan.duration // 30)
                    new_month = now.month + months_to_add
                    new_year = now.year + (new_month - 1) // 12
                    new_month = (new_month - 1) % 12 + 1
                    expiration_date = datetime(new_year, new_month, 1, 0, 0, 0)

            subscription = Subscription(
                plan_id=plan_id,
                subscriber_id=subscriber_id,
                created_at=created_at,
                expiration_date=expiration_date,
                renewal_total=0,
                is_renewal=True,
                cancel_at=None,
                activation_date=activation_date,
            )

            result = SubscriptionRepository.insert(subscription)

            if isinstance(result, dict) and result.get("subscription_id"):
                return {
                    "success": True,
                    "created": True,
                    "subscription_id": result["subscription_id"],
                }
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
            return result
        except Exception as e:
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}

    @staticmethod
    def get_plan_exp(subscriber_id):
        try:
            # Gọi method của repository để lấy thông tin gói cước
            result = SubscriptionRepository.get_by(subscriber_id)
            print("Kết quả từ get_by:", result)

            # Kiểm tra nếu kết quả hợp lệ
            if result:
                return result
            else:
                print(
                    "Không tìm thấy thông tin gói cước cho subscriber_id:",
                    subscriber_id,
                )
                return None  # Hoặc có thể trả về một danh sách rỗng nếu cần
        except Exception as e:
            print(f"Lỗi khi lấy thông tin gói cước: {e}")
            return None
