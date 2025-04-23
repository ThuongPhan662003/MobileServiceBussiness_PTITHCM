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
    def create_subscriber(data: dict):
        try:
            # In ra dữ liệu nhận được từ client
            print("Dữ liệu nhận được:", data)

            phone_number = data.get("phone_number")
            if not phone_number:
                return {"error": "Số điện thoại không được để trống"}

            # Gọi stored procedure tạo tài khoản từ số điện thoại
            account_result = AccountRepository.create_account_from_phone(phone_number)
            print("Kết quả trả về từ stored procedure:", account_result)
            if isinstance(account_result, dict) and "error" in account_result:
                return {"error": account_result["error"]}
            account_id = account_result  # Lấy account_id từ kết quả stored procedure

            # Cập nhật lại account_id vào dữ liệu
            data["account_id"] = account_id

            # Chuyển đổi các dữ liệu khác
            main_balance = Decimal(data.get("main_balance", 0))
            expiration_date_str = data.get("expiration_date")
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d") if expiration_date_str else None

            # Kiểm tra và ép kiểu subscriber_type thành chuỗi
            subscriber_type_str = str(data.get("subscriber_type", "Trả trước")).strip()

            # Kiểm tra nếu subscriber_type là "Trả sau" hoặc "Trả trước"
            subscriber = True if subscriber_type_str == "Trả sau" else False

            customer_id = int(data.get("customer_id"))

            # Tạo đối tượng Subscriber
            new_subscriber = Subscriber(
                phone_number=phone_number,
                main_balance=main_balance,
                expiration_date=expiration_date,
                subscriber_type=subscriber_type_str,  # Gán chuỗi subscriber_type vào đây
                customer_id=customer_id,
                account_id=account_id  # Gán account_id vào đối tượng subscriber
            )

            # ✅ In ra thông tin trước khi gọi stored procedure
            print("Chuẩn bị thêm subscriber với dữ liệu:")
            print(new_subscriber.to_dict())

            # Gọi phương thức create từ repository
            result = SubscriberRepository.create(new_subscriber)

            # In kết quả trả về từ repository
            print("Kết quả trả về từ repository:", result)

            # Kiểm tra kết quả trả về từ repository
            if result is True:
                return jsonify({"success": True, "message": "Thêm subscriber thành công"})
            else:
                return jsonify({"error": result})  # Trả về lỗi nếu có

        except Exception as e:
         return jsonify({"error": str(e)})

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
