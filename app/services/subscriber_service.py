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
            if not phone_number.isdigit() or not (10 <= len(phone_number) <= 11):
                return {"success": False, "message": "Số điện thoại không hợp lệ"}

            # Lấy và chuyển đổi main_balance
            try:
                main_balance = Decimal(data.get("main_balance", 0))
                if main_balance < 0:
                    return {"success": False, "message": "Số dư chính không được nhỏ hơn 0"}
            except:
                return {"success": False, "message": "Số dư chính không hợp lệ"}

            # Kiểm tra và chuyển expiration_date
            expiration_date_str = data.get("expiration_date")
            expiration_date = None
            if expiration_date_str:
                try:
                    expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d")
                    if expiration_date < datetime.now():
                        return {"success": False, "message": "Ngày hết hạn phải lớn hơn hoặc bằng ngày hiện tại"}
                except:
                    return {"success": False, "message": "Định dạng ngày hết hạn không hợp lệ"}

            # Kiểm tra loại thuê bao
            subscriber_type_str = str(data.get("subscriber", "Trả trước")).strip()
            if subscriber_type_str == "TRATRUOC":
                subscriber = "Trả sau"
            elif subscriber_type_str == "TRATRUOC":
                subscriber = "Trả trước"
            else:
                return {"success": False, "message": "Loại thuê bao không hợp lệ"}

            # Kiểm tra customer_id
            try:
                customer_id = int(data.get("customer_id"))
                if customer_id <= 0:
                    return {"success": False, "message": "Customer ID phải lớn hơn 0"}
            except:
                return {"success": False, "message": "Customer ID không hợp lệ"}

            # Kiểm tra chi phí cuộc gọi
            try:
                call_cost = float(data.get("ON_a_call_cost", 0))
                if call_cost < 0:
                    return {"success": False, "message": "Chi phí cuộc gọi không được nhỏ hơn 0"}
            except:
                return {"success": False, "message": "Chi phí cuộc gọi không hợp lệ"}

            # Kiểm tra chi phí SMS
            try:
                sms_cost = float(data.get("ON_SMS_cost", 0))
                if sms_cost < 0:
                    return {"success": False, "message": "Chi phí SMS không được nhỏ hơn 0"}
            except:
                return {"success": False, "message": "Chi phí SMS không hợp lệ"}

            # Tạo đối tượng Subscriber
            new_subscriber = Subscriber(
                phone_number=phone_number,
                main_balance=main_balance,
                expiration_date=expiration_date,
                subscriber=subscriber,
                customer_id=customer_id,
                ON_a_call_cost=call_cost,
                ON_SMS_cost=sms_cost
            )

            # Gọi repository để lưu subscriber vào CSDL
            result = SubscriberRepository.create(new_subscriber)
            if result.get("success"):
                return {"success": True, "message": result.get("message")}
            else:
                return {"success": False, "message": result.get("message")}

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

            subscriber_type = data.get("subscriber", "TRATRUOC").strip()

            # Tạo đối tượng subscriber để update
            subscriber = Subscriber(
                phone_number=phone_number,
                main_balance=main_balance,
                activation_date=None,  # Không thay đổi
                expiration_date=expiration_date,
                is_active=is_active,
                customer_id=customer_id,
                subscriber=subscriber_type,
                warning_date=warning_date,
                account_id=account_id

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
