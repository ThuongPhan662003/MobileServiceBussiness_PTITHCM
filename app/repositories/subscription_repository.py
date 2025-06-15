from app.database import db_instance
from app.models.subscription import Subscription


class SubscriptionRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_subscriptions", fetchall=True)
            subscriptions = []

            for row in result[0]:
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
            # Thực thi câu lệnh SQL
            result = db_instance.execute(
                "CALL AddSubscription(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data.plan_id,
                    data.subscriber_id,
                    data.created_at,
                    data.expiration_date,
                    data.renewal_total,
                    data.is_renewal,
                    data.cancel_at,
                    data.activation_date,
                ),
                fetchone=True,
                commit=True
            )
            if not isinstance(result, dict):
                print(f"Kết quả trả về không phải dictionary: {result}")
                return {"error": "Kết quả trả về không hợp lệ."}
            if result.get("error"):
                print(f"Lỗi khi thêm subscription: {result['error']}")

                return {"error": result["error"]}

            return result
        except Exception as e:
            print(f"Lỗi khi thêm subscription: {e}")
            return {"error": str(e)}

    @staticmethod
    def update(subscription_id, data: Subscription):
        try:
            # Giả sử bạn thực hiện cập nhật trong DB
            result = db_instance.execute(
                "CALL UpdateSubscription(%s, %s, %s, %s, %s, %s, %s)",
                (
                    subscription_id,
                    data.created_at,
                    data.expiration_date,
                    data.renewal_total,
                    data.is_renewal,
                    data.cancel_at,
                    data.activation_date,
                ),
                fetchone=True,
                commit=True,
            )

            # Nếu DB trả về kết quả hợp lệ, kiểm tra và trả kết quả thành công
            if result and isinstance(result, dict) and result.get("success"):
                return {"success": True}
            else:
                return {"error": "Không thể cập nhật subscription"}
        except Exception as e:
            print(f"Lỗi khi cập nhật subscription: {e}")
            return {"error": str(e)}

    @staticmethod
    def delete(subscription_id):
        try:
            result = db_instance.execute(
                "CALL DeleteSubscription(%s)", (subscription_id,), fetchone=True
            )
            print("kê", result)
            return result

        except Exception as e:
            return {"success": False, "message": f"Lỗi khi xóa subscription: {str(e)}"}

    @staticmethod
    def get_by_subscriber_and_plan(subscriber_id, plan_id):
        try:
            result = db_instance.execute(
                """
                SELECT * FROM subscriptions 
                WHERE subscriber_id = %s AND plan_id = %s 
                ORDER BY created_at DESC LIMIT 1
                """,
                (subscriber_id, plan_id),
                fetchone=True,
            )

            if result:
                s = Subscription()
                for key, value in result.items():
                    if key == "is_renewal":
                        setattr(s, key, bool(value))
                    else:
                        setattr(s, key, value)
                return s
            return None
        except Exception as e:
            print(f"Lỗi khi lấy subscription theo subscriber_id và plan_id: {e}")
            return None

    @staticmethod
    def get_subscription_by_subscriber_and_plan(subscriber_id, plan_id):
        try:
            query = """
                   SELECT id AS subscription_id
FROM subscriptions
WHERE subscriber_id = %s AND plan_id = %s 
ORDER BY created_at DESC
LIMIT 1;

                """
            result = db_instance.execute(query, (subscriber_id, plan_id), fetchone=True)

            if result:
                return result.get("subscription_id")
            else:
                return None  # Không tìm thấy subscription phù hợp
        except Exception as e:
            print(f"Lỗi khi truy vấn subscription: {e}")
            return None

    @staticmethod
    def get_by(subscriber_id):
        try:
            result = db_instance.execute(
                """
                CALL GetActiveSubscriptionDetailsBySubscriber(%s)
                """,
                (subscriber_id,),
                fetchall=True,
            )
            print("Kết quả trả về từ stored procedure:", result)

            # Kiểm tra nếu kết quả trả về không trống
            if result and isinstance(
                result[0], list
            ):  # Kiểm tra kiểu dữ liệu của phần tử đầu tiên
                subscriptions = []
                for row in result[
                    0
                ]:  # Truy cập phần tử đầu tiên trong danh sách (mảng 2 chiều)
                    subscription = {
                        "subscription_id": row["subscription_id"],
                        "plan_id": row["plan_id"],
                        "plan_code": row["plan_code"],
                        "free_data": row["free_data"],
                        "cancel_at": row["cancel_at"],
                        "expiration_date": row["expiration_date"],
                    }
                    subscriptions.append(subscription)
                return subscriptions

            return []
        except Exception as e:
            print(f"Lỗi khi lấy thông tin gói cước theo subscriber_id: {e}")
            return []
