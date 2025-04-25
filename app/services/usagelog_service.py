from datetime import datetime
from app.repositories.usagelog_repository import UsageLogRepository
from app.models.usagelog import UsageLog

def parse_datetime_safe(value):
    if isinstance(value, (datetime, date)):
        return value
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None

class UsageLogService:
    @staticmethod
    def get_all_usagelogs():
        try:
            result = UsageLogRepository.get_all()
            return result
        except Exception as e:
            print(f"Lỗi trong get_all_usagelogs: {e}")
            return []

    @staticmethod
    def get_usagelog_by_id(log_id):
        try:
            result = UsageLogRepository.get_by_id(log_id)
            return result
        except Exception as e:
            print(f"Lỗi trong get_usagelog_by_id: {e}")
            return None

    @staticmethod
    def get_logs_by_type(log_type: str):
        try:
            result = UsageLogRepository.get_by_type(log_type)
            return result
        except Exception as e:
            print(f"Lỗi trong get_logs_by_type: {e}")
            return []

    @staticmethod
    def search_usagelogs(log_type: str, subscriber_id: str, start_date: str):
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            result = UsageLogRepository.search(log_type, int(subscriber_id), start_date)
            return result
        except Exception as e:
            print(f"Lỗi trong search_usagelogs: {e}")
            return []

    @staticmethod
    def add_usagelog(log_type: str, data: dict):
        try:
            start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%dT%H:%M") if data.get("start_date") else None
            end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%dT%H:%M") if data.get("end_date") else None
            
            log = UsageLog(
                type=log_type,
                usage_value=int(data.get("usage_value")) if data.get("usage_value") else None,
                subscriber_id=int(data.get("subscriber_id")) if data.get("subscriber_id") else None,
                start_date=start_date,
                end_date=end_date if log_type != "TINNHAN" else start_date,
                by_from=data.get("by_from"),
                to=data.get("to") if log_type != "DULIEU" else None,
                contents=data.get("contents") if log_type == "TINNHAN" else None
            )
            
            result = UsageLogRepository.insert(log)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            print(f"Lỗi trong add_usagelog: {e}")
            return {"error": str(e)}