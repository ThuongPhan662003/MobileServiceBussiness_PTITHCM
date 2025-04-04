from app.database import db_instance
from app.models.payment import Payment


class PaymentRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_payments", fetchall=True)
            payments = []

            for row in result:
                payment = Payment()
                payment.id = row.get("id")
                payment.subscription_id = row.get("subscription_id")
                payment.payment_date = row.get("payment_date")
                payment.total_amount = row.get("total_amount")
                payment.payment_method = row.get("payment_method")
                payment.is_paid = row.get("is_paid")
                payment.due_date = row.get("due_date")
                payments.append(payment.to_dict())

            return payments
        except Exception as e:
            print(f"Lỗi khi lấy danh sách payment: {e}")
            return []

    @staticmethod
    def get_by_id(payment_id):
        try:
            result = db_instance.execute(
                "CALL GetPaymentById(%s)", (payment_id,), fetchone=True
            )
            if result:
                payment = Payment()
                payment.id = result.get("id")
                payment.subscription_id = result.get("subscription_id")
                payment.payment_date = result.get("payment_date")
                payment.total_amount = result.get("total_amount")
                payment.payment_method = result.get("payment_method")
                payment.is_paid = result.get("is_paid")
                payment.due_date = result.get("due_date")
                return payment
            return None
        except Exception as e:
            print(f"Lỗi khi lấy payment theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Payment):
        try:
            result = db_instance.execute(
                "CALL AddPayment(%s, %s, %s, %s, %s, %s)",
                (
                    data.subscription_id,
                    data.payment_date,
                    data.total_amount,
                    data.payment_method,
                    data.is_paid,
                    data.due_date,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm payment: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm payment: {e}")
            return False

    @staticmethod
    def update(payment_id, data: Payment):
        try:
            result = db_instance.execute(
                "CALL UpdatePayment(%s, %s, %s, %s, %s, %s, %s)",
                (
                    payment_id,
                    data.subscription_id,
                    data.payment_date,
                    data.total_amount,
                    data.payment_method,
                    data.is_paid,
                    data.due_date,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật payment: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật payment: {e}")
            return False

    @staticmethod
    def delete(payment_id):
        try:
            result = db_instance.execute(
                "CALL DeletePayment(%s)", (payment_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa payment: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa payment: {e}")
            return False
