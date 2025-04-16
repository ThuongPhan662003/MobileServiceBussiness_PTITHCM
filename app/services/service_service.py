from app.repositories.service_repository import ServiceRepository
from app.models.service import Service


class ServiceService:
    @staticmethod
    def get_all_services():
        return ServiceRepository.get_all()

    @staticmethod
    def get_service_by_id(service_id):
        return ServiceRepository.get_by_id(service_id)

    @staticmethod
    def create_service(data: dict):
        try:
            service = Service(
                service_name=data.get("service_name"),
                parent_id=data.get("parent_id"),
                coverage_area=data.get("coverage_area", False),
            )
            result = ServiceRepository.insert(service)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_service(service_id, data: dict):
        try:
            service = Service(
                service_name=data.get("service_name"),
                parent_id=data.get("parent_id"),
                coverage_area=data.get("coverage_area", False),
            )
            result = ServiceRepository.update(service_id, service)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_service(service_id):
        try:
            result, message = ServiceRepository.delete(service_id)
            print("delete_service", result, message)
            if result is True:
                return {"success": True}
            else:
                return {"error": message}
        except Exception as e:
            return {"error": str(e)}
