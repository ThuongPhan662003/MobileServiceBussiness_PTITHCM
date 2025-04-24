from app.database import db_instance
from app.models.voucher import Voucher
from app.services.staff_service import StaffService


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
                    voucher.staff_id = StaffService.get_staff_by_id(staff_id)
                else:
                    voucher.staff_id = None

                voucher.packages = row.get("packages")

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
                voucher.conandpromo = result.get("conandpromo")
                voucher.start_date = result.get("start_date")
                voucher.end_date = result.get("end_date")
                voucher.usage_limit = result.get("usage_limit")
                voucher.remaining_count = result.get("remaining_count")
                voucher.is_active = result.get("is_active")
                voucher.staff_id = result.get("staff_id")
                voucher.packages = result.get("packages")
                return voucher
            return None
        except Exception as e:
            print(f"Lỗi khi lấy voucher theo ID: {e}")
            return None

    @staticmethod
    def insert(voucher: Voucher):
        try:
            result = db_instance.execute(
                "CALL AddVoucher(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    voucher.code,
                    voucher.description,
                    voucher.conandpromo,
                    voucher.start_date,
                    voucher.end_date,
                    voucher.usage_limit,
                    voucher.remaining_count,
                    voucher.is_active,
                    voucher.staff_id,
                    voucher.packages,
                ),
                fetchone=True,
            )
            if result.get("error"):
                return result.get("error")
            return True

        except Exception as e:
            return {"error": f"Lỗi khi thêm voucher: {e}"}

    @staticmethod
    def update(voucher_id, voucher: Voucher):
        try:
            result = db_instance.execute(
                "CALL UpdateVoucher(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    voucher_id,
                    voucher.code,
                    voucher.description,
                    voucher.conandpromo,
                    voucher.start_date,
                    voucher.end_date,
                    voucher.usage_limit,
                    voucher.remaining_count,
                    voucher.is_active,
                    voucher.staff_id,
                    voucher.packages,
                ),
                fetchone=True,
            )
            if result.get("error"):
                return result.get("error")
            return True
        except Exception as e:
            return {"error": f"Lỗi khi cập nhật voucher: {e}"}

    @staticmethod
    def delete(voucher_id):
        try:
            result = db_instance.execute(
                "CALL DeleteVoucher(%s)", (voucher_id,), fetchone=True
            )
            if result.get("error"):
                return result.get("error")
            return True
        except Exception as e:
            return {"error": f"Lỗi khi xóa voucher: {e}"}
