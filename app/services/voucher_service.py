from datetime import datetime
from flask import session
from app.repositories.voucher_repository import VoucherRepository
from app.models.voucher import Voucher


class VoucherService:
    @staticmethod
    def get_all_vouchers():
        return VoucherRepository.get_all()

    @staticmethod
    def get_voucher_by_id(voucher_id):
        return VoucherRepository.get_by_id(voucher_id)

    @staticmethod
    def create_voucher(data: dict):
        try:
            # In ra dữ liệu để debug nếu cần
            print("[DEBUG] Dữ liệu đầu vào create_voucher:", data)

            # Gọi hàm insert trong repository
            result = VoucherRepository.insert(data)

            # Xử lý kết quả trả về
            if result.get("success"):
                return {
                    "success": True,
                    "error": False,
                    "message": result.get("message", "Thêm voucher thành công."),
                }
            else:
                print("[DEBUG] Insert voucher thất bại:", result)
                return {
                    "success": False,
                    "error": True,
                    "message": result.get("message", "Không thể thêm voucher."),
                }

        except Exception as e:
            print("[ERROR] Exception trong create_voucher:", str(e))
            return {
                "success": False,
                "error": True,
                "message": f"Lỗi trong quá trình tạo voucher: {str(e)}",
            }

    @staticmethod
    def update_voucher(voucher_id, data: dict):
        try:
            # Gọi tới repository xử lý update
            result = VoucherRepository.update(voucher_id, data)
            print("resultdddd:", result)

            if result.get("success"):
                return {
                    "success": True,
                    "message": result.get("message", "Cập nhật thành công."),
                    "data": result.get("data", {}),
                }
            else:
                print("Cập nhật voucher thất bại:", result)
                return {
                    "success": False,
                    "message": result.get("message", "Cập nhật thất bại."),
                    "data": result.get("data", {}),
                }

        except Exception as e:
            print("Exception khi cập nhật voucher:", str(e))
            return {
                "success": False,
                "message": f"Lỗi hệ thống: {str(e)}",
                "data": None,
            }

    @staticmethod
    def delete_voucher(voucher_id):
        try:
            result = VoucherRepository.delete(voucher_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
