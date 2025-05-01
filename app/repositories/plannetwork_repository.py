from app.database import db_instance
from app.models.plannetwork import PlanNetwork
from app.repositories.network_repository import NetworkRepository
from app.repositories.plan_repository import PlanRepository


class PlanNetworkRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_plan_networks", fetchall=True)
            print("repo-plan-network", result[0])
            plan_networks = []
            for row in result[0]:
                pn = PlanNetwork()
                pn.id = row.get("id")
                network_id = row.get("network_id")
                if network_id:
                    pn.network_id = NetworkRepository.get_by_id(network_id)
                else:
                    pn.network_id = None

                plan_id = row.get("plan_id")
                if plan_id:
                    pn.plan_id = PlanRepository.get_by_plan_id(plan_id)
                else:
                    pn.plan_id = None
                print("pn.to_dict", pn.network_id, pn.plan_id.to_dict(), pn.id)
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
                "CALL DeletePlanNetwork(%s)", (pn_id,), fetchone=True,commit=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa plan network: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa plan network: {e}")
            return False
