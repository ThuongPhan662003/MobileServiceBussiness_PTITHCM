from flask import json
from app.database import db_instance
from app.models.rolegroup import RoleGroup
from app.models.staff import Staff
from app.services.account_service import AccountService


class RoleGroupRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_role_groups", fetchall=True)
            role_groups = []

            for row in result[0]:
                role = RoleGroup()
                role.id = row.get("id")
                role.role_name = row.get("role_name")
                role_groups.append(role.to_dict())

            return role_groups
        except Exception as e:
            print(f"Lỗi khi lấy danh sách role group: {e}")
            return []

    @staticmethod
    def add_accounts_to_role_group(role_group_id, account_ids_csv):
        try:
            print("fffffffffffffff", role_group_id, account_ids_csv)
            result = db_instance.execute(
                "CALL sp_add_multiple_permissiondetails_from_csv(%s, %s)",
                (role_group_id, account_ids_csv),
                fetchone=True,
                commit=True,
            )
            if result and result.get("success"):
                return {"success": True}
            else:
                return result.get("error", "Có lỗi xảy ra")
        except Exception as e:
            print(f"Lỗi khi thêm accounts vào nhóm quyền: {e}")
            return {"error": f"Đã xảy ra lỗi: {str(e)}"}

    @staticmethod
    def get_staffs_by_role_group(role_group_id):
        try:
            # Gọi stored procedure 'GetStaffsByRoleGroupId' với tham số là role_group_id
            print("role_group_id", type(role_group_id))
            query = "CALL GetStaffsByRoleGroupId(%s)"
            result = db_instance.execute(query, (role_group_id,), fetchall=True)
            print("result", result)
            staffs = []
            for row in result[0]:
                staff = Staff()
                staff.id = row.get("staff_id")
                staff.full_name = row.get("full_name")
                staff.card_id = row.get("card_id")
                staff.phone = row.get("phone")
                staff.email = row.get("email")
                staff.gender = row.get("gender")
                staff.birthday = row.get("birthday")
                acc = AccountService.get_account_by_id(row.get("account_id"))
                staff.account_id = acc
                staffs.append(staff.to_dict())
                print(staff)
            return staffs
        except Exception as e:
            print(f"Lỗi khi lấy nhân viên theo role_group_id: {e}")
            return []

    @staticmethod
    def get_role_group_functions(role_group_id):
        try:
            result = db_instance.execute(
                "CALL GetRoleGroupFunctionsAndAvailableFunctions(%s)",
                (role_group_id,),
                fetchall=True,
            )
            print(result)
            if result:
                assigned_functions = []
                unassigned_functions = []

                # Xử lý các chức năng đã gán
                for row in result[0]:
                    print(int(row["id"]))
                    assigned_functions.append(
                        {"id": int(row["id"]), "function_name": row["function_name"]}
                    )

                # Xử lý các chức năng chưa gán
                for row in result[1]:
                    print(int(row["id"]))
                    unassigned_functions.append(
                        {"id": int(row["id"]), "function_name": row["function_name"]}
                    )

                return assigned_functions, unassigned_functions
            return [], []
        except Exception as e:
            print(f"Lỗi khi lấy chức năng cho nhóm quyền: {e}")
            return [], []

    @staticmethod
    def remove_function_from_role_group(role_group_id, function_id):
        try:
            print("role_group_id", type(role_group_id))
            print("function_id", type(function_id))

            # Tạo các biến để nhận giá trị OUT
            success = None
            message = None

            # Gọi stored procedure với các tham số IN và OUT
            db_instance.execute(
                "CALL RemoveFunctionFromRoleGroup(%s, %s, @p_success, @p_message)",
                (role_group_id, function_id),
                commit=True,
            )

            # Lấy kết quả từ các biến OUT sau khi thực thi stored procedure
            result = db_instance.execute(
                "SELECT @p_success, @p_message;", fetchone=True
            )
            print("resulsds444dsdt", result)
            # Kiểm tra kết quả trả về
            if result:
                p_success = result.get("@p_success")  # success từ OUT parameter
                p_message = result.get("@p_message")  # message từ OUT parameter

                # Kiểm tra kết quả thành công
                if p_success:

                    return {"success": True, "message": p_message}  # Thành công
                else:
                    return {"error": p_message}  # Thất bại, trả về thông báo lỗi

            return {"error": "Unknown error occurred"}  # Nếu không có kết quả hợp lệ

        except Exception as e:
            print(f"Lỗi khi xóa chức năng: {e}")
            return {"error": str(e)}  # Trả về thông báo lỗi nếu có lỗi

    @staticmethod
    def add_functions_to_role_group(role_group_id, function_ids):
        try:
            function_ids_json = json.dumps(
                function_ids
            )  # Chuyển danh sách function_ids thành JSON
            print("function_ids_json", function_ids_json)
            # Thực thi stored procedure
            result = db_instance.execute(
                "CALL AddFunctionsToRoleGroup(%s, %s)",
                (role_group_id, function_ids_json),
                fetchone=True,
            )
            print("result", result)
            if result and result.get("success"):
                return {"success": True}
            else:
                return result.get(
                    "error", "Có lỗi xảy ra"
                )  # Trả về thông báo lỗi nếu có lỗi

        except Exception as e:
            return {"error": f"Đã xảy ra lỗi: {str(e)}"}

    @staticmethod
    def get_by_id(role_id):
        try:
            result = db_instance.execute(
                "CALL GetRoleGroupById(%s)", (role_id,), fetchone=True
            )
            if result:
                role = RoleGroup()
                role.id = result.get("id")
                role.role_name = result.get("role_name")
                return role
            return None
        except Exception as e:
            print(f"Lỗi khi lấy role group theo ID: {e}")
            return None

    @staticmethod
    def insert(data: RoleGroup):
        try:
            result = db_instance.execute(
                "CALL AddRoleGroup(%s)", (data.role_name,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi thêm role group: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm role group: {e}")
            return False

    @staticmethod
    def update(role_id, data: RoleGroup):
        try:
            result = db_instance.execute(
                "CALL UpdateRoleGroup(%s, %s)",
                (role_id, data.role_name),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật role group: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật role group: {e}")
            return False

    @staticmethod
    def remove_staff_from_group(role_group_id, account_id):
        try:
            result = db_instance.execute(
                "CALL sp_remove_permission_detail(%s, %s)",
                (role_group_id, account_id),
                fetchone=True,
            )
            return result
        except Exception as e:
            print(f"[Repo] Lỗi khi xóa nhân viên khỏi nhóm quyền: {e}")
            return {"error": str(e)}

    @staticmethod
    def delete(role_id):
        try:
            result = db_instance.execute(
                "CALL DeleteRoleGroup(%s)", (role_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa role group: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa role group: {e}")
            return False

    @staticmethod
    def get_staffs_not_in_role_group(role_group_id):
        try:
            # result = db_instance.execute("SELECT * FROM v_staffs", fetchall=True)
            result = db_instance.execute(
                "CALL sp_get_staffs_not_in_role_group(%s)",
                (role_group_id,),
                fetchall=True,
            )
            print("re", result)
            staffs = []

            for row in result[0]:
                staff = Staff()
                staff.id = row.get("id")
                staff.full_name = row.get("full_name")
                # staff.card_id = row.get("card_id")
                staff.phone = row.get("phone")
                staff.email = row.get("email")
                # staff.is_active = True if row.get("is_active") else False
                # staff.gender = row.get("gender")
                # staff.birthday = row.get("birthday")
                acc = AccountService.get_account_by_id(row.get("account_id"))
                staff.account_id = acc
                staffs.append(staff.to_dict())

            return staffs
        except Exception as e:
            print(f"Lỗi khi lấy danh sách nhân viên: {e}")
            return []
