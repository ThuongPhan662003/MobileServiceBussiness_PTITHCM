from app.repositories.customer_repository import CustomerRepository
from app.models.customer import Customer
import re

class CustomerService:
    @staticmethod
    def get_all_customers():
        return CustomerRepository.get_all()

    @staticmethod
    def get_customer_by_id(customer_id):
        return CustomerRepository.get_by_id(customer_id)

    @staticmethod
    def create_customer(data: dict):
        try:
            card_id = data.get("card_id")
            full_name = data.get("full_name")

            if not card_id or not re.fullmatch(r"\d{12}", card_id):
                return {"error": "Số CMND/CCCD (card_id) phải gồm đúng 12 chữ số"}

            if not full_name or not re.fullmatch(r"[A-Za-zÀ-Ỹà-ỹ\s]+", full_name.strip()):
                return {"error": "Tên không hợp lệ. Chỉ được chứa chữ cái và khoảng trắng"}

            if CustomerRepository.exists_by_card_id(card_id):
                return {"error": "Số CMND/CCCD đã tồn tại"}

            customer = Customer(
                full_name=full_name.strip(),
                card_id=card_id
            )
            result = CustomerRepository.insert(customer)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}

        except Exception as e:
            return {"error": f"Lỗi tạo khách hàng: {str(e)}"}

    @staticmethod
    def update_customer(customer_id, data: dict):
        try:
            card_id = data.get("card_id")
            full_name = data.get("full_name")
            is_active = str(data.get("is_active", "true")).lower() == "true"

            if not card_id or not re.fullmatch(r"\d{12}", card_id):
                return {"error": "Số CMND/CCCD (card_id) phải gồm đúng 12 chữ số"}

            if not full_name or not re.fullmatch(r"[A-Za-zÀ-Ỹà-ỹ\s]+", full_name.strip()):
                return {"error": "Tên không hợp lệ. Chỉ được chứa chữ cái và khoảng trắng"}

            if CustomerRepository.exists_by_card_id(card_id, exclude_customer_id=customer_id):
                return {"error": "Số CMND/CCCD đã tồn tại ở khách hàng khác"}

            customer = Customer(
                full_name=full_name.strip(),
                is_active=is_active,
                card_id=card_id
            )
            result = CustomerRepository.update(customer_id, customer)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_customer(customer_id):
        try:
            result = CustomerRepository.delete(customer_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
