from app.repositories.customer_repository import CustomerRepository
from app.models.customer import Customer


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
            customer = Customer(
                full_name=data.get("full_name"),
                is_active=data.get("is_active", True),
                account_id=data.get("account_id"),
                card_id=data.get("card_id"),
            )
            result = CustomerRepository.insert(customer)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_customer(customer_id, data: dict):
        try:
            customer = Customer(
                full_name=data.get("full_name"),
                is_active=data.get("is_active", True),
                account_id=data.get("account_id"),
                card_id=data.get("card_id"),
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
