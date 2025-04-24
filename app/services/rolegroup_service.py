from app.repositories.rolegroup_repository import RoleGroupRepository
from app.models.rolegroup import RoleGroup


class RoleGroupService:
    @staticmethod
    def get_all_role_groups():
        return RoleGroupRepository.get_all()

    @staticmethod
    def get_staffs_by_role_group(role_group_id):
        try:
            # Gọi repository để lấy danh sách nhân viên
            staffs = RoleGroupRepository.get_staffs_by_role_group(role_group_id)
            return staffs
        except Exception as e:
            print(f"Lỗi trong RoleGroupService: {e}")
            return []

    @staticmethod
    def add_accounts_to_role_group(role_group_id, account_ids):
        return RoleGroupRepository.add_accounts_to_role_group(
            role_group_id, account_ids
        )

    @staticmethod
    def get_role_group_functions(role_group_id):
        # Lấy các chức năng đã gán và chưa gán cho nhóm quyền
        assigned_functions, unassigned_functions = (
            RoleGroupRepository.get_role_group_functions(role_group_id)
        )

        return {
            "assigned_functions": assigned_functions,
            "unassigned_functions": unassigned_functions,
        }

    @staticmethod
    def remove_function_from_role_group(role_group_id, function_id):
        # Gọi repository để thực hiện xóa chức năng
        result = RoleGroupRepository.remove_function_from_role_group(
            role_group_id, function_id
        )

        # Kiểm tra kết quả trả về và xử lý thông báo thành công hoặc thất bại
        if "success" in result:
            return {
                "message": "Chức năng đã được xóa khỏi nhóm quyền",
                "status": "success",
            }
        else:
            return {"message": result.get("error", "Có lỗi xảy ra"), "status": "error"}

    @staticmethod
    def add_functions_to_role_group(role_group_id, function_ids):
        return RoleGroupRepository.add_functions_to_role_group(
            role_group_id, function_ids
        )

    @staticmethod
    def get_role_group_by_id(role_id):
        return RoleGroupRepository.get_by_id(role_id)

    @staticmethod
    def create_role_group(data: dict):
        try:
            role = RoleGroup(
                role_name=data.get("role_name"),
            )
            result = RoleGroupRepository.insert(role)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_role_group(role_id, data: dict):
        try:
            role = RoleGroup(
                id=role_id,
                role_name=data.get("role_name"),
            )
            result = RoleGroupRepository.update(role_id, role)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_role_group(role_id):
        try:
            result = RoleGroupRepository.delete(role_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_staffs_not_in_role_group(role_group_id):
        return RoleGroupRepository.get_staffs_not_in_role_group(role_group_id)

    @staticmethod
    def remove_staff_from_group(role_group_id, account_id):
        return RoleGroupRepository.remove_staff_from_group(role_group_id, account_id)
