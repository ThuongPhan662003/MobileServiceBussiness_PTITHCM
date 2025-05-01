from app.database import db_instance
from app.models import Service, Staff
from app.models.plan import Plan
from app.repositories.service_repository import ServiceRepository
from app.repositories.staff_repository import StaffRepository

# import logging

# logging.basicConfig(filename='app.log', level=logging.ERROR)


class PlanRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("CALL GetAllPlans()", fetchall=True)
            plans = []
            for row in result[0]:
                plan = Plan()
                for key in row:
                    if key in ("is_active", "auto_renew"):
                        value = row[key]
                        setattr(
                            plan, key, bool(int(value)) if value is not None else False
                        )
                    elif key in ("ON_SMS_cost", "ON_a_call_cost", "price"):
                        value = row[key]
                        setattr(plan, key, float(value) if value is not None else None)
                    else:
                        setattr(plan, key, row[key])
                plans.append(plan)
            return plans
        except Exception as e:
            # logging.error(f"Lỗi khi lấy danh sách plan: {e}")
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
                    if key in ("is_active", "auto_renew"):
                        value = result[key]
                        setattr(
                            plan, key, bool(int(value)) if value is not None else False
                        )
                    elif key in ("ON_SMS_cost", "ON_a_call_cost", "price"):
                        value = result[key]
                        setattr(plan, key, float(value) if value is not None else None)
                    else:
                        setattr(plan, key, result[key])
                return plan
            return None
        except Exception as e:
            # logging.error(f"Lỗi khi lấy plan theo ID: {e}")
            return None

    @staticmethod
    def get_by_code(code):
        try:
            result = db_instance.execute(
                "SELECT id FROM plans WHERE code = %s", (code,), fetchone=True
            )
            if result:
                plan = Plan()
                plan.id = result["id"]
                return plan
            return None
        except Exception as e:
            # logging.error(f"Lỗi khi kiểm tra mã code: {e}")
            return None

    @staticmethod
    def check_syntax_exists(field, value, plan_id=None):
        try:
            query = f"SELECT id FROM plans WHERE {field} = %s"
            params = (value,)
            if plan_id:
                query += " AND id != %s"
                params = (value, plan_id)
            result = db_instance.execute(query, params, fetchone=True)
            return bool(result)
        except Exception as e:
            # logging.error(f"Lỗi khi kiểm tra cú pháp {field}: {e}")
            return False

    @staticmethod
    def insert(data: Plan, object_type: str, duration: int):
        try:
            result = db_instance.execute(
                "CALL AddPlan(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
                    data.ON_SMS_cost,
                    data.ON_a_call_cost,
                    object_type,
                    duration,
                ),
                fetchone=True,
                commit=True,
            )
            if result and result.get("error"):
                # logging.error(f"Lỗi khi thêm plan: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            # logging.error(f"Lỗi khi thêm plan: {e}")
            return str(e)

    @staticmethod
    def update(plan_id, data: Plan, object_type: str, duration: int):
        try:
            result = db_instance.execute(
                "CALL UpdatePlan(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
                    data.ON_SMS_cost,
                    data.ON_a_call_cost,
                    object_type,
                    duration,
                ),
                fetchone=True,
                commit=True,
            )
            if result and result.get("error"):
                # logging.error(f"Lỗi khi cập nhật plan: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            # logging.error(f"Lỗi khi cập nhật plan: {e}")
            return str(e)

    @staticmethod
    def lock(plan_id):
        try:
            result = db_instance.execute(
                "CALL LockPlan(%s)", (plan_id,), fetchone=True, commit=True
            )
            if result and result.get("error"):
                # logging.error(f"Lỗi khi khóa plan: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            # logging.error(f"Lỗi khi khóa plan: {e}")
            return str(e)

    @staticmethod
    def search(code, price, is_active, object_type):
        try:
            params = (
                code if code else None,
                float(price) if price else None,
                int(is_active) if is_active is not None else None,
                object_type if object_type else None,
            )
            result = db_instance.execute(
                "CALL SearchPlans(%s, %s, %s, %s)", params, fetchall=True
            )
            plans = []
            for row in result[0]:
                plan = Plan()
                for key in row:
                    if key in ("is_active", "auto_renew"):
                        value = row[key]
                        setattr(
                            plan, key, bool(int(value)) if value is not None else False
                        )
                    elif key in ("ON_SMS_cost", "ON_a_call_cost", "price"):
                        value = row[key]
                        setattr(plan, key, float(value) if value is not None else None)
                    else:
                        setattr(plan, key, row[key])
                plans.append(
                    plan.to_dict_plan(
                        duration=row.get("duration", None),
                        object_type=row.get("object_type", None),
                    )
                )
            return plans
        except Exception as e:
            # logging.error(f"Lỗi khi tìm kiếm plans: {e}")
            return []

    @staticmethod
    def get_sub_services(parent_service_id):
        try:
            result = db_instance.execute(
                "SELECT id, service_name FROM services WHERE parent_id = %s",
                (parent_service_id,),
                fetchall=True,
            )
            return [
                {"id": row["id"], "service_name": row["service_name"]}
                for row in result[0]
            ]
        except Exception as e:
            # logging.error(f"Lỗi khi lấy danh sách sub-services: {e}")
            return []

    @staticmethod
    def get_plans_by_service_id(service_id):
        try:
            result = db_instance.execute(
                "SELECT * FROM v_plans WHERE service_id = %s AND is_active = TRUE",
                (service_id,),
                fetchall=True,
            )
            plans = []
            for row in result[0]:
                plan = Plan()
                plan.id = row.get("id")
                plan.code = row.get("code")
                plan.price = row.get("price")
                plan.description = row.get("description")
                plan.service_id = row.get("service_id")
                plan.is_active = True if row.get("is_active") else False
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
                plan.auto_renew = True if row.get("auto_renew") else False
                plan.staff_id = row.get("staff_id")
                plan.created_at = row.get("created_at")
                plan.updated_at = row.get("updated_at")
                plan.maximum_on_network_call = row.get("maximum_on_network_call")
                plan.ON_SMS_cost = row.get("ON_SMS_cost")
                plan.ON_a_call_cost = row.get("ON_a_call_cost")
                plans.append(plan.to_dict())
            return plans
        except Exception as e:
            # logging.error(f"Lỗi khi lấy danh sách gói cước theo service_id: {e}")
            return []

    @staticmethod
    def get_by_plan_id(plan_id):
        try:
            result = db_instance.execute(
                "CALL GetPlanById(%s)", (plan_id,), fetchone=True
            )
            if result:
                plan = Plan()
                for key in result:
                    if key in ("is_active", "auto_renew"):
                        value = result[key]
                        setattr(
                            plan, key, bool(int(value)) if value is not None else False
                        )

                    elif key in ("ON_SMS_cost", "ON_a_call_cost", "price"):
                        value = result[key]
                        setattr(plan, key, float(value) if value is not None else None)
                    elif key in ("service_id"):
                        value = ServiceRepository.get_by_id(result[key])
                        setattr(plan, key, value if value else None)
                    elif key in ("staff_id"):
                        value = StaffRepository.get_by_id(result[key])
                        setattr(plan, key, value if value is not None else None)
                    else:
                        setattr(plan, key, result[key])
                return plan
            return None
        except Exception as e:
            print(f"Lỗi khi lấy plan theo ID: {e}")
            return None

    @staticmethod
    def get_all_codes():
        try:
            result = db_instance.execute(
                "SELECT DISTINCT code FROM plans WHERE is_active = 1", fetchall=True
            )
            return [row["code"] for row in result[0]] if result else []
        except Exception as e:
            print("Lỗi khi lấy danh sách mã gói:", e)
            return []
