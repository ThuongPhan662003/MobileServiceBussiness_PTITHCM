from app.database import db_instance
from app.models.account import Account


class AccountRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_accounts", fetchall=True)
            print(result)
            accounts = []

            for row in result:
                account = Account()
                account.id = row.get("id")
                account.username = row.get("username")
                account.password = row.get("password")
                account.is_active = True if row.get("is_active") else False
                accounts.append(account.to_dict())

            return accounts
        except Exception as e:
            print(f"Lỗi khi lấy danh sách account: {e}")
            return []

    @staticmethod
    def get_by_id(account_id):
        try:
            result = db_instance.execute(
                "CALL GetAccountById(%s)", (account_id,), fetchone=True
            )

            if result:
                account = Account()
                account.id = result.get("id")
                account.username = result.get("username")
                account.password = result.get("password")
                account.is_active = result.get("is_active")
                return account
            return None
        except Exception as e:
            print(f"Lỗi khi lấy account theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Account):
        try:
            result = db_instance.execute(
                "CALL CreateAccount(%s, %s, %s)",
                (data.username, data.password, data.is_active),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (insert): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi thêm account: {e}")
            return False

    @staticmethod
    def update(account_id, data: Account):
        try:
            result = db_instance.execute(
                "CALL UpdateAccount(%s, %s, %s, %s)",
                (account_id, data.username, data.password, data.is_active),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (update): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật account: {e}")
            return False

    @staticmethod
    def delete(account_id):
        try:
            result = db_instance.execute(
                "CALL DeleteAccount(%s)", (account_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (delete): {result['error']}")
                return result["error"]
            return result.get("success", False)
        except Exception as e:
            print(f"Lỗi khi xóa account: {e}")
            return False
