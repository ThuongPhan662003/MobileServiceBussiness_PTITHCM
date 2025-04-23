
# from app.repositories.plan_repository import PlanRepository
# from app.models.plan import Plan


# class PlanService:
#     @staticmethod
#     def get_all_plans():
#         return PlanRepository.get_all()

#     @staticmethod
#     def get_plan_by_id(plan_id):
#         return PlanRepository.get_by_id(plan_id)

#     @staticmethod
#     def create_plan(data: dict):
#         try:
#             plan = Plan(
#                 code=data.get("code"),
#                 price=data.get("price"),
#                 description=data.get("description"),
#                 service_id=data.get("service_id"),
#                 is_active=data.get("is_active", True),
#                 renewal_syntax=data.get("renewal_syntax"),
#                 registration_syntax=data.get("registration_syntax"),
#                 cancel_syntax=data.get("cancel_syntax"),
#                 free_data=data.get("free_data", 0),
#                 free_on_network_a_call=data.get("free_on_network_a_call", 0),
#                 free_on_network_call=data.get("free_on_network_call", 0),
#                 free_on_network_SMS=data.get("free_on_network_SMS", 0),
#                 free_off_network_a_call=data.get("free_off_network_a_call", 0),
#                 free_off_network_call=data.get("free_off_network_call", 0),
#                 free_off_network_SMS=data.get("free_off_network_SMS", 0),
#                 auto_renew=data.get("auto_renew", False),
#                 staff_id=data.get("staff_id"),
#                 maximum_on_network_call=data.get("maximum_on_network_call", 0),
#                 ON_SMS_cost=data.get("ON_SMS_cost"),
#                 ON_a_call_cost=data.get("ON_a_call_cost"),
#             )
#             result = PlanRepository.insert(plan)
#             if result is True:
#                 return {"success": True}
#             return {"error": result}
#         except Exception as e:
#             return {"error": str(e)}

#     @staticmethod
#     def update_plan(plan_id, data: dict):
#         try:
#             plan = Plan(
#                 code=data.get("code"),
#                 price=data.get("price"),
#                 description=data.get("description"),
#                 service_id=data.get("service_id"),
#                 is_active=data.get("is_active", True),
#                 renewal_syntax=data.get("renewal_syntax"),
#                 registration_syntax=data.get("registration_syntax"),
#                 cancel_syntax=data.get("cancel_syntax"),
#                 free_data=data.get("free_data", 0),
#                 free_on_network_a_call=data.get("free_on_network_a_call", 0),
#                 free_on_network_call=data.get("free_on_network_call", 0),
#                 free_on_network_SMS=data.get("free_on_network_SMS", 0),
#                 free_off_network_a_call=data.get("free_off_network_a_call", 0),
#                 free_off_network_call=data.get("free_off_network_call", 0),
#                 free_off_network_SMS=data.get("free_off_network_SMS", 0),
#                 auto_renew=data.get("auto_renew", False),
#                 staff_id=data.get("staff_id"),
#                 maximum_on_network_call=data.get("maximum_on_network_call", 0),
#                 ON_SMS_cost=data.get("ON_SMS_cost"),
#                 ON_a_call_cost=data.get("ON_a_call_cost"),
#             )
#             result = PlanRepository.update(plan_id, plan)
#             if result is True:
#                 return {"success": True}
#             return {"error": result}
#         except Exception as e:
#             return {"error": str(e)}

#     @staticmethod
#     def lock_plan(plan_id):
#         try:
#             result = PlanRepository.lock(plan_id)
#             if result is True:
#                 return {"success": True}
#             return {"error": result}
#         except Exception as e:
#             return {"error": str(e)}

#     @staticmethod
#     def search_plans(code, price, is_active):
#         try:
#             return PlanRepository.search(code, price, is_active)
#         except Exception as e:
#             print(f"Lỗi khi tìm kiếm plans: {e}")
#             return []


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
                ON_SMS_cost=data.get("ON_SMS_cost"),
                ON_a_call_cost=data.get("ON_a_call_cost"),
            )
            result = PlanRepository.insert(plan)
            if result is True:
                return {"success": True}
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
                ON_SMS_cost=data.get("ON_SMS_cost"),
                ON_a_call_cost=data.get("ON_a_call_cost"),
            )
            result = PlanRepository.update(plan_id, plan)
            if result is True:
                return {"success": True}
            return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def lock_plan(plan_id):
        try:
            result = PlanRepository.lock(plan_id)
            if result is True:
                return {"success": True}
            return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def search_plans(code, price, is_active):
        try:
            return PlanRepository.search(code, price, is_active)
        except Exception as e:
            print(f"Lỗi khi tìm kiếm plans: {e}")
            return []

    @staticmethod
    def get_sub_services(parent_service_id):
        return PlanRepository.get_sub_services(parent_service_id)

    @staticmethod
    def get_plans_by_service_id(service_id):
        plans = PlanRepository.get_plans_by_service_id(service_id)
        return [
            {
                "id": plan["id"],
                "code": plan["code"],
                "price": f"{plan['price']:,}",
                "description": plan["description"],
                "free_data": plan["free_data"],
                "service_id": plan["service_id"],
            }
            for plan in plans
        ]

    @staticmethod
    def get_plan_details(plan_id):
        plan = PlanRepository.get_by_id(plan_id)
        if plan:
            plan_dict = plan.to_dict()
            return {
                "id": plan_dict["id"],
                "code": plan_dict["code"],
                "price": f"{plan_dict['price']:,}",
                "description": plan_dict["description"],
                "free_data": plan_dict["free_data"],
                "service_id": plan_dict["service_id"],
                "registration_syntax": plan_dict["registration_syntax"],  # Thêm cú pháp đăng ký
                "renewal_syntax": plan_dict["renewal_syntax"],  # Thêm cú pháp gia hạn
                "cancel_syntax": plan_dict["cancel_syntax"],  # Thêm cú pháp hủy
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
        return None