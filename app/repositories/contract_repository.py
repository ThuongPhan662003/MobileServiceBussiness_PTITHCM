from app.database import db_instance
from app.models.contract import Contract
from app.models.subscriber import Subscriber


class ContractRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_contracts", fetchall=True)
            contracts = []

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
                contract.start_date = row["start_date"]
                contract.end_date = row["end_date"]
                contract.is_active = True if row["is_active"] else False

                contracts.append(contract.to_dict())
            print("len(contracts)", len(contracts))
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
    def insert(data: Contract):
        try:
            result = db_instance.execute(
                "CALL CreateContract(%s, %s, %s, %s, %s, %s)",
                (
                    data.contents,
                    data.title,
                    data.start_date,
                    data.end_date,
                    data.is_active,
                    data.subscriber_id,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (insert): {result['error']}")
                return result["error"]
            return result.get("success", False)
        except Exception as e:
            print(f"Lỗi khi thêm contract: {e}")
            return False

    @staticmethod
    def update(contract_id, data: Contract):
        try:
            print(
                "data.is_active,",
                data.is_active,
            )
            result = db_instance.execute(
                "CALL UpdateContract(%s, %s)",
                (
                    contract_id,
                    data.is_active,
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
                "CALL DeleteContract(%s)", (contract_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (delete): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa contract: {e}")
            return False
