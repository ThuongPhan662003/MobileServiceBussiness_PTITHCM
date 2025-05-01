from typing import Optional
from datetime import date


class Voucher:
    __id: Optional[int]
    __code: Optional[str]
    __description: Optional[str]
    __conandpromo: Optional[str]
    __start_date: Optional[date]
    __end_date: Optional[date]
    __usage_limit: Optional[int]
    __remaining_count: Optional[int]
    __is_active: Optional[bool]
    __staff_id: Optional["Staff"]
    __packages: Optional[str]

    def __init__(
        self,
        id=None,
        code=None,
        description=None,
        conandpromo=None,
        start_date=None,
        end_date=None,
        usage_limit=None,
        remaining_count=0,
        is_active=True,
        staff_id=None,
        packages=None,
    ):
        self.id = id
        self.code = code
        self.description = description
        self.conandpromo = conandpromo
        self.start_date = start_date
        self.end_date = end_date
        self.usage_limit = usage_limit
        self.remaining_count = remaining_count
        self.is_active = is_active
        self.staff_id = staff_id
        self.packages = packages

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("code must be a string")
        self.__code = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("description must be a string")
        self.__description = value

    @property
    def conandpromo(self):
        return self.__conandpromo

    @conandpromo.setter
    def conandpromo(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("conandpromo must be a string")
        self.__conandpromo = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        if value is not None and not isinstance(value, date):
            raise ValueError("start_date must be a date")
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        if value is not None and not isinstance(value, date):
            raise ValueError("end_date must be a date")
        self.__end_date = value

    @property
    def usage_limit(self):
        return self.__usage_limit

    @usage_limit.setter
    def usage_limit(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("usage_limit must be an integer")
        self.__usage_limit = value

    @property
    def remaining_count(self):
        return self.__remaining_count

    @remaining_count.setter
    def remaining_count(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("remaining_count must be an integer")
        self.__remaining_count = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_active must be a boolean")
        self.__is_active = value

    @property
    def staff_id(self):
        return self.__staff_id

    @staff_id.setter
    def staff_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("staff_id must be an integer")
        self.__staff_id = value

    @property
    def packages(self):
        return self.__packages

    @packages.setter
    def packages(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("packages must be a string")
        self.__packages = value

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "description": self.description,
            "conandpromo": self.conandpromo,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "usage_limit": self.usage_limit,
            "remaining_count": self.remaining_count,
            "is_active": self.is_active,
            "staff_id": (
                self.staff_id.to_dict()
                if hasattr(self.staff_id, "to_dict")
                else self.staff_id
            ),
            "packages": self.packages,
        }
