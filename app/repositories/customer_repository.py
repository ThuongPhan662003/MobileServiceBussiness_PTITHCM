# customer repositorie
from app.database import db_instance
from app.models.customer import Customer


class CustomerRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_customers", fetchall=True)
            customers = []

            for row in result:
                customer = Customer()
                customer.id = row.get("id")
                customer.full_name = row.get("full_name")
                customer.is_active = True if row.get("is_active") else False
                customer.account_id = row.get("account_id")
                customer.card_id = row.get("card_id")
                customers.append(customer.to_dict())

            return customers
        except Exception as e:
            print(f"Lỗi khi lấy danh sách khách hàng: {e}")
            return []

    @staticmethod
    def get_by_id(customer_id):
        try:
            result = db_instance.execute(
                "CALL GetCustomerById(%s)", (customer_id,), fetchone=True
            )
            if result:
                customer = Customer()
                customer.id = result.get("id")
                customer.full_name = result.get("full_name")
                customer.is_active = result.get("is_active")
                customer.account_id = result.get("account_id")
                customer.card_id = result.get("card_id")
                return customer
            return None
        except Exception as e:
            print(f"Lỗi khi lấy khách hàng theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Customer):
        try:
            result = db_instance.execute(
                "CALL AddCustomer(%s, %s, %s, %s)",
                (data.full_name, data.is_active, data.account_id, data.card_id),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (insert): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm khách hàng: {e}")
            return False

    @staticmethod
    def update(customer_id, data: Customer):
        try:
            result = db_instance.execute(
                "CALL UpdateCustomer(%s, %s, %s, %s, %s)",
                (
                    customer_id,
                    data.full_name,
                    data.is_active,
                    data.account_id,
                    data.card_id,
                ),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (update): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật khách hàng: {e}")
            return False

    @staticmethod
    def delete(customer_id):
        try:
            result = db_instance.execute(
                "CALL DeleteCustomer(%s)", (customer_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (delete): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa khách hàng: {e}")
            return False
