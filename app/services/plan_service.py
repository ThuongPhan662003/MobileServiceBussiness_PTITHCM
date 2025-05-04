from app.models.plan import Plan
from app.repositories.plan_repository import PlanRepository


class PlanService:
    @staticmethod
    def _create_plan_object(data):
        plan = Plan()
        plan.code = data.get("code")
        plan.price = float(data.get("price")) if data.get("price") else None
        plan.description = data.get("description")
        plan.service_id = (
            int(data.get("service_id")) if data.get("service_id") else None
        )
        plan.is_active = data.get("is_active", False)
        plan.renewal_syntax = data.get("renewal_syntax")
        plan.registration_syntax = data.get("registration_syntax")
        plan.cancel_syntax = data.get("cancel_syntax")
        plan.free_data = int(data.get("free_data", 0))
        plan.free_on_network_a_call = int(data.get("free_on_network_a_call", 0))
        plan.free_on_network_call = int(data.get("free_on_network_call", 0))
        plan.free_on_network_SMS = int(data.get("free_on_network_SMS", 0))
        plan.free_off_network_a_call = int(data.get("free_off_network_a_call", 0))
        plan.free_off_network_call = int(data.get("free_off_network_call", 0))
        plan.free_off_network_SMS = int(data.get("free_off_network_SMS", 0))
        plan.auto_renew = data.get("auto_renew", False)
        plan.staff_id = int(data.get("staff_id")) if data.get("staff_id") else None
        plan.maximum_on_network_call = int(data.get("maximum_on_network_call", 0))
        plan.ON_SMS_cost = (
            float(data.get("ON_SMS_cost", 0)) if data.get("ON_SMS_cost") else None
        )
        plan.ON_a_call_cost = (
            float(data.get("ON_a_call_cost", 0)) if data.get("ON_a_call_cost") else None
        )
        return plan

    @staticmethod
    def get_all_plans():
        result = PlanRepository.get_all()
        if isinstance(result, dict) and "error" in result:
            return []
        return result

    @staticmethod
    def get_plan_by_code(code):
        result = PlanRepository.get_by_code(code)
        if isinstance(result, dict) and "error" in result:
            return None
        return result

    @staticmethod
    def check_syntax_exists(field, value, plan_id=None):
        if not value:
            return False
        result = PlanRepository.check_syntax_exists(field, value, plan_id)
        if isinstance(result, dict) and "error" in result:
            return False
        return result

    @staticmethod
    def create_plan(data):
        try:
            plan = PlanService._create_plan_object(data)
            object_type = data.get("object_type")
            duration = int(data.get("duration")) if data.get("duration") else None

            result = PlanRepository.insert(plan, object_type, duration)
            if result is True:
                return {"success": True}
            return {"success": False, "error": result}
        except Exception as e:
            return {"success": False, "error": f"Không thể tạo gói cước: {str(e)}"}

    @staticmethod
    def update_plan(plan_id, data):
        try:
            plan = PlanService._create_plan_object(data)
            object_type = data.get("object_type")
            duration = int(data.get("duration")) if data.get("duration") else None

            result = PlanRepository.update(plan_id, plan, object_type, duration)
            if result is True:
                return {"success": True}
            return {"success": False, "error": result}
        except Exception as e:
            return {"success": False, "error": f"Không thể cập nhật gói cước: {str(e)}"}

    @staticmethod
    def lock_plan(plan_id):
        try:
            result = PlanRepository.lock(plan_id)
            if result is True:
                return {"success": True}
            return {"success": False, "error": result}
        except Exception as e:
            return {"success": False, "error": f"Không thể khóa gói cước: {str(e)}"}

    @staticmethod
    def search_plans(code, price, is_active, object_type):
        result = PlanRepository.search(code, price, is_active, object_type)
        if isinstance(result, dict) and "error" in result:
            return []
        return result

    @staticmethod
    def get_sub_services(parent_service_id):
        result = PlanRepository.get_sub_services(parent_service_id)
        if isinstance(result, dict) and "error" in result:
            return []
        return result

    @staticmethod
    def get_plans_by_service_id(service_id):
        plans = PlanRepository.get_plans_by_service_id(service_id)
        if isinstance(plans, dict) and "error" in plans:
            return []
        return [
            {
                "id": plan["id"],
                "code": plan["code"],
                "price": plan["price"],
                "description": plan["description"],
                "free_data": plan["free_data"],
                "service_id": plan["service_id"],
            }
            for plan in plans
        ]

    @staticmethod
    def get_plan_details(plan_id):
        plan = PlanRepository.get_by_id(plan_id)
        if isinstance(plan, dict) and "error" in plan:
            return None
        if plan:
            plan_dict = plan.to_dict()
            return {
                "id": plan_dict["id"],
                "code": plan_dict["code"],
                "price": plan_dict["price"],
                "description": plan_dict["description"],
                "free_data": plan_dict["free_data"],
                "service_id": plan_dict["service_id"],
                "registration_syntax": plan_dict["registration_syntax"],
                "renewal_syntax": plan_dict["renewal_syntax"],
                "cancel_syntax": plan_dict["cancel_syntax"],
                "free_off_network_SMS": plan_dict["free_off_network_SMS"],
                "free_off_network_call": plan_dict["free_off_network_call"],
                "free_off_network_a_call": plan_dict["free_off_network_a_call"],
                "free_on_network_SMS": plan_dict["free_on_network_SMS"],
                "free_on_network_call": plan_dict["free_on_network_call"],
                "free_on_network_a_call": plan_dict["free_on_network_a_call"],
                "maximum_on_network_call": plan_dict["maximum_on_network_call"],
                "auto_renew": plan_dict["auto_renew"],
                "ON_a_call_cost": plan_dict["ON_a_call_cost"],
                "ON_SMS_cost": plan_dict["ON_SMS_cost"],
            }

    @staticmethod
    def get_all_codes():
        result = PlanRepository.get_all_codes()
        if isinstance(result, dict) and "error" in result:
            return []
        return result

    @staticmethod
    def get_plan_detail_from_subscription(subscription_id):
        return PlanRepository.get_plan_by_subscription_id(subscription_id)
