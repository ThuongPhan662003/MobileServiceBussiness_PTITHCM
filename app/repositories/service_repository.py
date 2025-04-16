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
    def insert(data: Service):
        results = None
        print("start")
        try:

            result = db_instance.execute(
                "CALL AddService(%s, %s, %s)",
                (data.service_name, data.parent_id, data.coverage_area),
                fetchone=True,
                commit=True,
            )

            if result.get("error"):
                print(f"Lỗi khi thêm dịch vụ: {result['error']}")
                return result["error"]
            print("oke")
            return True
        except Exception as e:
            print(f"Lỗi khi thêm dịch vụ: {e}")
            return False

    @staticmethod
    def update(service_id, data: Service):
        try:
            result = db_instance.execute(
                "CALL UpdateService(%s, %s, %s, %s)",
                (service_id, data.service_name, data.parent_id, data.coverage_area),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật dịch vụ: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật dịch vụ: {e}")
            return False

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
