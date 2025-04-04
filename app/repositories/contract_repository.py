from app.database import db_instance
from app.models.contract import Contract


class ContractRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_contracts", fetchall=True)
            contracts = []

            for row in result:
                contract = Contract()
                contract.id = row.get("id")
                contract.created_at = row.get("created_at")
                contract.contents = row.get("contents")
                contract.title = row.get("title")
                contract.subscriber = row.get("subscriber")
                contract.start_date = row.get("start_date")
                contract.end_date = row.get("end_date")
                contract.is_active = row.get("is_active")
                contract.subscriber_id = row.get("subscriber_id")
                contracts.append(contract.to_dict())

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

            if result:
                contract = Contract()
                contract.id = result.get("id")
                contract.created_at = result.get("created_at")
                contract.contents = result.get("contents")
                contract.title = result.get("title")
                contract.subscriber = result.get("subscriber")
                contract.start_date = result.get("start_date")
                contract.end_date = result.get("end_date")
                contract.is_active = result.get("is_active")
                contract.subscriber_id = result.get("subscriber_id")
                return contract
            return None
        except Exception as e:
            print(f"Lỗi khi lấy contract theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Contract):
        try:
            result = db_instance.execute(
                "CALL CreateContract(%s, %s, %s, %s, %s, %s, %s)",
                (
                    data.contents,
                    data.title,
                    data.subscriber,
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
            result = db_instance.execute(
                "CALL UpdateContract(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    contract_id,
                    data.contents,
                    data.title,
                    data.subscriber,
                    data.start_date,
                    data.end_date,
                    data.is_active,
                    data.subscriber_id,
                ),
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
