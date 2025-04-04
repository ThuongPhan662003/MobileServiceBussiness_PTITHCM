# network repositorie
from app.database import db_instance
from app.models.network import Network


class NetworkRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_networks", fetchall=True)
            networks = []

            for row in result:
                network = Network()
                network.id = row.get("id")
                network.network_name = row.get("network_name")
                network.display_name = row.get("display_name")
                network.country_id = row.get("country_id")
                networks.append(network.to_dict())

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
                network.country_id = result.get("country_id")
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
            )
            if result.get("error"):
                print(f"Lỗi khi thêm network: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm network: {e}")
            return False

    @staticmethod
    def update(network_id, data: Network):
        try:
            result = db_instance.execute(
                "CALL UpdateNetwork(%s, %s, %s, %s)",
                (network_id, data.network_name, data.display_name, data.country_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật network: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật network: {e}")
            return False

    @staticmethod
    def delete(network_id):
        try:
            result = db_instance.execute(
                "CALL DeleteNetwork(%s)", (network_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa network: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa network: {e}")
            return False
