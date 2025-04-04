from app.database import db_instance
from app.models.staff import Staff


class StaffRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_staffs", fetchall=True)
            staffs = []

            for row in result:
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
                staffs.append(staff.to_dict())

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
                return staff
            return None
        except Exception as e:
            print(f"Lỗi khi lấy nhân viên theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Staff):
        try:
            result = db_instance.execute(
                "CALL AddStaff(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data.full_name,
                    data.card_id,
                    data.phone,
                    data.email,
                    data.is_active,
                    data.gender,
                    data.birthday,
                    data.account_id,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm nhân viên: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm nhân viên: {e}")
            return False

    @staticmethod
    def update(staff_id, data: Staff):
        try:
            result = db_instance.execute(
                "CALL UpdateStaff(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    staff_id,
                    data.full_name,
                    data.card_id,
                    data.phone,
                    data.email,
                    data.is_active,
                    data.gender,
                    data.birthday,
                    data.account_id,
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
