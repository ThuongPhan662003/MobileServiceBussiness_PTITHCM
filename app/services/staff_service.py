import re
from app.repositories.staff_repository import StaffRepository
from app.models.staff import Staff
from datetime import datetime
from app.viewmodels.staff_view_model import StaffViewModel


class StaffService:
    @staticmethod
    def get_all_staffs():
        return StaffRepository.get_all()

    @staticmethod
    def get_staff_by_id(staff_id):
        return StaffRepository.get_by_id(staff_id)

    @staticmethod
    def get_staff_by_account_id(account_id):
        return StaffRepository.get_by_account_id(account_id)

    # @staticmethod
    # def create_staff(data: dict):
    # try:
    # birthday_str = data.get("birthday")
    # birthday = datetime.strptime(birthday_str, "%Y-%m-%d") if birthday_str else None

    # staff_model = Staff(
    # full_name=data.get("full_name"),
    # card_id=data.get("card_number"),
    # phone=data.get("phone"),
    # email=data.get("email"),
    # gender=data.get("gender"),
    # birthday=birthday,

    # )

    # staff = StaffViewModel(
    # staff_model,
    # role_name=data.get("role_name"),
    # username=data.get("username"),
    # password=data.get("password")
    # )
    # print(staff)
    # result = StaffRepository.insert(staff)
    # if result is True:
    # return {"success": True}
    # else:
    # return {"error": result}

    # except Exception as e:
    # return {"error": str(e)}

    @staticmethod
    def create_staff(data: dict):
        try:
            # Check required fields
            required_fields = [
                "full_name",
                "card_id",
                "phone",
                "email",
                "birthday",
                "gender",
                "role_name",
                "username",
                "password",
            ]
            for field in required_fields:
                if not data.get(field):
                    return {"error": f"Trường '{field}' là bắt buộc."}

            card_id = data.get("card_id")
            phone = data.get("phone")
            email = data.get("email")
            username = data.get("username")
            birthday_str = data.get("birthday")
            birthday = (
                datetime.strptime(birthday_str, "%Y-%m-%d") if birthday_str else None
            )

            # Kiểm tra Mã số thẻ
            if not re.fullmatch(r"\d{12}", card_id):
                return {"error": "Mã số thẻ phải là số và gồm đúng 12 chữ số."}

            # Kiểm tra SĐT
            if not re.fullmatch(r"\d{10}", phone):
                return {"error": "Số điện thoại phải là số và gồm đúng 10 chữ số."}

            # Kiểm tra email
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
                return {"error": "Email không đúng định dạng."}

            # Kiểm tra ngày sinh
            if birthday >= datetime.now():
                return {"error": "Ngày sinh phải trước ngày hiện tại."}

            # Kiểm tra username có bị trùng không
            if StaffRepository.check_username_exists(username):
                return {"error": "Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác."}

            # Kiểm tra trùng mã thẻ
            if StaffRepository.check_card_id_exists(card_id):
                return {"error": "Mã số thẻ đã tồn tại. Vui lòng nhập mã khác."}

            # Kiểm tra trùng SĐT
            if StaffRepository.check_phone_exists(phone):
                return {"error": "Số điện thoại đã tồn tại. Vui lòng nhập số khác."}

            # Kiểm tra trùng Email
            if StaffRepository.check_email_exists(email):
                return {"error": "Email đã tồn tại. Vui lòng nhập email khác."}

            # Nếu qua hết các kiểm tra
            staff_model = Staff(
                full_name=data.get("full_name"),
                card_id=data.get("card_id"),
                phone=data.get("phone"),
                email=data.get("email"),
                gender=data.get("gender"),
                birthday=birthday,
            )
            staff = StaffViewModel(
                staff_model,
                role_name=data.get("role_name"),
                username=data.get("username"),
                password=data.get("password"),
            )
            result = StaffRepository.insert(staff)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_staff(staff_id, data: dict):
        try:
            # Check required fields
            required_fields = [
                "full_name",
                "phone",
                "email",
                "birthday",
                "gender",
                "role_name",
            ]
            for field in required_fields:
                if not data.get(field):
                    return {"error": f"Trường '{field}' là bắt buộc."}
            card_id = data.get("card_id")
            phone = data.get("phone")
            email = data.get("email")
            birthday_str = data.get("birthday")
            birthday = (
                datetime.strptime(birthday_str, "%Y-%m-%d") if birthday_str else None
            )
            # Kiểm tra SĐT
            if not re.fullmatch(r"\d{10}", phone):
                return {"error": "Số điện thoại phải là số và gồm đúng 10 chữ số."}
            # Kiểm tra email
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
                return {"error": "Email không đúng định dạng."}
            # Kiểm tra ngày sinh
            if birthday >= datetime.now():
                return {"error": "Ngày sinh phải trước ngày hiện tại."}
            # Kiểm tra email
            if StaffRepository.check_email_exists_for_update(email, staff_id):
                return {"error": "Email đã tồn tại trong hệ thống"}
            # Kiểm tra điện thoại
            if StaffRepository.check_phone_exists_for_update(phone, staff_id):
                return {"error": "Số điện thoại đã tồn tại trong hệ thống"}

            staff_model = Staff(
                full_name=data.get("full_name"),
                phone=data.get("phone"),
                email=data.get("email"),
                gender=data.get("gender"),
                birthday=birthday,
            )
            staff = StaffViewModel(
                staff_model,
                role_name=data.get("role_name"),
                password=data.get("password"),
            )
            print(staff.password)
            result = StaffRepository.update(staff_id, staff)
            print(result)
            if result is True:
                return {"success": True}
            else:

                return {"error": result}
        except Exception as e:
            print(e)
            return {"error": str(e)}

    @staticmethod
    def delete_staff(staff_id):
        try:
            result = StaffRepository.delete(staff_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def search_staffs(filters: dict):
        return StaffRepository.search_staffs(
            full_name=filters.get("full_name"),
            account_id=filters.get("account_id"),
            gender=filters.get("gender"),
            is_active=filters.get("is_active"),
            role_name=filters.get("role"),
        )
