from app.repositories.plannetwork_repository import PlanNetworkRepository
from app.models.plannetwork import PlanNetwork


class PlanNetworkService:
    @staticmethod
    def get_all_plan_networks():
        return PlanNetworkRepository.get_all()

    @staticmethod
    def get_plan_network_by_id(pn_id):
        return PlanNetworkRepository.get_by_id(pn_id)

    @staticmethod
    def create_plan_network(data: dict):
        try:
            pn = PlanNetwork(
                network_id=data.get("network_id"),
                plan_id=data.get("plan_id"),
            )
            result = PlanNetworkRepository.insert(pn)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_plan_network(pn_id, data: dict):
        try:
            pn = PlanNetwork(
                id=pn_id,
                network_id=data.get("network_id"),
                plan_id=data.get("plan_id"),
            )
            result = PlanNetworkRepository.update(pn_id, pn)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_plan_network(pn_id):
        try:
            result = PlanNetworkRepository.delete(pn_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
