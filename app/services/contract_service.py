from datetime import datetime
from app.repositories.contract_repository import ContractRepository
from app.models.contract import Contract


class ContractService:
    @staticmethod
    def get_all_contracts():
        return ContractRepository.get_all()

    @staticmethod
    def get_contract_by_id(contract_id):
        return ContractRepository.get_by_id(contract_id)

    @staticmethod
    def create_contract(data: dict):
        try:
            contract = Contract(
                contents=data.get("contents"),
                title=data.get("title"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
                is_active=data.get("is_active", True),
                subscriber_id=data.get("subscriber_id"),
            )
            result = ContractRepository.insert(contract)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_contract(contract_id, data: dict):
        try:
            start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
            contract = Contract(
                contents=data.get("contents"),
                title=data.get("title"),
                start_date=start_date,
                end_date=None,
                is_active=data.get("is_active", True),
                subscriber_id=data.get("subscriber_id"),
            )
            result = ContractRepository.update(contract_id, contract)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_contract(contract_id):
        try:
            result = ContractRepository.delete(contract_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
