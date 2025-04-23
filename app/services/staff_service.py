from app.repositories.staff_repository import StaffRepository
from app.models.staff import Staff


class StaffService:
    @staticmethod
    def get_all_staffs():
        return StaffRepository.get_all()

    

    @staticmethod
    def get_staff_by_id(staff_id):
        return StaffRepository.get_by_id(staff_id)

    @staticmethod
    def create_staff(data: dict):
        try:
            staff = Staff(
                full_name=data.get("full_name"),
                card_id=data.get("card_id"),
                phone=data.get("phone"),
                email=data.get("email"),
                is_active=data.get("is_active", True),
                gender=data.get("gender"),
                birthday=data.get("birthday"),
                account_id=data.get("account_id"),
            )
            result = StaffRepository.insert(staff)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_staff(staff_id, data: dict):
        try:
            staff = Staff(
                full_name=data.get("full_name"),
                card_id=data.get("card_id"),
                phone=data.get("phone"),
                email=data.get("email"),
                is_active=data.get("is_active", True),
                gender=data.get("gender"),
                birthday=data.get("birthday"),
                account_id=data.get("account_id"),
            )
            result = StaffRepository.update(staff_id, staff)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_staff(staff_id):
        try:
            result = StaffRepository.delete(staff_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
