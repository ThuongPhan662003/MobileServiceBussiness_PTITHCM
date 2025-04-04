from app.database import db_instance
from app.models.permissiondetail import PermissionDetail


class PermissionDetailRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute(
                "SELECT * FROM v_permission_details", fetchall=True
            )
            permissions = []

            for row in result:
                permission = PermissionDetail()
                permission.role_group_id = row.get("role_group_id")
                permission.account_id = row.get("account_id")
                permissions.append(permission.to_dict())

            return permissions
        except Exception as e:
            print(f"Lỗi khi lấy danh sách permission detail: {e}")
            return []

    @staticmethod
    def get_by_id(role_group_id, account_id):
        try:
            result = db_instance.execute(
                "CALL GetRoleGroupById(%s, %s)",
                (role_group_id, account_id),
                fetchone=True,
            )
            if result:
                permission = PermissionDetail()
                permission.role_group_id = result.get("role_group_id")
                permission.account_id = result.get("account_id")
                return permission
            return None
        except Exception as e:
            print(f"Lỗi khi lấy permission detail theo ID kép: {e}")
            return None

    @staticmethod
    def insert(data: PermissionDetail):
        try:
            result = db_instance.execute(
                "CALL AddPermissionDetail(%s, %s)",
                (data.role_group_id, data.account_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm permission detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm permission detail: {e}")
            return False

    @staticmethod
    def update(role_group_id, account_id, data: PermissionDetail):
        """
        Cập nhật permission detail cho một role_group_id và account_id nhất định.
        """
        try:
            # Execute stored procedure to update the permission detail
            result = db_instance.execute(
                "CALL UpdatePermissionDetail(%s, %s, %s, %s)",
                (role_group_id, account_id, data.role_group_id, data.account_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật permission detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật permission detail: {e}")
            return False

    @staticmethod
    def delete(role_group_id, account_id):
        try:
            result = db_instance.execute(
                "CALL DeletePermissionDetail(%s, %s)",
                (role_group_id, account_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi xóa permission detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa permission detail: {e}")
            return False
