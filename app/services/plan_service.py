from app.repositories.plan_repository import PlanRepository
from app.models.plan import Plan


class PlanService:
    @staticmethod
    def get_all_plans():
        return PlanRepository.get_all()

    @staticmethod
    def get_plan_by_id(plan_id):
        return PlanRepository.get_by_id(plan_id)

    @staticmethod
    def create_plan(data: dict):
        try:
            plan = Plan(
                code=data.get("code"),
                price=data.get("price"),
                description=data.get("description"),
                service_id=data.get("service_id"),
                is_active=data.get("is_active", True),
                renewal_syntax=data.get("renewal_syntax"),
                registration_syntax=data.get("registration_syntax"),
                cancel_syntax=data.get("cancel_syntax"),
                free_data=data.get("free_data", 0),
                free_on_network_a_call=data.get("free_on_network_a_call", 0),
                free_on_network_call=data.get("free_on_network_call", 0),
                free_on_network_SMS=data.get("free_on_network_SMS", 0),
                free_off_network_a_call=data.get("free_off_network_a_call", 0),
                free_off_network_call=data.get("free_off_network_call", 0),
                free_off_network_SMS=data.get("free_off_network_SMS", 0),
                auto_renew=data.get("auto_renew", False),
                staff_id=data.get("staff_id"),
                maximum_on_network_call=data.get("maximum_on_network_call", 0),
            )
            result = PlanRepository.insert(plan)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_plan(plan_id, data: dict):
        try:
            plan = Plan(
                code=data.get("code"),
                price=data.get("price"),
                description=data.get("description"),
                service_id=data.get("service_id"),
                is_active=data.get("is_active", True),
                renewal_syntax=data.get("renewal_syntax"),
                registration_syntax=data.get("registration_syntax"),
                cancel_syntax=data.get("cancel_syntax"),
                free_data=data.get("free_data", 0),
                free_on_network_a_call=data.get("free_on_network_a_call", 0),
                free_on_network_call=data.get("free_on_network_call", 0),
                free_on_network_SMS=data.get("free_on_network_SMS", 0),
                free_off_network_a_call=data.get("free_off_network_a_call", 0),
                free_off_network_call=data.get("free_off_network_call", 0),
                free_off_network_SMS=data.get("free_off_network_SMS", 0),
                auto_renew=data.get("auto_renew", False),
                staff_id=data.get("staff_id"),
                maximum_on_network_call=data.get("maximum_on_network_call", 0),
            )
            result = PlanRepository.update(plan_id, plan)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_plan(plan_id):
        try:
            result = PlanRepository.delete(plan_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
