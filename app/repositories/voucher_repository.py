from flask import json
from app.database import db_instance
from app.models.voucher import Voucher


from app.repositories.staff_repository import StaffRepository


class VoucherRepository:

    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_vouchers", fetchall=True)
            vouchers = []

            for row in result[0]:
                voucher = Voucher()
                voucher.id = row.get("id")
                voucher.code = row.get("code")
                voucher.description = row.get("description")
                voucher.conandpromo = row.get("conandpromo")
                voucher.start_date = row.get("start_date")
                voucher.end_date = row.get("end_date")
                voucher.usage_limit = row.get("usage_limit")
                voucher.remaining_count = row.get("remaining_count")
                voucher.is_active = True if row.get("is_active") else False

                # Gán staff_id là đối tượng Staff thay vì số nguyên
                staff_id = row.get("staff_id")
                if staff_id:

                    voucher.staff_id = StaffRepository.get_by_id(staff_id)

                else:
                    voucher.staff_id = None

                voucher.packages = row.get("packages")
                print("voucher------------------", voucher.to_dict)
                vouchers.append(voucher.to_dict())
                print(voucher)

            return vouchers

        except Exception as e:
            print(f"Lỗi khi lấy danh sách voucher: {e}")
            return []

    @staticmethod
    def get_by_id(voucher_id):
        try:
            result = db_instance.execute(
                "CALL GetVoucherById(%s)", (voucher_id,), fetchone=True
            )
            if result:
                voucher = Voucher()
                voucher.id = result.get("id")
                voucher.code = result.get("code")
                voucher.description = result.get("description")
                print("conandpromo", result.get("conandpromo"))
                voucher.conandpromo = result.get("conandpromo")
                voucher.start_date = result.get("start_date")
                voucher.end_date = result.get("end_date")
                voucher.usage_limit = result.get("usage_limit")
                voucher.remaining_count = result.get("remaining_count")
                voucher.is_active = True if result.get("is_active") else False
                voucher.staff_id = StaffRepository.get_by_id(result.get("staff_id"))
                voucher.packages = result.get("packages")
                return voucher
            return None
        except Exception as e:
            print(f"Lỗi khi lấy voucher theo ID: {e}")
            return None

    @staticmethod
    def insert(voucher: dict):
        try:
            # Xử lý trường hợp conandpro là dict → chuỗi JSON
            # conandpromo = voucher.get("conandpro", "")
            # if isinstance(conandpromo, dict):
            #     conandpromo = json.dumps(conandpromo, ensure_ascii=False)
            #     print("dict", conandpromo)
            # elif not isinstance(conandpromo, str):
            #     conandpromo = str(conandpromo)
            print("str", type(voucher.get("conandpromo")))

            # Gọi stored procedure AddVoucher
            result = db_instance.execute(
                "CALL AddVoucher(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    voucher.get("code"),
                    voucher.get("description"),
                    json.dumps(voucher.get("conandpromo"), ensure_ascii=False),
                    voucher.get("start_date"),
                    voucher.get("end_date"),
                    voucher.get("usage_limit"),
                    voucher.get("remaining_count"),
                    voucher.get("is_active"),
                    voucher.get("staff_id").get("id"),
                    voucher.get("packages"),
                ),
                fetchone=True,
                commit=True,
            )

            # Xử lý kết quả trả về từ stored procedure
            if result.get("success"):
                return {
                    "success": True,
                    "error": False,
                    "message": result.get("message", "Thêm voucher thành công."),
                }
            else:
                return {
                    "success": False,
                    "error": True,
                    "message": result.get("message", "Không thể thêm voucher."),
                }

        except Exception as e:
            return {
                "success": False,
                "error": True,
                "message": f"Đã xảy ra lỗi hệ thống khi thêm voucher: {str(e)}",
            }

    @staticmethod
    def update(voucher_id, voucher: dict):
        try:
            result = db_instance.execute(
                "CALL UpdateVoucher(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    voucher_id,
                    voucher.get("code"),
                    voucher.get("description"),
                    voucher.get("conandpromo"),
                    voucher.get("start_date"),
                    voucher.get("end_date"),
                    voucher.get("is_active"),
                    voucher.get("packages"),
                ),
                fetchone=True,
                commit=True,
            )
            print("resultd", result)
            if result is None:
                return {
                    "success": False,
                    "message": "Không nhận được phản hồi từ stored procedure.",
                    "data": None,
                }

            message = result.get("message", "Không có thông báo.")
            # Xử lý kết quả có 'success' hoặc 'error'
            if result.get("success"):
                return {"success": True, "message": message, "data": result}
            else:
                return {"success": False, "message": message, "data": result}

        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi cập nhật voucher: {str(e)}",
                "data": None,
            }

    @staticmethod
    def delete(voucher_id):
        try:
            result = db_instance.execute(
                "CALL DeleteVoucher(%s)", (voucher_id,), fetchone=True, commit=True
            )
            if result.get("error"):
                return result.get("error")
            return True
        except Exception as e:
            return {"error": f"Lỗi khi xóa voucher: {e}"}
