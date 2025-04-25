# network repositorie
from app.database import db_instance
from app.models.network import Network
from app.repositories.country_repository import CountryRepository


class NetworkRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_networks", fetchall=True)
            networks = []
            print("repo", result[0])
            for row in result[0]:
                network = Network()
                network.id = row.get("id")
                network.network_name = row.get("network_name")
                network.display_name = row.get("display_name")
                print(row.get("country_id"))
                network.country_id = CountryRepository.get_by_id(row.get("country_id"))

                networks.append(network.to_dict())
            print("networks", networks)
            return networks
        except Exception as e:
            print(f"Lỗi khi lấy danh sách mạng: {e}")
            return []

    @staticmethod
    def get_by_id(network_id):
        try:
            result = db_instance.execute(
                "CALL GetNetworkById(%s)", (network_id,), fetchone=True
            )
            if result:
                network = Network()
                network.id = result.get("id")
                network.network_name = result.get("network_name")
                network.display_name = result.get("display_name")
                network.country_id = CountryRepository.get_by_id(
                    result.get("country_id")
                )
                return network
            return None
        except Exception as e:
            print(f"Lỗi khi lấy mạng theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Network):
        try:
            result = db_instance.execute(
                "CALL AddNetwork(%s, %s, %s)",
                (data.network_name, data.display_name, data.country_id),
                fetchone=True,
                commit=True,
            )
            if result.get("error"):
                return {"success": False, "error": True, "message": result["message"]}
            return {
                "success": True,
                "message": result.get("message", "Thêm mạng thành công"),
            }
        except Exception as e:
            print(f"Lỗi khi thêm network: {e}")
            return {"success": False, "error": True, "message": str(e)}

    @staticmethod
    def update(network_id, data: Network):
        try:
            result = db_instance.execute(
                "CALL UpdateNetwork(%s, %s, %s)",
                (network_id, data.display_name, data.country_id),
                fetchone=True,
                commit=True,
            )
            if result.get("error"):
                return {"success": False, "error": True, "message": result["message"]}
            return {
                "success": True,
                "message": result.get("message", "Cập nhật thành công"),
            }
        except Exception as e:
            print(f"Lỗi khi cập nhật network: {e}")
            return {"success": False, "error": True, "message": str(e)}

    @staticmethod
    def delete(network_id):
        try:
            result = db_instance.execute(
                "CALL DeleteNetwork(%s)",
                (network_id,),
                fetchone=True,
                commit=True,
            )
            if result.get("error"):
                return {"success": False, "error": True, "message": result["message"]}
            return {"success": True, "message": result.get("message", "Xóa thành công")}
        except Exception as e:
            print(f"Lỗi khi xóa network: {e}")
            return {"success": False, "error": True, "message": str(e)}
