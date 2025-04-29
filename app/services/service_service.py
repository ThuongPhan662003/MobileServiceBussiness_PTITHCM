from app.repositories.service_repository import ServiceRepository
from app.models.service import Service


class ServiceService:
    @staticmethod
    def get_all():
        return ServiceRepository.get_all()

    @staticmethod
    def get_all_services():
        return ServiceRepository.get_all_services()

    @staticmethod
    def get_service_by_id(service_id):
        return ServiceRepository.get_by_id(service_id)

    @staticmethod
    def create_service(data: dict):
        try:
            print("Bắt đầu xử lý tạo dịch vụ...")

            # Gọi repository insert
            result = ServiceRepository.insert(data)
            print("Kết quả từ repository:", result)

            # Nếu repository trả về lỗi
            if not result.get("success"):
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "message": result.get("message", "Tạo dịch vụ thất bại."),
                }

            # Thành công
            return {
                "success": True,
                "message": result.get("message", "Tạo dịch vụ thành công."),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Lỗi hệ thống trong quá trình tạo dịch vụ.",
            }

    @staticmethod
    def update_service(service_id, data: dict):
        try:
            # Khởi tạo đối tượng Service từ dữ liệu đầu vào
            service = Service(
                service_name=data.get("service_name"),
                parent_id=data.get("parent_id"),
                coverage_area=data.get("coverage_area", False),
            )

            # Gọi repository để update
            result = ServiceRepository.update(service_id, service)
            print("[Update Result in Service Layer]", result)

            # Xử lý kết quả từ repository
            if result.get("success"):
                return {
                    "success": True,
                    "message": result.get("message", "Cập nhật dịch vụ thành công."),
                }
            else:
                return {
                    "success": False,
                    "error": True,
                    "message": result.get("message", "Cập nhật dịch vụ thất bại."),
                }

        except Exception as e:
            return {
                "success": False,
                "error": True,
                "message": f"Lỗi hệ thống khi cập nhật: {str(e)}",
            }

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
