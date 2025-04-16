from typing import Optional, List

from flask_login import UserMixin


class Account(UserMixin):
    __id: Optional[int]
    __username: Optional[str]
    __password: Optional[str]
    __is_active: Optional[bool]

    def __init__(
        self,
        id=None,
        username=None,
        password=None,
        is_active=True,
    ):
        self.id = id
        self.username = username
        self.password = password
        self.is_active = is_active

    @property
    def id(self):
        return self.__id

    def get_id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("username must be a string")
        self.__username = value

    def get_full_name(self):
        return self.__full_name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("password must be a string")
        self.__password = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_active must be a boolean")
        self.__is_active = value

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "is_active": self.is_active,
        }
