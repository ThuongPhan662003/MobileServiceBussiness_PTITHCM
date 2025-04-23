from app.database import db_instance
from app.models.customer import Customer


class CustomerRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_customers", fetchall=True)
            customers = []
            for row in result[0]:
                customer = Customer()
                customer.id = int(row.get("id")) if row.get("id") is not None else None
                customer.full_name = row.get("full_name")
                customer.card_id = row.get("card_id")
                customer.is_active = bool(row.get("is_active"))
                customers.append(customer.to_dict())
            return customers
        except Exception as e:
            print(f"Lỗi khi lấy danh sách khách hàng: {e}")
            return []

    @staticmethod
    def get_by_id(customer_id):
        try:
            result = db_instance.execute(
                "CALL GetCustomerById(%s)", (customer_id,),
                fetchone=True, commit=True
            )
            if result:
                customer = Customer()
                customer.id = result.get("id")
                customer.full_name = result.get("full_name")
                customer.is_active = True if result.get("is_active") == 1 else False
                customer.card_id = result.get("card_id")
                return customer
            else:
                return None
        except Exception as e:
            print(f"Lỗi khi lấy khách hàng theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Customer):
        try:
            result = db_instance.execute(
                "CALL AddCustomer(%s, %s)",
                (data.full_name,  data.card_id),
                fetchone=True, commit=True
            )
            if result.get("error"):
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm khách hàng: {e}")
            return False

    @staticmethod
    def update(customer_id, data: Customer):
        try:
            result = db_instance.execute(
                "CALL UpdateCustomer(%s, %s, %s, %s)",
                (customer_id, data.full_name, data.is_active, data.card_id),
                fetchone=True
            )
            if result.get("error"):
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
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa khách hàng: {e}")
            return False

    @staticmethod
    def exists_by_card_id(card_id: str, exclude_customer_id=None):
        try:
            query = "SELECT COUNT(*) AS count FROM customers WHERE card_id = %s"
            params = [card_id]

            if exclude_customer_id is not None:
                query += " AND id != %s"
                params.append(exclude_customer_id)

            result = db_instance.execute(query, tuple(params), fetchone=True)
            return result.get("count", 0) > 0
        except Exception as e:
            print(f"Lỗi khi kiểm tra card_id tồn tại: {e}")
            return False
