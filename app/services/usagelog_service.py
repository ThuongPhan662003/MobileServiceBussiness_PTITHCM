from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from flask import json, session

from app.repositories.subscriber_repository import SubscriberRepository
from app.repositories.usagelog_repository import UsageLogRepository
from app.models.usagelog import UsageLog
from app.services.subscriber_service import SubscriberService

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
            start_date = (
                datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            )
            result = UsageLogRepository.search(log_type, int(subscriber_id), start_date)
            return result
        except Exception as e:
            print(f"Lỗi trong search_usagelogs: {e}")
            return []

    # @staticmethod
    # def add_usagelog(log_type: str, data: dict):
    #     try:
    #         log_type = data.get("type")
    #         subscriber_id = int(data.get("subscriber_id"))
    #
    #         # Bước 1: kiểm tra ưu đãi còn không
    #         if not UsageLogService.check_promotion_available(subscriber_id, log_type):
    #             return {
    #                 "status_code": 400,
    #                 "message": "Không còn ưu đãi cho hoạt động này",
    #             }
    #         start_date = (
    #             datetime.strptime(data.get("start_date"), "%Y-%m-%dT%H:%M")
    #             if data.get("start_date")
    #             else None
    #         )
    #         end_date = (
    #             datetime.strptime(data.get("end_date"), "%Y-%m-%dT%H:%M")
    #             if data.get("end_date")
    #             else None
    #         )
    #
    #         log = UsageLog(
    #             type=log_type,
    #             usage_value=(
    #                 int(data.get("usage_value")) if data.get("usage_value") else None
    #             ),
    #             subscriber_id=(
    #                 int(data.get("subscriber_id"))
    #                 if data.get("subscriber_id")
    #                 else None
    #             ),
    #             start_date=start_date,
    #             end_date=end_date if log_type != "TINNHAN" else start_date,
    #             by_from=data.get("by_from"),
    #             to=data.get("to") if log_type != "DULIEU" else None,
    #             contents=data.get("contents") if log_type == "TINNHAN" else None,
    #         )
    #
    #         result = UsageLogRepository.insert(log)
    #
    #         if result is True:
    #             return {"success": True}
    #         else:
    #             return {"success": False, "error": result}
    #
    #     except Exception as e:
    #         print(f"Lỗi trong add_usagelog: {e}")
    #         return {"success": False, "error": str(e)}

    @staticmethod
    def get_usagelog_by_subscriber_id(subscriber_id):
        try:
            result = UsageLogRepository.get_by_subscriber_id(subscriber_id)
            return result
        except Exception as e:
            print(f"Lỗi trong get_usagelog_by_id: {e}")
            return None

    @staticmethod
    def check_promotion_available(subscriber_id: int, log_type: str):
        try:
            result = UsageLogService.check_promotion_available(
                subscriber_id, log_type
            )
            return result
        except Exception as e:
            print(f"Lỗi trong get_usagelog_by_id: {e}")
            return None

    @staticmethod
    def get_latest_promotions(subscriber_id: int):
        return UsageLogRepository.get_latest_promotions(subscriber_id)

    @staticmethod
    def check_phone_belongs_to_subscriber(phone_number: str):
        return UsageLogRepository.check_phone_exists(phone_number)

    @staticmethod
    def add_usagelog(log_type,data: dict):
        try:
            subscriber_id = int(data.get("subscriber_id"))
            usage_value = (
                Decimal(data.get("usage_value")).quantize(
                    Decimal("0.001"), rounding=ROUND_HALF_UP
                )
                if data.get("usage_value") is not None
                else None
            )

            start_date = (
                datetime.strptime(data.get("start_date"), "%Y-%m-%dT%H:%M")
                if data.get("start_date")
                else datetime.now()
            )
            end_date = (
                datetime.strptime(data.get("end_date"), "%Y-%m-%dT%H:%M")
                if data.get("end_date")
                else (start_date if log_type == "TINNHAN" else None)
            )

            promotions_json = json.dumps(
                data.get("promotions_json", []), ensure_ascii=False
            )
            params = {
                "type": log_type,
                "usage_value": usage_value,
                "subscriber_id": subscriber_id,
                "start_date": start_date,
                "end_date": end_date,
                "by_from": data.get("by_from"),
                "to": data.get("to") if log_type != "DULIEU" else None,
                "contents": (
                    data.get("contents") if log_type == "TINNHAN" else None
                ),
                "promotions_json": promotions_json,
            }
            print("liuliu", params)
            result = UsageLogRepository.add_log_and_apply_promotions(params)
            main_balance = data.get("main_balance")
            if result and result.get("success"):
                if main_balance:
                    subscriber = SubscriberService.get_subscriber_by_id(
                        session["subscriber_id"]
                    )
                    subscriber.main_balance = main_balance
                    # data = {
                    #     "phone_number": subscriber.phone_number,
                    #     "main_balance": main_balance,
                    #     "customer_id": subscriber.customer_id,
                    #     "account_id": subscriber.account_id,
                    #     "expiration_date": None,
                    #     "warning_date": None,
                    #     "is_active": str(subscriber.is_active).lower(),
                    #     "subscriber": subscriber.subscriber_type,
                    # }
                    result1 = SubscriberRepository.update(
                        session["subscriber_id"], subscriber
                    )
                    if result.get("success"):
                        if result1:
                            return {"success": True, "message": result.get("message")}
                        else:
                            return {
                                "success": False,
                                "message": result.get("message", "Lỗi không xác định"),
                            }
                    return {
                        "success": False,
                        "message": result.get("message", "Lỗi không xác định"),
                    }
            else:
                return {
                    "success": False,"message": result.get("message", "Lỗi không xác định"),
                }

        except Exception as e:
            print(f"[Service] Error: {e}")
            return {"success": False, "message": str(e)}