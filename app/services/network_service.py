from app.repositories.network_repository import NetworkRepository
from app.models.network import Network


class NetworkService:
    @staticmethod
    def get_all_networks():
        return NetworkRepository.get_all()

    @staticmethod
    def get_network_by_id(network_id):
        return NetworkRepository.get_by_id(network_id)

    @staticmethod
    def create_network(data: dict):
        try:
            network = Network(
                network_name=data.get("network_name"),
                display_name=data.get("display_name"),
                country_id=data.get("country_id"),
            )
            result = NetworkRepository.insert(network)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_network(network_id, data: dict):
        try:
            network = Network(
                network_name=data.get("network_name"),
                display_name=data.get("display_name"),
                country_id=data.get("country_id"),
            )
            result = NetworkRepository.update(network_id, network)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_network(network_id):
        try:
            result = NetworkRepository.delete(network_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
