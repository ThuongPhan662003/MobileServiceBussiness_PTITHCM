from datetime import date, datetime
from app.database import db_instance
from app.models.contract import Contract
from app.models.subscriber import Subscriber


class ContractRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_contracts", fetchall=True)
            contracts = []
            # print("result", result)
            for row in result[0]:
                contract = Contract()
                contract.id = row["id"]
                contract.created_at = row["created_at"]
                contract.contents = row["contents"]
                contract.title = row["title"]
                subscriber_id_data = row["subscriber_id"]
                subcriber_data = db_instance.execute(
                    "CALL GetSubscriberById(%s)",
                    int(
                        subscriber_id_data,
                    ),
                    fetchone=True,
                )
                subscriber_obj = Subscriber()
                subscriber_obj.id = subcriber_data["id"]
                subscriber_obj.phone_number = subcriber_data["phone_number"]

                contract.subscriber_id = subscriber_obj
                # print("data", contract.subscriber_id)
                contract.start_date = row["start_date"]
                contract.end_date = row["end_date"]
                contract.is_active = True if row["is_active"] else False
                # print("contract", contract)
                contracts.append(contract.to_dict())
            # print("len(contracts)", len(contracts))
            return contracts
        except Exception as e:
            print(f"Lỗi khi lấy danh sách contract: {e}")
            return []

    @staticmethod
    def get_by_id(contract_id):
        try:
            result = db_instance.execute(
                "CALL GetContractById(%s)", (contract_id,), fetchone=True
            )
            print("result", result)
            if result:
                contract = Contract()
                contract.id = result.get("id")
                contract.created_at = result.get("created_at")
                contract.contents = result.get("contents")
                contract.title = result.get("title")
                contract.start_date = result.get("start_date")
                contract.end_date = result.get("end_date")
                contract.is_active = True if result.get("is_active") else False
                subscriber_id_data = result.get("subscriber_id")
                subcriber_data = db_instance.execute(
                    "CALL GetSubscriberById(%s)",
                    int(
                        subscriber_id_data,
                    ),
                    fetchone=True,
                )
                subscriber_obj = Subscriber()
                subscriber_obj.id = subcriber_data["id"]
                subscriber_obj.phone_number = subcriber_data["phone_number"]
                contract.subscriber_id = subscriber_obj
                print("contract", contract)
                return contract
            return None
        except Exception as e:
            print(f"Lỗi khi lấy contract theo ID: {e}")
            return None

    @staticmethod
    def insert(data: dict):
        print("dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", data)
        try:
            print("ngày bắt đầu", data["start_date"])
            # Nếu start_date là chuỗi thì ép kiểu về date
            start_date = data["start_date"]
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            elif isinstance(start_date, datetime):
                start_date = start_date.date()
            elif not isinstance(start_date, date):
                raise ValueError("start_date must be a date object")
            print("ngày bắt đầu", start_date)
            # end_date có thể là None hoặc chuỗi
            end_date = data["end_date"]
            if isinstance(end_date, str) and end_date.strip() != "":
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            elif isinstance(end_date, datetime):
                end_date = end_date.date()
            elif not isinstance(end_date, (date, type(None))):
                raise ValueError("end_date must be a date object or None")
            result = db_instance.execute(
                "CALL CreateContract(%s, %s, %s, %s)",
                (
                    data["title"],
                    data["contents"],
                    start_date,
                    data["subscriber_id"],
                ),
                fetchone=True,
                commit=True,
            )

            print("kết quả", result)
            if result.get("error"):
                print(f"Lỗi từ stored procedure (insert): {result['error']}")
                return result["error"]
            return result.get("success", False)
        except Exception as e:
            print(f"Lỗi khi thêm contract: {e}")
            return False

    @staticmethod
    def update(contract_id, data: dict):
        try:
            # print(
            #     "data.is_active,",
            #     data.is_active,
            # )
            print("dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", data)
            result = db_instance.execute(
                "CALL UpdateContract(%s, %s)",
                (
                    contract_id,
                    data["is_active"],
                    # data.contents,
                    # data.title,
                    # data.start_date,
                    # data.end_date,
                    # data.is_active,
                    # data.subscriber_id,
                ),
                commit=True,
                fetchone=True,
            )
            print("update", result)
            if result.get("error"):
                print(f"Lỗi từ stored procedure (update): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật contract: {e}")
            return False

    @staticmethod
    def delete(contract_id):
        try:
            result = db_instance.execute(
                "CALL DeleteContract(%s)", (contract_id,), fetchone=True, commit=True
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (delete): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa contract: {e}")
            return False
