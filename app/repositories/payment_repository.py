from app.database import db_instance
from app.models.payment import Payment
import logging

logger = logging.getLogger(__name__)


class PaymentRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_payments", fetchall=True)
            logger.debug(f"Raw result from db_instance: {result}")

            # Xử lý cấu trúc dữ liệu
            if not result:
                logger.warning("No data returned from v_payments")
                return []

            # Nếu result là [[{...}, {...}]], lấy result[0]
            data = (
                result[0]
                if isinstance(result, list)
                and len(result) == 1
                and isinstance(result[0], list)
                else result
            )
            payments = []

            for row in data:
                # Chỉ xử lý nếu row là dictionary
                if not isinstance(row, dict):
                    logger.warning(f"Skipping invalid row (not a dictionary): {row}")
                    continue

                logger.debug(f"Processing row: {row}")
                payment = Payment()
                payment.id = row.get("id", None)
                payment.subscription_id = row.get("subscription_id", None)
                payment.payment_date = row.get("payment_date", None)
                total_amount = row.get("total_amount")
                payment.total_amount = (
                    float(total_amount) if total_amount is not None else 0.0
                )
                payment.payment_method = row.get("payment_method", None)
                payment.is_paid = bool(row.get("is_paid", False))
                payment.due_date = row.get("due_date", None)
                payments.append(payment.to_dict())
                logger.debug(f"Processed payment: {payment.to_dict()}")
            logger.info(f"Retrieved {len(payments)} payments from v_payments")
            return payments
        except Exception as e:
            logger.error(f"Lỗi khi lấy danh sách payment: {e}")
            return []

    @staticmethod
    def get_by_id(payment_id):
        try:
            result = db_instance.execute(
                "SELECT * FROM v_payments WHERE id = %s", (payment_id,), fetchone=True
            )
            logger.debug(f"Raw result for get_by_id: {result}")
            if result:
                payment = Payment()
                payment.id = result.get("id", None)
                payment.subscription_id = result.get("subscription_id", None)
                payment.payment_date = result.get("payment_date", None)
                total_amount = result.get("total_amount")
                payment.total_amount = (
                    float(total_amount) if total_amount is not None else 0.0
                )
                payment.payment_method = result.get("payment_method", None)
                payment.is_paid = bool(result.get("is_paid", False))
                payment.due_date = result.get("due_date", None)
                return payment
            return None
        except Exception as e:
            logger.error(f"Lỗi khi lấy payment theo ID: {e}")
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
                logger.error(f"Lỗi khi thêm payment: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            logger.error(f"Lỗi khi thêm payment: {e}")
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
                logger.error(f"Lỗi khi cập nhật payment: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            logger.error(f"Lỗi khi cập nhật payment: {e}")
            return False

    @staticmethod
    def delete(payment_id):
        try:
            result = db_instance.execute(
                "CALL DeletePayment(%s)", (payment_id,), fetchone=True
            )
            if result.get("error"):
                logger.error(f"Lỗi khi xóa payment: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            logger.error(f"Lỗi khi xóa payment: {e}")
            return False

    @staticmethod
    def search_payments(
        subscription_id=None, payment_date=None, payment_method=None, is_paid=None
    ):
        try:
            query = "SELECT * FROM v_payments WHERE 1=1"
            params = []
            if subscription_id:
                query += " AND subscription_id = %s"
                params.append(subscription_id)
            if payment_date:
                query += " AND DATE(payment_date) = %s"
                params.append(payment_date)
            if (
                payment_method and payment_method != "Tất cả"
            ):  # Chỉ lọc nếu không phải "Tất cả"
                if payment_method not in ["Paypal", "Main balance"]:
                    logger.warning(
                        f"Invalid payment_method: {payment_method}, ignoring filter"
                    )
                else:
                    query += " AND payment_method = %s"
                    params.append(payment_method)
            if is_paid is not None:
                query += " AND is_paid = %s"
                params.append(is_paid)

            result = db_instance.execute(query, tuple(params), fetchall=True)
            logger.debug(f"Raw result from search: {result}")
            data = (
                result[0]
                if isinstance(result, list)
                and len(result) == 1
                and isinstance(result[0], list)
                else result
            )
            payments = []
            for row in data:
                if not isinstance(row, dict):
                    logger.warning(f"Skipping invalid row (not a dictionary): {row}")
                    continue
                payment = Payment()
                payment.id = row.get("id", None)
                payment.subscription_id = row.get("subscription_id", None)
                payment.payment_date = row.get("payment_date", None)
                total_amount = row.get("total_amount")
                payment.total_amount = (
                    float(total_amount) if total_amount is not None else 0.0
                )
                payment.payment_method = row.get("payment_method", None)
                payment.is_paid = bool(row.get("is_paid", False))
                payment.due_date = row.get("due_date", None)
                payments.append(payment.to_dict())
            logger.info(f"Retrieved {len(payments)} payments from search")
            return payments
        except Exception as e:
            logger.error(f"Lỗi khi tìm kiếm payment: {e}")
            return []

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
