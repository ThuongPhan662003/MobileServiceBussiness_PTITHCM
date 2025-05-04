from datetime import datetime, date  # Thêm import date
from app.database import db_instance
from app.models.usagelog import UsageLog
from app.repositories.subscriber_repository import SubscriberRepository


def parse_datetime_safe(value):
    if isinstance(value, (datetime, date)):  # Kiểm tra datetime hoặc date
        return value
    if value == "0000-00-00 00:00:00":  # Xử lý giá trị không hợp lệ
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


class UsageLogRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_usage_logs", fetchall=True)
            logs = []
            if not result or not result[0]:  # Kiểm tra result rỗng
                print("Không có dữ liệu trong result[0]")
                return []
            for row in result[0]:
                if not isinstance(row, dict):  # Kiểm tra row là dictionary
                    print(f"Cảnh báo: Row không phải dictionary: {row}")
                    continue
                try:
                    id_value = int(row.get("id")) if row.get("id") is not None else None
                    subscriber_id = (
                        int(row.get("subscriber_id"))
                        if row.get("subscriber_id") is not None
                        else None
                    )
                    usage_value = (
                        int(row.get("usage_value"))
                        if row.get("usage_value") is not None
                        else None
                    )
                except (ValueError, TypeError) as e:
                    print(
                        f"Cảnh báo: Giá trị không hợp lệ: id={row.get('id')}, subscriber_id={row.get('subscriber_id')}, usage_value={row.get('usage_value')}, lỗi={e}"
                    )
                    continue
                sub = SubscriberRepository.get_by_id(subscriber_id)
                if sub:
                    u = UsageLog(
                        id=id_value,
                        type=row.get("type"),
                        usage_value=usage_value,
                        subscriber_id=sub.id,
                        start_date=parse_datetime_safe(row.get("start_date")),
                        end_date=parse_datetime_safe(row.get("end_date")),
                        by_from=row.get("by_from"),
                        to=row.get("to"),
                        contents=row.get("contents"),
                    )
                    logs.append(u.to_dict())
                else:
                    print(f"Cảnh báo: Không tìm thấy subscriber với id={subscriber_id}")
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
                u = UsageLog(
                    id=result.get("id"),
                    type=result.get("type"),
                    usage_value=result.get("usage_value"),
                    subscriber_id=result.get("subscriber_id"),
                    start_date=parse_datetime_safe(result.get("start_date")),
                    end_date=parse_datetime_safe(result.get("end_date")),
                    by_from=result.get("by_from"),
                    to=result.get("to"),
                    contents=result.get("contents"),
                )
                return u
            return None
        except Exception as e:
            print(f"Lỗi khi lấy usage log theo ID: {e}")
            return None

    @staticmethod
    def get_by_type(log_type: str):
        try:
            result = db_instance.execute(
                "SELECT * FROM v_usage_logs WHERE type = %s", (log_type,), fetchall=True
            )
            logs = []
            if not result or not result[0]:  # Kiểm tra result rỗng
                print(f"Không có dữ liệu cho type={log_type}")
                return []
            for row in result[0]:
                if not isinstance(row, dict):  # Kiểm tra row là dictionary
                    print(f"Cảnh báo: Row không phải dictionary: {row}")
                    continue
                try:

                    id_value = int(row.get("id")) if row.get("id") is not None else None
                    subscriber_id = (
                        int(row.get("subscriber_id"))
                        if row.get("subscriber_id") is not None
                        else None
                    )
                    usage_value = (
                        int(row.get("usage_value"))
                        if row.get("usage_value") is not None
                        else None
                    )
                except (ValueError, TypeError) as e:
                    print(
                        f"Cảnh báo: Giá trị không hợp lệ: id={row.get('id')}, subscriber_id={row.get('subscriber_id')}, usage_value={row.get('usage_value')}, lỗi={e}"
                    )
                    continue
                sub = SubscriberRepository.get_by_id(subscriber_id)
                if sub:
                    u = UsageLog(
                        id=id_value,
                        type=row.get("type"),
                        usage_value=usage_value,
                        subscriber_id=sub.id,
                        start_date=parse_datetime_safe(row.get("start_date")),
                        end_date=parse_datetime_safe(row.get("end_date")),
                        by_from=row.get("by_from"),
                        to=row.get("to"),
                        contents=row.get("contents"),
                    )
                    logs.append(u.to_dict())
                else:
                    print(f"Cảnh báo: Không tìm thấy subscriber với id={subscriber_id}")
            return logs
        except Exception as e:
            print(f"Lỗi khi lấy usage log theo type: {e}")
            return []

    @staticmethod
    def search(log_type: str, subscriber_id: int, start_date: datetime):
        try:
            result = db_instance.execute(
                "CALL SearchUsageLogs(%s, %s, %s)",
                (log_type, subscriber_id, start_date),
                fetchall=True,
            )
            logs = []
            if not result or not result[0]:  # Kiểm tra result rỗng
                print(
                    f"Không có dữ liệu cho search type={log_type}, subscriber_id={subscriber_id}"
                )
                return []
            for row in result[0]:

                if not isinstance(row, dict):  # Kiểm tra row là dictionary
                    print(f"Cảnh báo: Row không phải dictionary: {row}")
                    continue
                try:

                    id_value = int(row.get("id")) if row.get("id") is not None else None
                    subscriber_id_val = (
                        int(row.get("subscriber_id"))
                        if row.get("subscriber_id") is not None
                        else None
                    )
                    usage_value = (
                        int(row.get("usage_value"))
                        if row.get("usage_value") is not None
                        else None
                    )
                except (ValueError, TypeError) as e:
                    print(
                        f"Cảnh báo: Giá trị không hợp lệ: id={row.get('id')}, subscriber_id={row.get('subscriber_id')}, usage_value={row.get('usage_value')}, lỗi={e}"
                    )
                    continue
                sub = SubscriberRepository.get_by_id(subscriber_id_val)
                if sub:
                    u = UsageLog(
                        id=id_value,
                        type=row.get("type"),
                        usage_value=usage_value,
                        subscriber_id=sub.id,
                        start_date=parse_datetime_safe(row.get("start_date")),
                        end_date=parse_datetime_safe(row.get("end_date")),
                        by_from=row.get("by_from"),
                        to=row.get("to"),
                        contents=row.get("contents"),
                    )
                    logs.append(u.to_dict())
                else:
                    print(
                        f"Cảnh báo: Không tìm thấy subscriber với id={subscriber_id_val}"
                    )
            return logs
        except Exception as e:
            print(f"Lỗi khi tìm kiếm usage log: {e}")
            return []

    @staticmethod
    def insert(data: UsageLog):
        try:
            result = db_instance.execute(
                "CALL AddUsageLog(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    data.type,
                    data.usage_value,
                    data.subscriber_id,
                    data.start_date,
                    data.end_date,
                    data.by_from,
                    data.to,
                    data.contents,
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
