from app.database import db_instance
from app.models import Service, Staff
from app.models.plan import Plan
from app.repositories.service_repository import ServiceRepository
from app.repositories.staff_repository import StaffRepository


class PlanRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("CALL GetAllPlans()", fetchall=True)
            plans = []
            for row in result[0]:
                # plan = PlanRepository._row_to_plan(row)
                print("row", row)
                plan = Plan()
                plan.id = row.get("id")
                plan.code = row.get("code") if row.get("code") is not None else None
                plan.price = row.get("price") if row.get("price") is not None else None
                plan.description = (
                    row.get("description")
                    if row.get("description") is not None
                    else None
                )
                print("plan", plan.to_dict_plan())
                service_id = (
                    row.get("service_id") if row.get("service_id") is not None else None
                )
                if service_id:
                    service = ServiceRepository.get_by_id(service_id)
                    plan.service_id = service if service else None
                plan.is_active = True if row.get("is_active") else False
                plan.renewal_syntax = (
                    row.get("renewal_syntax")
                    if row.get("renewal_syntax") is not None
                    else None
                )
                plan.registration_syntax = (
                    row.get("registration_syntax")
                    if row.get("registration_syntax") is not None
                    else None
                )
                plan.cancel_syntax = (
                    row.get("cancel_syntax")
                    if row.get("cancel_syntax") is not None
                    else None
                )
                plan.free_data = (
                    row.get("free_data") if row.get("free_data") is not None else None
                )
                plan.free_on_network_a_call = (
                    row.get("free_on_network_a_call")
                    if row.get("free_on_network_a_call") is not None
                    else None
                )
                plan.free_on_network_call = (
                    row.get("free_on_network_call")
                    if row.get("free_on_network_call") is not None
                    else None
                )
                plan.free_on_network_SMS = (
                    row.get("free_on_network_SMS")
                    if row.get("free_on_network_SMS") is not None
                    else None
                )
                plan.free_off_network_a_call = (
                    row.get("free_off_network_a_call")
                    if row.get("free_off_network_a_call") is not None
                    else None
                )
                plan.free_off_network_call = (
                    row.get("free_off_network_call")
                    if row.get("free_off_network_call") is not None
                    else None
                )
                plan.free_off_network_SMS = (
                    row.get("free_off_network_SMS")
                    if row.get("free_off_network_SMS") is not None
                    else None
                )
                plan.auto_renew = True if row.get("auto_renew") else False
                staff_id = (
                    row.get("staff_id") if row.get("staff_id") is not None else None
                )
                if staff_id:
                    staff = StaffRepository.get_by_id(staff_id)
                    if isinstance(staff, dict) and "error" in staff:
                        plan.staff_id = None
                    else:
                        plan.staff_id = staff
                else:
                    plan.staff_id = None
                plan.maximum_on_network_call = (
                    row.get("maximum_on_network_call")
                    if row.get("maximum_on_network_call") is not None
                    else None
                )
                plan.ON_SMS_cost = (
                    row.get("ON_SMS_cost")
                    if row.get("ON_SMS_cost") is not None
                    else None
                )
                plan.ON_a_call_cost = (
                    row.get("ON_a_call_cost")
                    if row.get("ON_a_call_cost") is not None
                    else None
                )
                plan.object_type = (
                    row.get("object_type")
                    if row.get("object_type") is not None
                    else None
                )
                plan.duration = (
                    row.get("duration") if row.get("duration") is not None else None
                )
                plans.append(plan)
            return plans
        except Exception as e:
            return {"error": f"Không thể lấy danh sách gói cước: {str(e)}"}

    @staticmethod
    def get_by_id(plan_id):
        try:
            result = db_instance.execute(
                "CALL GetPlanById(%s)", (plan_id,), fetchone=True
            )
            if result:
                return PlanRepository._row_to_plan(result)
            return None
        except Exception as e:
            return {"error": f"Không thể lấy gói cước theo ID {plan_id}: {str(e)}"}

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
            return {"error": f"Không thể kiểm tra mã code {code}: {str(e)}"}

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
            return {
                "error": f"Không thể kiểm tra cú pháp {field} với giá trị {value}: {str(e)}"
            }

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
                return result["error"]
            return True
        except Exception as e:
            error_msg = str(e)
            # Xử lý lỗi từ stored procedure
            if "Mã gói cước đã tồn tại" in error_msg:
                return "Mã gói cước đã tồn tại"
            elif "Cú pháp đăng ký đã tồn tại" in error_msg:
                return "Cú pháp đăng ký đã tồn tại"
            elif "Cú pháp gia hạn đã tồn tại" in error_msg:
                return "Cú pháp gia hạn đã tồn tại"
            elif "Cú pháp hủy đã tồn tại" in error_msg:
                return "Cú pháp hủy đã tồn tại"
            elif "ID Dịch vụ không tồn tại" in error_msg:
                return "ID Dịch vụ không tồn tại"
            elif "ID Nhân viên không tồn tại" in error_msg:
                return "ID Nhân viên không tồn tại"
            elif "Hình thức thanh toán phải là TRATRUOC hoặc TRASAU" in error_msg:
                return "Hình thức thanh toán phải là TRATRUOC hoặc TRASAU"
            elif "Thời hạn phải là số dương" in error_msg:
                return "Thời hạn phải là số dương"
            elif "Mã gói cước là bắt buộc" in error_msg:
                return "Mã gói cước là bắt buộc"
            elif "Giá gói cước phải là số dương" in error_msg:
                return "Giá gói cước phải là số dương"
            elif "ID Dịch vụ là bắt buộc" in error_msg:
                return "ID Dịch vụ là bắt buộc"
            # Xử lý lỗi Duplicate entry từ ràng buộc UNIQUE
            if "Duplicate entry" in error_msg:
                if "code" in error_msg:
                    return "Mã gói cước đã tồn tại"
                elif "registration_syntax" in error_msg:
                    return "Cú pháp đăng ký đã tồn tại"
                elif "renewal_syntax" in error_msg:
                    return "Cú pháp gia hạn đã tồn tại"
                elif "cancel_syntax" in error_msg:
                    return "Cú pháp hủy đã tồn tại"
            return f"Không thể thêm gói cước: {error_msg}"

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
                return result["error"]
            return True
        except Exception as e:
            error_msg = str(e)
            # Xử lý lỗi từ stored procedure
            if "Mã gói cước đã tồn tại" in error_msg:
                return "Mã gói cước đã tồn tại"
            elif "Cú pháp đăng ký đã tồn tại" in error_msg:
                return "Cú pháp đăng ký đã tồn tại"
            elif "Cú pháp gia hạn đã tồn tại" in error_msg:
                return "Cú pháp gia hạn đã tồn tại"
            elif "Cú pháp hủy đã tồn tại" in error_msg:
                return "Cú pháp hủy đã tồn tại"
            elif "ID Dịch vụ không tồn tại" in error_msg:
                return "ID Dịch vụ không tồn tại"
            elif "ID Nhân viên không tồn tại" in error_msg:
                return "ID Nhân viên không tồn tại"
            elif "Hình thức thanh toán phải là TRATRUOC hoặc TRASAU" in error_msg:
                return "Hình thức thanh toán phải là TRATRUOC hoặc TRASAU"
            elif "Thời hạn phải là số dương" in error_msg:
                return "Thời hạn phải là số dương"
            elif "Gói cước không tồn tại" in error_msg:
                return "Gói cước không tồn tại"
            # Xử lý lỗi Duplicate entry từ ràng buộc UNIQUE
            if "Duplicate entry" in error_msg:
                if "code" in error_msg:
                    return "Mã gói cước đã tồn tại"
                elif "registration_syntax" in error_msg:
                    return "Cú pháp đăng ký đã tồn tại"
                elif "renewal_syntax" in error_msg:
                    return "Cú pháp gia hạn đã tồn tại"
                elif "cancel_syntax" in error_msg:
                    return "Cú pháp hủy đã tồn tại"
            return f"Không thể cập nhật gói cước ID {plan_id}: {error_msg}"

    @staticmethod
    def lock(plan_id):
        try:
            print("plan_id: ", plan_id)
            result = db_instance.execute(
                "CALL LockPlan(%s)", (plan_id,), fetchone=True, commit=True
            )
            if result and result.get("error"):
                return result["error"]
            return True
        except Exception as e:
            return f"Không thể khóa gói cước ID {plan_id}: {str(e)}"

    @staticmethod
    def search(code, price, is_active, object_type):
        try:
            params = (
                code if code else None,
                float(price) if price else None,
                int(is_active) if is_active is not None else None,
                object_type if object_type else None,
            )
            print("Search params:", params)  # Debug log
            result = db_instance.execute(
                "CALL SearchPlans(%s, %s, %s, %s)", params, fetchall=True
            )
            print("Search result:", result)  # Debug log
            plans = []
            if result and result[0]:  # Kiểm tra result[0] tồn tại
                for row in result[0]:
                    plan = PlanRepository._row_to_plan(row)
                    plans.append(
                        plan.to_dict_plan(
                            duration=row.get("duration", None),
                            object_type=row.get("object_type", None),
                        )
                    )
            return plans
        except Exception as e:
            print("Error in PlanRepository.search:", str(e))  # Debug log
            return {"error": f"Không thể tìm kiếm gói cước: {str(e)}"}

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
            return {"error": f"Không thể lấy danh sách sub-services: {str(e)}"}

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
                service_id = row.get("service_id")
                if service_id:
                    service = ServiceRepository.get_by_id(service_id)
                    plan.service_id = service if service else None
                else:
                    plan.service_id = None
                plan.is_active = (
                    bool(row.get("is_active"))
                    if row.get("is_active") is not None
                    else False
                )
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
                plan.auto_renew = (
                    bool(row.get("auto_renew"))
                    if row.get("auto_renew") is not None
                    else False
                )
                staff_id = row.get("staff_id")
                if staff_id:
                    staff = StaffRepository.get_by_id(staff_id)
                    if isinstance(staff, dict) and "error" in staff:
                        plan.staff_id = None
                    else:
                        plan.staff_id = staff
                else:
                    plan.staff_id = None
                plan.created_at = row.get("created_at")
                plan.updated_at = row.get("updated_at")
                plan.maximum_on_network_call = row.get("maximum_on_network_call")
                plan.ON_SMS_cost = row.get("ON_SMS_cost")
                plan.ON_a_call_cost = row.get("ON_a_call_cost")
                plans.append(plan.to_dict())
            return plans
        except Exception as e:
            return {
                "error": f"Không thể lấy danh sách gói cước theo service_id {service_id}: {str(e)}"
            }

    @staticmethod
    def get_by_plan_id(plan_id):
        try:
            result = db_instance.execute(
                "CALL GetPlanById(%s)", (plan_id,), fetchone=True
            )
            if result:
                return PlanRepository._row_to_plan(result)
            return None
        except Exception as e:
            return {"error": f"Không thể lấy gói cước theo ID {plan_id}: {str(e)}"}

    @staticmethod
    def get_all_codes():
        try:
            result = db_instance.execute(
                "SELECT DISTINCT code FROM plans WHERE is_active = 1", fetchall=True
            )
            return [row["code"] for row in result[0]] if result else []
        except Exception as e:
            return {"error": f"Không thể lấy danh sách mã gói: {str(e)}"}

    @staticmethod
    def _row_to_plan(row):
        plan = Plan()
        #         plan.id = row.get("id")
        #         for key in row:
        #             print("key", key)
        #             if key in ("is_active", "auto_renew"):
        #                 value = row[key]
        #                 setattr(plan, key, bool(value) if value is not None else False)
        #             elif key in ("ON_SMS_cost", "ON_a_call_cost", "price"):
        #                 value = row[key]
        #                 setattr(plan, key, float(value) if value is not None else None)
        #             elif key in ("service_id"):
        #                 value = ServiceRepository.get_by_id(row[key])
        #                 setattr(plan, key, value if value else None)
        #             elif key in ("staff_id"):
        #                 value = StaffRepository.get_by_id(row[key])
        #                 if isinstance(value, dict) and "error" in value:
        #                     setattr(plan, key, None)
        #                 else:
        #                     setattr(plan, key, value)
        #             else:
        #                 print("key", key)
        #                 setattr(plan, key, row[key])

        #             print("data", key, row[key])
        #         print("plan", plan.to_dict_plan())
        #         return plan
        # Gán giá trị từng thuộc tính một cách tường minh
        plan.id = int(row["id"]) if row.get("id") is not None else 0
        plan.code = row.get("code")
        plan.price = float(row["price"]) if row.get("price") is not None else None
        plan.description = row.get("description")

        # Xử lý service_id là object
        try:
            service_id = row.get("service_id")
            plan.service_id = (
                ServiceRepository.get_by_id(service_id).to_dict()
                if service_id
                else None
            )
        except Exception:
            plan.service_id = None

        plan.is_active = (
            bool(row.get("is_active")) if row.get("is_active") is not None else False
        )
        plan.renewal_syntax = row.get("renewal_syntax")
        plan.registration_syntax = row.get("registration_syntax")
        plan.cancel_syntax = row.get("cancel_syntax")
        plan.free_data = (
            int(row["free_data"]) if row.get("free_data") is not None else 0
        )
        plan.free_on_network_a_call = (
            int(row["free_on_network_a_call"])
            if row.get("free_on_network_a_call") is not None
            else 0
        )
        plan.free_on_network_call = (
            int(row["free_on_network_call"])
            if row.get("free_on_network_call") is not None
            else 0
        )
        plan.free_on_network_SMS = (
            int(row["free_on_network_SMS"])
            if row.get("free_on_network_SMS") is not None
            else 0
        )
        plan.free_off_network_a_call = (
            int(row["free_off_network_a_call"])
            if row.get("free_off_network_a_call") is not None
            else 0
        )
        plan.free_off_network_call = (
            int(row["free_off_network_call"])
            if row.get("free_off_network_call") is not None
            else 0
        )
        plan.free_off_network_SMS = (
            int(row["free_off_network_SMS"])
            if row.get("free_off_network_SMS") is not None
            else 0
        )
        plan.auto_renew = (
            bool(row.get("auto_renew")) if row.get("auto_renew") is not None else False
        )

        # Xử lý staff_id là object
        try:
            staff_id = row.get("staff_id")
            staff = StaffRepository.get_by_id(staff_id).to_dict() if staff_id else None
            plan.staff_id = (
                None if isinstance(staff, dict) and "error" in staff else staff
            )
        except Exception:
            plan.staff_id = None

        plan.created_at = row.get("created_at")
        plan.updated_at = row.get("updated_at")
        plan.maximum_on_network_call = (
            int(row["maximum_on_network_call"])
            if row.get("maximum_on_network_call") is not None
            else 0
        )
        plan.ON_SMS_cost = (
            float(row["ON_SMS_cost"]) if row.get("ON_SMS_cost") is not None else None
        )
        plan.ON_a_call_cost = (
            float(row["ON_a_call_cost"])
            if row.get("ON_a_call_cost") is not None
            else None
        )

        return plan

    @staticmethod
    def get_plan_by_subscription_id(subscription_id):
        try:
            result = db_instance.execute(
                "CALL sp_get_plan_by_subscription_id(%s)",
                [subscription_id],
                fetchone=True,
            )
            if not result:
                return None
            return {
                "plan_id": result.get("plan_id"),
                "plan_code": result.get("plan_code"),
                "price": result.get("price"),
                "description": result.get("description"),
                "service_id": result.get("service_id"),
                "free_data": result.get("free_data"),
                "free_on_network_a_call": result.get("free_on_network_a_call"),
                "free_off_network_a_call": result.get("free_off_network_a_call"),
                "free_on_network_call": result.get("free_on_network_call"),
                "free_off_network_call": result.get("free_off_network_call"),
                "free_on_network_SMS": result.get("free_on_network_SMS"),
                "free_off_network_SMS": result.get("free_off_network_SMS"),
                "auto_renew": result.get("auto_renew"),
                "ON_a_call_cost": result.get("ON_a_call_cost"),
                "ON_SMS_cost": result.get("ON_SMS_cost"),
            }
        except Exception as e:
            print(f"[Repository] Lỗi khi gọi SP get_plan_by_subscription_id: {e}")
            return None
