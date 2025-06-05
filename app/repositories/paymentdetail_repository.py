from app.database import db_instance
from app.models.paymentdetail import PaymentDetail


class PaymentDetailRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute(
                "SELECT * FROM v_payment_details", fetchall=True
            )
            details = []

            for row in result[0]:
                detail = PaymentDetail()
                detail.id = row.get("id")
                detail.payment_id = row.get("payment_id")
                detail.free_data = row.get("free_data")
                detail.free_ON_a_call = row.get("free_ON_a_call")
                detail.free_OffN_a_call = row.get("free_OffN_a_call")
                detail.free_ON_call = row.get("free_ON_call")
                detail.free_OffN_call = row.get("free_OffN_call")
                detail.free_ON_SMS = row.get("free_ON_SMS")
                detail.free_OffN_SMS = row.get("free_OffN_SMS")
                detail.ON_a_call_cost = row.get("ON_a_call_cost")
                detail.ON_SMS_cost = row.get("ON_SMS_cost")
                details.append(detail)

            return details
        except Exception as e:
            print(f"Lỗi khi lấy danh sách payment detail: {e}")
            return []

    @staticmethod
    def get_by_id(detail_id):
        try:
            result = db_instance.execute(
                "CALL GetPaymentDetailById(%s)", (detail_id,), fetchone=True
            )
            if result:
                detail = PaymentDetail()
                detail.id = result.get("id")
                detail.payment_id = result.get("payment_id")
                detail.free_data = result.get("free_data")
                detail.free_ON_a_call = result.get("free_ON_a_call")
                detail.free_OffN_a_call = result.get("free_OffN_a_call")
                detail.free_ON_call = result.get("free_ON_call")
                detail.free_OffN_call = result.get("free_OffN_call")
                detail.free_ON_SMS = result.get("free_ON_SMS")
                detail.free_OffN_SMS = result.get("free_OffN_SMS")
                detail.ON_a_call_cost = result.get("ON_a_call_cost")
                detail.ON_SMS_cost = result.get("ON_SMS_cost")
                return detail
            return None
        except Exception as e:
            print(f"Lỗi khi lấy payment detail theo ID: {e}")
            return None

    @staticmethod
    def insert(payment_detail_data: dict):
        try:
            print("Fdsfs", payment_detail_data)

            # Thực thi câu lệnh SQL để chèn thông tin vào payment_detail

            result = db_instance.execute(
                "CALL AddPaymentDetail(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    payment_detail_data["payment_id"],
                    payment_detail_data["free_data"],
                    payment_detail_data["free_ON_a_call"],
                    payment_detail_data["free_OffN_a_call"],
                    payment_detail_data["free_ON_call"],
                    payment_detail_data["free_OffN_call"],
                    payment_detail_data["free_ON_SMS"],
                    payment_detail_data["free_OffN_SMS"],
                    payment_detail_data["ON_a_call_cost"],
                    payment_detail_data["ON_SMS_cost"],
                ),
                commit=True,
                fetchone=True,  # ⚠️ Đây là lệnh INSERT nên không dùng fetchone
            )
            if result and result.get("success"):
                return {
                    "success": True,
                    "error": None,
                    "message": result.get("message", "Thêm payment detail thành công."),
                    "data": payment_detail_data,
                }
            else:
                return {
                    "success": False,
                    "error": result.get("message", "Thêm payment detail thất bại."),
                    "message": result.get("message", "Thêm payment detail thất bại."),
                    "data": None,
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Lỗi ngoại lệ khi thêm payment detail.",
                "data": None,
            }

    @staticmethod
    def update(detail_id, data: PaymentDetail):
        try:
            result = db_instance.execute(
                "CALL UpdatePaymentDetail(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    detail_id,
                    data.payment_id,
                    data.free_data,
                    data.free_ON_a_call,
                    data.free_OffN_a_call,
                    data.free_ON_call,
                    data.free_OffN_call,
                    data.free_ON_SMS,
                    data.free_OffN_SMS,
                    data.ON_a_call_cost,
                    data.ON_SMS_cost,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật payment detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật payment detail: {e}")
            return False

    @staticmethod
    def delete(detail_id):
        try:
            result = db_instance.execute(
                "CALL DeletePaymentDetail(%s)", (detail_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa payment detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa payment detail: {e}")
            return False

    @staticmethod
    def get_by_payment_id(payment_id):
        try:
            result = db_instance.execute(
                "SELECT * FROM v_payment_details WHERE payment_id = %s",
                (payment_id,),
                fetchall=True,
            )
            details = []
            for row in result[0]:
                detail = PaymentDetail()
                detail.id = row.get("id")
                detail.payment_id = row.get("payment_id")
                detail.free_data = row.get("free_data")
                detail.free_ON_a_call = row.get("free_on_a_call")
                detail.free_OffN_a_call = row.get("free_offn_a_call")
                detail.free_ON_call = row.get("free_on_call")
                detail.free_OffN_call = row.get("free_offn_call")
                detail.free_ON_SMS = row.get("free_on_sms")
                detail.free_OffN_SMS = row.get("free_offn_sms")
                detail.ON_a_call_cost = row.get("on_a_call_cost")
                detail.ON_SMS_cost = row.get("on_sms_cost")
                details.append(detail)
            return details
        except Exception as e:
            print(f"Lỗi khi lấy payment detail theo payment_id: {e}")
            return []
