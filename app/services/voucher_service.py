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
            # Ép kiểu từ chuỗi → datetime
            start_date_str = data.get("start_date")
            end_date_str = data.get("end_date")

            start_date = (
                datetime.strptime(start_date_str, "%Y-%m-%d")
                if start_date_str
                else None
            )
            end_date = (
                datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
            )
            voucher = Voucher(
                id=data.get("id"),
                code=data.get("code"),
                description=data.get("description"),
                conandpromo=data.get("conandpromo"),
                start_date=start_date,
                end_date=end_date,
                usage_limit=data.get("usage_limit"),
                remaining_count=data.get("remaining_count", 0),
                is_active=True if data.get("is_active") else False,
                staff_id=session["staff_id"],
                packages=data.get("packages"),
            )
            result = VoucherRepository.update(voucher_id, voucher)
            print("result", result)
            if result and result["success"]:
                return result
            else:
                print("lỗi")
                return result
        except Exception as e:
            print("exception")
            return {"error": str(e)}

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
