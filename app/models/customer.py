from typing import Optional, List




class Customer:
    __id: Optional[int]
    __full_name: Optional[str]
    __is_active: Optional[bool]
    __account_id: Optional[int]
    __card_id: Optional[str]
    __subscribers: Optional[List["Subscriber"]]

    def __init__(
        self,
        id=None,
        full_name=None,
        is_active=True,
        account_id=None,
        card_id=None,
        subscribers=None,
    ):
        self.id = id
        self.full_name = full_name
        self.is_active = is_active
        self.account_id = account_id
        self.card_id = card_id
        self.subscribers = subscribers or []

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
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_active must be a boolean")
        self.__is_active = value

    @property
    def account_id(self):
        return self.__account_id

    @account_id.setter
    def account_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("account_id must be an integer")
        self.__account_id = value

    @property
    def card_id(self):
        return self.__card_id

    @card_id.setter
    def card_id(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("card_id must be a string")
        self.__card_id = value

    @property
    def subscribers(self):
        return self.__subscribers

    @subscribers.setter
    def subscribers(self, value):
        if value is not None and not isinstance(value, list):
            raise ValueError("subscribers must be a list")
        self.__subscribers = value

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "account_id": self.account_id,
            "card_id": self.card_id,
            "subscribers": (
                [s.to_dict() for s in self.subscribers] if self.subscribers else []
            ),
        }
