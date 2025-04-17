from app.repositories.account_repository import AccountRepository
from app.models.account import Account


class AccountService:
    @staticmethod
    def get_all_accounts():
        return AccountRepository.get_all()

    @staticmethod
    def get_account_by_id(account_id):
        return AccountRepository.get_by_id(account_id)

    @staticmethod
    def check_login(username, password):
        print(
            "service",
            AccountRepository.check_login_by_username_and_password(username, password)[
                "data"
            ].to_dict(),
        )
        return AccountRepository.check_login_by_username_and_password(
            username, password
        )

    @staticmethod
    def create_account(data: dict):
        try:
            account = Account(
                username=data.get("username"),
                password=data.get("password"),
                is_active=data.get("is_active", True),
            )
            result = AccountRepository.insert(account)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
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
