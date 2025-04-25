from app.database import db_instance
from app.models.staff import Staff
from app.services.account_service import AccountService
from app.viewmodels.staff_view_model import StaffViewModel


class StaffRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute(
                """SELECT s.*, rg.role_name
    FROM staffs s
    JOIN accounts a ON s.account_id = a.id
    JOIN permissiondetail pd ON a.id = pd.account_id
    JOIN rolegroup rg ON pd.role_group_id = rg.id""",
                fetchall=True,
            )
            staffs = []

            for row in result[0]:
                staff = Staff()
                staff.id = row.get("id")
                staff.full_name = row.get("full_name")
                staff.card_id = row.get("card_id")
                staff.phone = row.get("phone")
                staff.email = row.get("email")
                staff.is_active = True if row.get("is_active") else False
                staff.gender = row.get("gender")
                staff.birthday = row.get("birthday")

                #                 acc = AccountService.get_account_by_id(row.get("account_id"))
                #                 staff.account_id = acc
                #                 staffs.append(staff.to_dict())

                staff.account_id = row.get("account_id")

                # Tạo ViewModel với role_name
                staff_vm = StaffViewModel(staff, row.get("role_name"))
                staffs.append(staff_vm.to_dict())

            return staffs
        except Exception as e:
            print(f"Lỗi khi lấy danh sách nhân viên: {e}")
            return []

    @staticmethod
    def get_by_id(staff_id):
        try:
            result = db_instance.execute(
                "CALL GetStaffById(%s)", (staff_id,), fetchone=True
            )
            if result:
                staff = Staff()
                for key in result:
                    setattr(staff, key, result[key])
                staff["is_active"] = True if result["is_active"] else False
                return staff
            return None
        except Exception as e:
            print(f"Lỗi khi lấy nhân viên theo ID: {e}")
            return None

    @staticmethod
    def get_by_account_id(account_id):
        try:
            result = db_instance.execute(
                "CALL GetStaffByAccountId(%s)", (account_id,), fetchone=True
            )
            print("kết quả từ sp", result)
            if result:
                result["is_active"] = True if result["is_active"] else False
                return result
            return None
        except Exception as e:
            print(f"Lỗi khi lấy nhân viên theo ID: {e}")
            return None

    @staticmethod
    def insert(data: StaffViewModel):

        try:
            print(data.to_dict())
            result = db_instance.execute(
                "CALL AddStaff(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data.full_name,
                    data.card_id,
                    data.phone,
                    data.email,
                    data.birthday,
                    data.gender,
                    data.role_name,
                    data.username,
                    data.password,
                ),
                fetchone=True,
                commit=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm nhân viên: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm nhân viên: {e}")
            return False

    @staticmethod
    def check_username_exists(username: str):
        try:
            result = db_instance.execute(
                "SELECT COUNT(*) AS count FROM accounts WHERE username = %s",
                (username,),
                fetchone=True,
            )
            return result["count"] > 0
        except Exception as e:
            print(f"Lỗi khi kiểm tra username: {e}")
            return True  # giả định đã tồn tại nếu lỗi DB

    @staticmethod
    def check_card_id_exists(card_id: str):
        try:
            result = db_instance.execute(
                "SELECT COUNT(*) AS count FROM staffs WHERE card_id = %s",
                (card_id,),
                fetchone=True,
            )
            return result["count"] > 0
        except Exception as e:
            print(f"Lỗi khi kiểm tra card_id: {e}")
            return True  # Giả định đã tồn tại nếu lỗi DB

    @staticmethod
    def check_phone_exists(phone: str):
        try:
            result = db_instance.execute(
                "SELECT COUNT(*) AS count FROM staffs WHERE phone = %s",
                (phone,),
                fetchone=True,
            )
            return result["count"] > 0
        except Exception as e:
            print(f"Lỗi khi kiểm tra phone: {e}")
        return True

    @staticmethod
    def check_email_exists(email: str):
        try:
            result = db_instance.execute(
                "SELECT COUNT(*) AS count FROM staffs WHERE email = %s",
                (email,),
                fetchone=True,
            )
            return result["count"] > 0
        except Exception as e:
            print(f"Lỗi khi kiểm tra email: {e}")
            return True

    @staticmethod
    def check_email_exists_for_update(email: str, staff_id: int):
        try:
            result = db_instance.execute(
                """
                SELECT COUNT(*) AS count
                FROM staffs
                WHERE email = %s AND id != %s
                """,
                (email, staff_id),
                fetchone=True,
            )
            return result["count"] > 0
        except Exception as e:
            print(f"Lỗi khi kiểm tra email trong cập nhật: {e}")
            return True  # trả về True để phòng tránh lỗi logic nếu exception

    @staticmethod
    def check_phone_exists_for_update(phone: str, staff_id: int):
        try:
            result = db_instance.execute(
                """
                SELECT COUNT(*) AS count
                FROM staffs
                WHERE phone = %s AND id != %s
                """,
                (phone, staff_id),
                fetchone=True,
            )
            return result["count"] > 0
        except Exception as e:
            print(f"Lỗi khi kiểm tra số điện thoại trong cập nhật: {e}")
            return True

    @staticmethod
    def update(staff_id, data: StaffViewModel):
        try:
            print(staff_id)
            print(data.to_dict())
            result = db_instance.execute(
                "CALL UpdateStaff(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    staff_id,
                    data.full_name,
                    data.phone,
                    data.email,
                    data.gender,
                    data.birthday,
                    data.role_name,
                    data.password,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật nhân viên: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật nhân viên: {e}")
            return False

    @staticmethod
    def delete(staff_id):
        try:
            result = db_instance.execute(
                "CALL DeleteStaff(%s)", (staff_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa nhân viên: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa nhân viên: {e}")
            return False

    @staticmethod
    def search_staffs(
        full_name=None, account_id=None, gender=None, is_active=None, role_name=None
    ):
        try:
            result = db_instance.execute(
                "CALL SearchStaffs(%s, %s, %s, %s, %s)",
                (
                    full_name if full_name else None,
                    account_id if account_id else None,
                    gender if gender else None,
                    (
                        int(is_active)
                        if is_active != "" and is_active is not None
                        else None
                    ),
                    role_name if role_name else None,
                ),
                fetchall=True,
            )

            staffs = []
            for row in result[0]:
                staff = Staff()
                staff.id = row.get("id")
                staff.full_name = row.get("full_name")
                staff.card_id = row.get("card_id")
                staff.phone = row.get("phone")
                staff.email = row.get("email")
                staff.is_active = True if row.get("is_active") else False
                staff.gender = row.get("gender")
                staff.birthday = row.get("birthday")
                staff.account_id = row.get("account_id")

                staff_vm = StaffViewModel(staff, row.get("role_name"))
                staffs.append(staff_vm.to_dict())
            return staffs
        except Exception as e:
            print(f"Lỗi tìm kiếm nhân viên: {e}")
            return []
