from app.repositories.usagelog_repository import UsageLogRepository
from app.models.usagelog import UsageLog


class UsageLogService:
    @staticmethod
    def get_all_usage_logs():
        return UsageLogRepository.get_all()

    @staticmethod
    def get_usage_log_by_id(log_id):
        return UsageLogRepository.get_by_id(log_id)

    @staticmethod
    def create_usage_log(data: dict):
        try:
            log = UsageLog(
                type=data.get("type"),
                usage_value=data.get("usage_value"),
                subscriber_id=data.get("subscriber_id"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
            )
            result = UsageLogRepository.insert(log)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_usage_log(log_id, data: dict):
        try:
            log = UsageLog(
                type=data.get("type"),
                usage_value=data.get("usage_value"),
                subscriber_id=data.get("subscriber_id"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
            )
            result = UsageLogRepository.update(log_id, log)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_usage_log(log_id):
        try:
            result = UsageLogRepository.delete(log_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
