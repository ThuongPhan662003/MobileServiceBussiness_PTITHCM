from app.repositories.rolegroupdetail_repository import RoleGroupDetailRepository
from app.models.rolegroupdetail import RoleGroupDetail


class RoleGroupDetailService:
    @staticmethod
    def get_all_role_group_details():
        return RoleGroupDetailRepository.get_all()

    @staticmethod
    def get_role_group_detail_by_id(role_group_id, function_id):
        return RoleGroupDetailRepository.get_by_id(role_group_id, function_id)

    @staticmethod
    def create_role_group_detail(data: dict):
        try:
            detail = RoleGroupDetail(
                role_group_id=data.get("role_group_id"),
                function_id=data.get("function_id"),
            )
            result = RoleGroupDetailRepository.insert(detail)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_role_group_detail(role_group_id, function_id):
        try:
            result = RoleGroupDetailRepository.delete(role_group_id, function_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
