from typing import Optional

from . import *

class PermissionDetail:
    __role_group_id: Optional["RoleGroup"]
    __account_id: Optional["Account"]

    def __init__(self, role_group_id=None, account_id=None):
        self.role_group_id = role_group_id
        self.account_id = account_id

    @property
    def role_group_id(self):
        return self.__role_group_id

    @role_group_id.setter
    def role_group_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("role_group_id must be an integer")
        self.__role_group_id = value

    @property
    def account_id(self):
        return self.__account_id

    @account_id.setter
    def account_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("account_id must be an integer")
        self.__account_id = value

    def to_dict(self):
        return {
            "role_group_id": self.role_group_id.to_dict(),
            "account_id": self.account_id.to_dict(),
        }

    @staticmethod
    def get_accounts_by_role_group(role_group_id, permissions: list):
        """
        Lấy danh sách account_id theo role_group_id từ danh sách PermissionDetail truyền vào.
        """
        if not isinstance(permissions, list):
            raise ValueError("permissions must be a list of PermissionDetail objects")

        return [
            p.account_id
            for p in permissions
            if isinstance(p, PermissionDetail) and p.role_group_id == role_group_id
        ]
