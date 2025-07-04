from app.repositories.account_repository import AccountRepository
from app.models.account import Account
from werkzeug.security import generate_password_hash


class AccountService:
    @staticmethod
    def get_all_accounts():
        return AccountRepository.get_all()

    @staticmethod
    def get_account_by_id(account_id):
        return AccountRepository.get_by_id(account_id)

    @staticmethod
    def check_login(username, password):
        return AccountRepository.check_login_by_username_and_password(
            username, password
        )

    @staticmethod
    def create_account(data: dict):
        try:
            print("data", data)
            account = Account(
                username=data.get("username"),
                password=data.get("password"),
                is_active=data.get("is_active", True),
            )
            print("tài khoản", account.to_dict())
            result = AccountRepository.insert(account)
            print("kết quả", result)
            if result["success"] is True:
                return result
            else:
                return result
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_account(account_id, data: dict):
        try:
            account = Account(
                username=data.get("username"),
                password=data.get("password"),
                is_active=data.get("is_active", True),
            )
            result = AccountRepository.update(account_id, account)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_account(account_id):
        try:
            result = AccountRepository.delete(account_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def reset_password_by_email_or_phone(identifier: str, new_password: str):
        hashed_password = generate_password_hash(new_password)

        result = AccountRepository.update_password_by_email_or_phone(
            identifier, hashed_password
        )

        if not result.get("success"):
            raise Exception(result.get("message"))

        return result
