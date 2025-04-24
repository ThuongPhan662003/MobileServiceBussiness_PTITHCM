from app.database import db_instance
from app.models.service import Service


class ServiceRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_services", fetchall=True)
            services = []
            print("resultdd", result)
            for row in result[0]:
                print("row", row)
                service = Service()
                service.id = row.get("id")
                service.service_name = row.get("service_name")
                service.parent_id = row.get("parent_id")
                service.coverage_area = True if row.get("coverage_area") else False
                services.append(service)

            return services
        except Exception as e:
            print(f"Lỗi khi lấy danh sách dịch vụ: {e}")
            return []

    @staticmethod
    def get_all_services():
        try:
            result = db_instance.execute(
                "SELECT id, service_name FROM services", fetchall=True
            )
            return result[0] if result else []
        except Exception as e:
            print("Lỗi khi lấy danh sách dịch vụ:", e)
            return []

    @staticmethod
    def get_by_id(service_id):
        try:
            result = db_instance.execute(
                "CALL GetServiceById(%s)", (service_id,), fetchone=True
            )
            if result:
                service = Service()
                service.id = result.get("id")
                service.service_name = result.get("service_name")
                service.parent_id = result.get("parent_id")
                service.coverage_area = True if result.get("coverage_area") else False
                return service
            return None
        except Exception as e:
            print(f"Lỗi khi lấy dịch vụ theo ID: {e}")
            return None

    @staticmethod
    def insert(data: dict):
        try:
            print("Start insert service...")
            print("coverage_area type:", type(data["coverage_area"]))

            result = db_instance.execute(
                "CALL AddService(%s, %s, %s)",
                (data["service_name"], data["parent_id"], data["coverage_area"]),
                fetchone=True,
                commit=True,
            )
            print("Kết quả từ stored procedure:", result)

            # Nếu stored procedure trả về lỗi logic (ví dụ trùng tên)
            if result.get("error") or result.get("success") is False:
                return {
                    "success": False,
                    "error": result.get("error"),
                    "message": result.get("message", "Thêm dịch vụ thất bại."),
                }

            # Thành công
            return {
                "success": True,
                "message": result.get("message", "Thêm dịch vụ thành công."),
            }

        except Exception as e:
            print("Lỗi exception khi insert service:", e)
            return {
                "success": False,
                "error": str(e),
                "message": "Lỗi hệ thống khi tạo dịch vụ.",
            }

    @staticmethod
    def update(service_id: int, data: Service):
        try:
            result = db_instance.execute(
                "CALL UpdateService(%s, %s, %s)",
                (service_id, data.parent_id, data.coverage_area),
                fetchone=True,
                commit=True,
            )

            print("[Update Result]", result)

            # ✅ Trường hợp có lỗi (result là dict chứa "error")
            if result.get("error"):
                return {
                    "success": False,
                    "error": True,
                    "message": result.get("message", "Lỗi khi cập nhật dịch vụ."),
                }

            return {
                "success": True,
                "message": result.get("message", "Cập nhật dịch vụ thành công."),
            }

        except Exception as e:
            print(f"[Exception] Lỗi khi cập nhật dịch vụ:", str(e))
            return {
                "success": False,
                "error": True,
                "message": f"Lỗi hệ thống: {str(e)}",
            }

    @staticmethod
    def delete(service_id):
        try:
            result = db_instance.execute(
                "CALL DeleteService(%s)", (service_id,), fetchone=True, commit=True
            )
            print("delete,ddd", result)

            if not result.get("success"):
                print(f"Lỗi khi xóa dịch vụ: {result['message']}")
                return False, result["message"]
            return True, ""
        except Exception as e:
            print(f"Lỗi khi xóa dịch vụ: {e}")
            return False, e
