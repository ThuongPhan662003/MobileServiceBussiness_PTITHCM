from typing import Optional, List
from datetime import date

from . import *


class Staff:
    __id: Optional[int]
    __full_name: Optional[str]
    __card_id: Optional[str]
    __phone: Optional[str]
    __email: Optional[str]
    __is_active: Optional[bool]
    __gender: Optional[str]
    __birthday: Optional[date]
    __account_id: Optional["Account"]

    def __init__(
        self,
        id=None,
        full_name=None,
        card_id=None,
        phone=None,
        email=None,
        is_active=True,
        gender=None,
        birthday=None,
        account_id=None,
    ):
        self.id = id
        self.full_name = full_name
        self.card_id = card_id
        self.phone = phone
        self.email = email
        self.is_active = is_active
        self.gender = gender
        self.birthday = birthday
        self.account_id = account_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("full_name must be a string")
        self.__full_name = value

    @property
    def card_id(self):
        return self.__card_id

    @card_id.setter
    def card_id(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("card_id must be a string")
        self.__card_id = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("phone must be a string")
        self.__phone = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("email must be a string")
        self.__email = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_active must be a boolean")
        self.__is_active = value

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        if value is not None and value not in ("Nam", "Nữ", "Khác"):
            raise ValueError("gender must be 'Nam', 'Nữ', or 'Khác'")
        self.__gender = value

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, value):
        if value is not None and not isinstance(value, date):
            raise ValueError("birthday must be a date")
        self.__birthday = value

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
            "id": self.id,
            #
            # "full_name": self.full_name,
            # "card_id": self.card_id,
            # "phone": self.phone,
            # "email": self.email,
            # "is_active": self.is_active,
            # "gender": self.gender,
            # "birthday": self.birthday.isoformat() if self.birthday else None,
            # "account_id": self.account_id.to_dict() if hasattr(self.account_id, 'to_dict') else self.account_id,

            "full_name": self.full_name or "",
            "card_id": self.card_id or "",
            "phone": self.phone or "",
            "email": self.email or "",
            "is_active": self.is_active if self.is_active is not None else False,
            "gender": self.gender or "",
            "birthday": self.birthday.isoformat() if self.birthday else "",
            "account_id": self.account_id.to_dict() if self.account_id else {},

        }

    # @staticmethod
    # def get_staffs_by_role_group(
    #     role_group_id: int, staffs: List["Staff"], permissions: List["PermissionDetail"]
    # ) -> List["Staff"]:
    #     """
    #     Trả về danh sách Staff có account_id thuộc role_group_id, dựa trên PermissionDetail.
    #     """
    #     account_ids = PermissionDetail.get_accounts_by_role_group(
    #         role_group_id, permissions
    #     )
    #     return [staff for staff in staffs if staff.account_id in account_ids]
