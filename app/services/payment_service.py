from app.repositories.payment_repository import PaymentRepository
from app.models.payment import Payment


class PaymentService:
    @staticmethod
    def get_all_payments():
        return PaymentRepository.get_all()

    @staticmethod
    def get_payment_by_id(payment_id):
        return PaymentRepository.get_by_id(payment_id)

    @staticmethod
    def create_payment(data: dict):
        try:
            payment = Payment(
                subscription_id=data.get("subscription_id"),
                total_amount=data.get("total_amount"),
                payment_method=data.get("payment_method"),
                is_paid=data.get("is_paid", False),
                due_date=data.get("due_date"),
            )
            result = PaymentRepository.insert(payment)
            if result is True:
                return {"success": True, "payment_id": result["payment_id"]}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_payment(payment_id, data: dict):
        try:
            payment = Payment(
                subscription_id=data.get("subscription_id"),
                payment_date=data.get("payment_date"),
                total_amount=data.get("total_amount"),
                payment_method=data.get("payment_method"),
                is_paid=data.get("is_paid", False),
                due_date=data.get("due_date"),
            )
            result = PaymentRepository.update(payment_id, payment)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_payment(payment_id):
        try:
            result = PaymentRepository.delete(payment_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def create_transaction(plan_code: str, subscriber_id: int):
        return PaymentRepository.create_full_payment_transaction(
            plan_code, subscriber_id
        )

    @staticmethod
    def search_payments(
        subscription_id=None, payment_date=None, payment_method=None, is_paid=None
    ):
        return PaymentRepository.search_payments(
            subscription_id, payment_date, payment_method, is_paid
        )
