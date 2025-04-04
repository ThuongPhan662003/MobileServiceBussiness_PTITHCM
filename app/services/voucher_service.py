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
            voucher = Voucher(
                code=data.get("code"),
                description=data.get("description"),
                conandpromo=data.get("conandpromo"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
                usage_limit=data.get("usage_limit"),
                remaining_count=data.get("remaining_count", 0),
                is_active=data.get("is_active", True),
                staff_id=data.get("staff_id"),
                packages=data.get("packages"),
            )
            result = VoucherRepository.insert(voucher)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_voucher(voucher_id, data: dict):
        try:
            voucher = Voucher(
                code=data.get("code"),
                description=data.get("description"),
                conandpromo=data.get("conandpromo"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
                usage_limit=data.get("usage_limit"),
                remaining_count=data.get("remaining_count", 0),
                is_active=data.get("is_active", True),
                staff_id=data.get("staff_id"),
                packages=data.get("packages"),
            )
            result = VoucherRepository.update(voucher_id, voucher)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
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
