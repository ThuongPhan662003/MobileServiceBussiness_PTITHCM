from app.repositories.paymentdetail_repository import PaymentDetailRepository
from app.models.paymentdetail import PaymentDetail


class PaymentDetailService:
    @staticmethod
    def get_all_payment_details():
        return PaymentDetailRepository.get_all()

    @staticmethod
    def get_payment_detail_by_id(detail_id):
        return PaymentDetailRepository.get_by_id(detail_id)

    @staticmethod
    def create_payment_detail(data: dict):
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
            result = PaymentDetailRepository.insert(detail)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

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