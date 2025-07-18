from app.repositories.payment_repository import PaymentRepository
from app.repositories.paymentdetail_repository import PaymentDetailRepository
from app.models.paymentdetail import PaymentDetail
from app.repositories.plan_repository import PlanRepository


class PaymentDetailService:
    @staticmethod
    def get_all_payment_details():
        return PaymentDetailRepository.get_all()

    @staticmethod
    def get_payment_detail_by_id(detail_id):
        return PaymentDetailRepository.get_by_id(detail_id)

    @staticmethod
    def create_payment_detail(payment_id: int, plan_id: int):
        try:
            # Lấy thông tin từ bảng plan
            plan = PlanRepository.get_by_id(plan_id)
            if not plan:
                return {
                    "success": False,
                    "error": "Không tìm thấy thông tin gói cước",
                    "message": "Không tìm thấy thông tin gói cước",
                    "data": None,
                }

            # Chuẩn bị dữ liệu để chèn vào payment_detail
            payment_detail_data = {
                "payment_id": payment_id,
                "free_data": plan.free_data,
                "free_ON_a_call": plan.free_on_network_a_call,
                "free_OffN_a_call": plan.free_off_network_a_call,
                "free_ON_call": plan.free_on_network_call,
                "free_OffN_call": plan.free_off_network_call,
                "free_ON_SMS": plan.free_on_network_SMS,
                "free_OffN_SMS": plan.free_off_network_SMS,
                "ON_a_call_cost": plan.ON_a_call_cost,
                "ON_SMS_cost": plan.ON_SMS_cost,
            }

            # Bảo vệ nếu có giá trị None
            payment_detail_data = {
                key: (value if value is not None else None)
                for key, value in payment_detail_data.items()
            }

            # Gọi insert từ repository
            result = PaymentDetailRepository.insert(payment_detail_data)

            if result.get("success"):
                return {
                    "success": True,
                    "error": None,
                    "message": "Thêm thông tin payment detail thành công",
                    "data": payment_detail_data,
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Không thể thêm payment detail"),
                    "message": result.get("message", "Không thể thêm payment detail"),
                    "data": None,
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Lỗi ngoại lệ khi tạo payment detail",
                "data": None,
            }

    @staticmethod
    def update_payment_detail(detail_id, data: dict):
        try:
            detail = PaymentDetail(
                payment_id=data.get("payment_id"),
                free_data=data.get("free_data"),
                free_ON_a_call=data.get("free_ON_a_call"),
                free_OffN_a_call=data.get("free_OffN_a_call"),
                free_ON_call=data.get("free_ON_call"),
                free_OffN_call=data.get("free_OffN_call"),
                free_ON_SMS=data.get("free_ON_SMS"),
                free_OffN_SMS=data.get("free_OffN_SMS"),
                ON_a_call_cost=data.get("ON_a_call_cost"),
                ON_SMS_cost=data.get("ON_SMS_cost"),
            )
            result = PaymentDetailRepository.update(detail_id, detail)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_payment_detail(detail_id):
        try:
            result = PaymentDetailRepository.delete(detail_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_by_payment_id(payment_id):
        return PaymentDetailRepository.get_by_payment_id(payment_id)
