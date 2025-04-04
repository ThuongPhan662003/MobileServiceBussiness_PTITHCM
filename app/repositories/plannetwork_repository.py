from app.database import db_instance
from app.models.plannetwork import PlanNetwork


class PlanNetworkRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_plan_networks", fetchall=True)
            plan_networks = []

            for row in result:
                pn = PlanNetwork()
                pn.id = row.get("id")
                pn.network_id = row.get("network_id")
                pn.plan_id = row.get("plan_id")
                plan_networks.append(pn.to_dict())

            return plan_networks
        except Exception as e:
            print(f"Lỗi khi lấy danh sách plan network: {e}")
            return []

    @staticmethod
    def get_by_id(pn_id):
        try:
            result = db_instance.execute(
                "CALL GetPlanNetworkById(%s)", (pn_id,), fetchone=True
            )
            if result:
                pn = PlanNetwork()
                pn.id = result.get("id")
                pn.network_id = result.get("network_id")
                pn.plan_id = result.get("plan_id")
                return pn
            return None
        except Exception as e:
            print(f"Lỗi khi lấy plan network theo ID: {e}")
            return None

    @staticmethod
    def insert(data: PlanNetwork):
        try:
            result = db_instance.execute(
                "CALL AddPlanNetwork(%s, %s)",
                (data.network_id, data.plan_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm plan network: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm plan network: {e}")
            return False

    @staticmethod
    def update(pn_id, data: PlanNetwork):
        try:
            result = db_instance.execute(
                "CALL UpdatePlanNetwork(%s, %s, %s)",
                (pn_id, data.network_id, data.plan_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật plan network: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật plan network: {e}")
            return False

    @staticmethod
    def delete(pn_id):
        try:
            result = db_instance.execute(
                "CALL DeletePlanNetwork(%s)", (pn_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa plan network: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa plan network: {e}")
            return False
