from app.database import db_instance
from app.models.plan import Plan


class PlanRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_plans", fetchall=True)
            plans = []

            for row in result:
                plan = Plan()
                plan.id = row.get("id")
                plan.code = row.get("code")
                plan.price = row.get("price")
                plan.description = row.get("description")
                plan.service_id = row.get("service_id")
                plan.is_active = row.get("is_active")
                plan.renewal_syntax = row.get("renewal_syntax")
                plan.registration_syntax = row.get("registration_syntax")
                plan.cancel_syntax = row.get("cancel_syntax")
                plan.free_data = row.get("free_data")
                plan.free_on_network_a_call = row.get("free_on_network_a_call")
                plan.free_on_network_call = row.get("free_on_network_call")
                plan.free_on_network_SMS = row.get("free_on_network_SMS")
                plan.free_off_network_a_call = row.get("free_off_network_a_call")
                plan.free_off_network_call = row.get("free_off_network_call")
                plan.free_off_network_SMS = row.get("free_off_network_SMS")
                plan.auto_renew = row.get("auto_renew")
                plan.staff_id = row.get("staff_id")
                plan.created_at = row.get("created_at")
                plan.updated_at = row.get("updated_at")
                plan.maximum_on_network_call = row.get("maximum_on_network_call")
                plans.append(plan.to_dict())

            return plans
        except Exception as e:
            print(f"Lỗi khi lấy danh sách plan: {e}")
            return []

    @staticmethod
    def get_by_id(plan_id):
        try:
            result = db_instance.execute(
                "CALL GetPlanById(%s)", (plan_id,), fetchone=True
            )
            if result:
                plan = Plan()
                for key in result:
                    setattr(plan, key, result[key])
                return plan
            return None
        except Exception as e:
            print(f"Lỗi khi lấy plan theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Plan):
        try:
            result = db_instance.execute(
                "CALL AddPlan(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data.code,
                    data.price,
                    data.description,
                    data.service_id,
                    data.is_active,
                    data.renewal_syntax,
                    data.registration_syntax,
                    data.cancel_syntax,
                    data.free_data,
                    data.free_on_network_a_call,
                    data.free_on_network_call,
                    data.free_on_network_SMS,
                    data.free_off_network_a_call,
                    data.free_off_network_call,
                    data.free_off_network_SMS,
                    data.auto_renew,
                    data.staff_id,
                    data.maximum_on_network_call,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm plan: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm plan: {e}")
            return False

    @staticmethod
    def update(plan_id, data: Plan):
        try:
            result = db_instance.execute(
                "CALL UpdatePlan(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    plan_id,
                    data.code,
                    data.price,
                    data.description,
                    data.service_id,
                    data.is_active,
                    data.renewal_syntax,
                    data.registration_syntax,
                    data.cancel_syntax,
                    data.free_data,
                    data.free_on_network_a_call,
                    data.free_on_network_call,
                    data.free_on_network_SMS,
                    data.free_off_network_a_call,
                    data.free_off_network_call,
                    data.free_off_network_SMS,
                    data.auto_renew,
                    data.staff_id,
                    data.maximum_on_network_call,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật plan: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật plan: {e}")
            return False

    @staticmethod
    def delete(plan_id):
        try:
            result = db_instance.execute("CALL DeletePlan(%s)", (plan_id,), fetchone=True)
            if result.get("error"):
                print(f"Lỗi khi xóa plan: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa plan: {e}")
            return False
