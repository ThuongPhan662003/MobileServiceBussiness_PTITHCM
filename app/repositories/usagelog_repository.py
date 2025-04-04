from app.database import db_instance
from app.models.usagelog import UsageLog


class UsageLogRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_usage_logs", fetchall=True)
            logs = []

            for row in result:
                u = UsageLog()
                u.id = row.get("id")
                u.type = row.get("type")
                u.usage_value = row.get("usage_value")
                u.subscriber_id = row.get("subscriber_id")
                u.start_date = row.get("start_date")
                u.end_date = row.get("end_date")
                logs.append(u.to_dict())

            return logs
        except Exception as e:
            print(f"Lỗi khi lấy danh sách usage log: {e}")
            return []

    @staticmethod
    def get_by_id(log_id):
        try:
            result = db_instance.execute(
                "CALL GetUsageLogById(%s)", (log_id,), fetchone=True
            )
            if result:
                u = UsageLog()
                for key, value in result.items():
                    setattr(u, key, value)
                return u
            return None
        except Exception as e:
            print(f"Lỗi khi lấy usage log theo ID: {e}")
            return None

    @staticmethod
    def insert(data: UsageLog):
        try:
            result = db_instance.execute(
                "CALL AddUsageLog(%s, %s, %s, %s, %s)",
                (
                    data.type,
                    data.usage_value,
                    data.subscriber_id,
                    data.start_date,
                    data.end_date,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm usage log: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm usage log: {e}")
            return False

    @staticmethod
    def update(log_id, data: UsageLog):
        try:
            result = db_instance.execute(
                "CALL UpdateUsageLog(%s, %s, %s, %s, %s, %s)",
                (
                    log_id,
                    data.type,
                    data.usage_value,
                    data.subscriber_id,
                    data.start_date,
                    data.end_date,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật usage log: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật usage log: {e}")
            return False

    @staticmethod
    def delete(log_id):
        try:
            result = db_instance.execute(
                "CALL DeleteUsageLog(%s)", (log_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa usage log: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa usage log: {e}")
            return False
