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
    def insert(payment: Payment):
        try:
            # Thực thi stored procedure
            result = db_instance.execute(
                "CALL AddPayment(%s, %s, %s, %s, %s)",
                (
                    payment.subscription_id,
                    payment.total_amount,
                    payment.payment_method,
                    payment.is_paid,
                    payment.due_date,
                ),
                fetchone=True,
                commit=True,
            )

            if not result:
                return {"error": "Không có phản hồi từ stored procedure"}

            # Kiểm tra kết quả từ stored procedure
            if result.get("success") == 1:
                # Giả sử stored procedure trả về id_payment
                id_payment = result.get("id_payment")  # Giả sử bạn nhận id_payment từ kết quả
                return {"success": True, "id_payment": id_payment}  # Trả về id_payment
            else:
                return {"error": result.get("message", "Lỗi không xác định")}

        except Exception as e:
            return {"error": str(e)}

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

    @staticmethod
    def create_full_payment_transaction(plan_code: str, subscriber_id: int):
        try:
            result = db_instance.execute(
                "CALL CreateFullPaymentTransaction(%s, %s)",
                (plan_code, subscriber_id),
                fetchone=True,
                commit=True,
            )
            if result.get("success"):
                return {
                    "success": True,
                    "message": result.get("message"),
                    "subscription_id": result.get("subscription_id"),
                    "payment_id": result.get("payment_id"),
                }
            else:
                return {"success": False, "message": result.get("message")}
        except Exception as e:
            print(f"[Repository] Lỗi khi tạo giao dịch thanh toán đầy đủ: {e}")
            return {"success": False, "message": str(e)}
