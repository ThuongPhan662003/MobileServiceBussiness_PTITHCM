from app.database import db_instance
from app.models.plandetail import PlanDetail


class PlanDetailRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_plan_details", fetchall=True)
            details = []

            for row in result:
                detail = PlanDetail()
                detail.plan_id = row.get("plan_id")
                detail.object_type = row.get("object_type")
                detail.duration = row.get("duration")
                details.append(detail.to_dict())

            return details
        except Exception as e:
            print(f"Lỗi khi lấy danh sách plan detail: {e}")
            return []

    @staticmethod
    def get_by_id(plan_id):
        try:
            result = db_instance.execute(
                "CALL GetPlanDetailById(%s)", (plan_id,), fetchone=True
            )
            if result:
                detail = PlanDetail()
                detail.plan_id = result.get("plan_id")
                detail.object_type = result.get("object_type")
                detail.duration = result.get("duration")
                return detail
            return None
        except Exception as e:
            print(f"Lỗi khi lấy plan detail theo ID: {e}")
            return None

    @staticmethod
    def insert(data: PlanDetail):
        try:
            result = db_instance.execute(
                "CALL AddPlanDetail(%s, %s, %s)",
                (data.plan_id, data.object_type, data.duration),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm plan detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm plan detail: {e}")
            return False

    @staticmethod
    def update(plan_id, data: PlanDetail):
        try:
            result = db_instance.execute(
                "CALL UpdatePlanDetail(%s, %s, %s)",
                (plan_id, data.object_type, data.duration),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật plan detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật plan detail: {e}")
            return False

    @staticmethod
    def delete(plan_id):
        try:
            result = db_instance.execute(
                "CALL DeletelanDetail(%s)", (plan_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa plan detail: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa plan detail: {e}")
            return False
