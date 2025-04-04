from app.repositories.permissiondetail_repository import PermissionDetailRepository
from app.models.permissiondetail import PermissionDetail


class PermissionDetailService:
    @staticmethod
    def get_all_permission_details():
        return PermissionDetailRepository.get_all()

    @staticmethod
    def get_permission_detail_by_id(role_group_id, account_id):
        return PermissionDetailRepository.get_by_id(role_group_id, account_id)

    @staticmethod
    def create_permission_detail(data: dict):
        try:
            permission = PermissionDetail(
                role_group_id=data.get("role_group_id"),
                account_id=data.get("account_id"),
            )
            result = PermissionDetailRepository.insert(permission)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_permission_detail(role_group_id, account_id):
        try:
            result = PermissionDetailRepository.delete(role_group_id, account_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
