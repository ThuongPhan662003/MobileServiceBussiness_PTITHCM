from app.repositories.plandetail_repository import PlanDetailRepository
from app.models.plandetail import PlanDetail


class PlanDetailService:
    @staticmethod
    def get_all_plan_details():
        return PlanDetailRepository.get_all()

    @staticmethod
    def get_plan_detail_by_id(plan_id):
        return PlanDetailRepository.get_by_id(plan_id)

    @staticmethod
    def create_plan_detail(data: dict):
        try:
            detail = PlanDetail(
                plan_id=data.get("plan_id"),
                object_type=data.get("object_type"),
                duration=data.get("duration"),
            )
            result = PlanDetailRepository.insert(detail)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_plan_detail(plan_id, data: dict):
        try:
            detail = PlanDetail(
                plan_id=plan_id,  # hoặc giữ nguyên ID nếu đã được xác định từ trước
                object_type=data.get("object_type"),
                duration=data.get("duration"),
            )
            result = PlanDetailRepository.update(plan_id, detail)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_plan_detail(plan_id):
        try:
            result = PlanDetailRepository.delete(plan_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
