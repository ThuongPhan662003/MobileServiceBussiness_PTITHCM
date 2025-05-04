from datetime import datetime
from decimal import Decimal

from flask import jsonify

from app.models.subscriber import Subscriber
from app.repositories.account_repository import AccountRepository
from app.repositories.subscriber_repository import SubscriberRepository


class SubscriberService:
    @staticmethod
    def get_all_subscribers():
        return SubscriberRepository.get_all()

    @staticmethod
    def get_subscriber_by_id(subscriber_id):
        return SubscriberRepository.get_by_id(subscriber_id)

    @staticmethod
    def get_by_account_id(account_id: int):
        return SubscriberRepository.get_by_account_id(account_id)

    @staticmethod
    def create_subscriber(data: dict):
        try:
            print("Dữ liệu nhận được:", data)

            # Kiểm tra số điện thoại
            phone_number = data.get("phone_number")
            print(phone_number)
            if not phone_number:
                return {"success": False, "message": "Số điện thoại không được để trống"}
            account_result = AccountRepository.create_account_from_phone(phone_number)
            account_id = account_result
            print("Kết quả từ AccountRepository:", account_result)
            data["account_id"] = account_id
            # Lấy và chuyển đổi các thông tin khác
            main_balance = Decimal(data.get("main_balance", 0))
            expiration_date_str = data.get("expiration_date")
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d") if expiration_date_str else None

            # Chuyển đổi subscriber thành chuỗi hợp lệ ("Trả sau" hoặc "Trả trước")
            subscriber_type_str = str(data.get("subscriber", "Trả trước")).strip()
            if subscriber_type_str == "Trả sau":
                subscriber = "Trả sau"  # Để kiểu chuỗi "Trả sau"
            elif subscriber_type_str == "Trả trước":
                subscriber = "Trả trước"  # Để kiểu chuỗi "Trả trước"
            else:
                return {"success": False, "message": "Loại thuê bao không hợp lệ"}

            # Chuyển customer_id về kiểu int
            try:
                customer_id = int(data.get("customer_id"))
            except ValueError:
                return {"success": False, "message": "Customer ID không hợp lệ"}

            # Lấy thêm chi phí gọi và tin nhắn
            call_cost = float(data.get("ON_a_call_cost", 0))
            sms_cost = float(data.get("ON_SMS_cost", 0))

            # Tạo đối tượng Subscriber
            new_subscriber = Subscriber(
                phone_number=phone_number,
                main_balance=main_balance,
                expiration_date=expiration_date,
                subscriber=subscriber,  # Truyền vào chuỗi "Trả sau" hoặc "Trả trước"
                customer_id=customer_id,
                account_id=account_id,
                ON_a_call_cost=call_cost,
                ON_SMS_cost=sms_cost
            )

            # Gọi repository để lưu subscriber vào CSDL
            result = SubscriberRepository.create(new_subscriber)
            if result is True:
                return {"success": True, "message": "Tạo thuê bao thành công"}
            else:
                return {"success": False, "message": str(result)}

        except Exception as e:
            print(f"❌ Lỗi khi tạo subscriber: {e}")
            return {"success": False, "message": str(e)}

    @staticmethod
    def update_subscriber(subscriber_id, data: dict):
        try:
            phone_number = data.get("phone_number")
            if not phone_number or not phone_number.isdigit():
                return {"error": "Số điện thoại không hợp lệ"}

            main_balance = Decimal(data.get("main_balance", 0))
            customer_id = int(data.get("customer_id"))
            account_id = int(data.get("account_id"))

            expiration_date_str = data.get("expiration_date")
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date() if expiration_date_str else None

            warning_date_str = data.get("warning_date")
            warning_date = datetime.strptime(warning_date_str, "%Y-%m-%d") if warning_date_str else None

            is_active = str(data.get("is_active", "true")).lower() == "true"
            is_messaged = str(data.get("is_messaged", "false")).lower() == "true"

            subscriber_type = data.get("subscriber_type", "Trả trước").strip()

            # Tạo đối tượng subscriber để update
            subscriber = Subscriber(
                phone_number=phone_number,
                main_balance=main_balance,
                activation_date=None,  # Không thay đổi
                expiration_date=expiration_date,
                is_active=is_active,
                customer_id=customer_id,
                warning_date=warning_date,
                is_messaged=is_messaged,
                account_id=account_id,
                subscriber_type=subscriber_type
            )

            result = SubscriberRepository.update(subscriber_id, subscriber)
            return {"success": True} if result is True else {"error": result}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_subscriber(subscriber_id):
        try:
            result = SubscriberRepository.delete(subscriber_id)
            return {"success": True} if result is True else {"error": result}
        except Exception as e:
            return {"error": str(e)}
