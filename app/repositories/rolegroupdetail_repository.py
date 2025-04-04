from app.database import db_instance
from app.models.rolegroupdetail import RoleGroupDetail


class RoleGroupDetailRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute(
                "SELECT * FROM v_role_group_details", fetchall=True
            )
            details = []

            for row in result:
                detail = RoleGroupDetail()
                detail.role_group_id = row.get("role_group_id")
                detail.function_id = row.get("function_id")
                details.append(detail.to_dict())

            return details
        except Exception as e:
            print(f"Lỗi khi lấy danh sách role group detail: {e}")
            return []

    @staticmethod
    def get_by_id(role_group_id, function_id):
        try:
            result = db_instance.execute(
                "CALL GetRoleGroupDetailById(%s, %s)",
                (role_group_id, function_id),
                fetchone=True,
            )
            if result:
                detail = RoleGroupDetail()
                detail.role_group_id = result.get("role_group_id")
                detail.function_id = result.get("function_id")
                return detail
            return None
        except Exception as e:
            print(f"Lỗi khi lấy role group detail theo ID: {e}")
            return None

    @staticmethod
    def insert(data: RoleGroupDetail):
        try:
            result = db_instance.execute(
                "CALL AddRoleGroupDetail(%s, %s)",
                (data.role_group_id, data.function_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm role group detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm role group detail: {e}")
            return False

    @staticmethod
    def update(role_group_id, function_id, data: RoleGroupDetail):
        """
        Cập nhật role group detail cho một role_group_id và function_id nhất định.
        """
        try:
            # Execute stored procedure to update the role group detail
            result = db_instance.execute(
                "CALL UpdateRoleGroupDetail(%s, %s, %s, %s)",
                (role_group_id, function_id, data.role_group_id, data.function_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật role group detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật role group detail: {e}")
            return False

    @staticmethod
    def delete(role_group_id, function_id):
        try:
            result = db_instance.execute(
                "CALL DeleteRoleGroupDetail(%s, %s)",
                (role_group_id, function_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi xóa role group detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa role group detail: {e}")
            return False
