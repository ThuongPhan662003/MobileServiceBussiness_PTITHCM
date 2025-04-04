from typing import Optional
from datetime import datetime


class UsageLog:
    __id: Optional[int]
    __type: Optional[str]
    __usage_value: Optional[int]
    __subscriber_id: Optional[int]
    __start_date: Optional[datetime]
    __end_date: Optional[datetime]

    def __init__(
        self,
        id=None,
        type=None,
        usage_value=None,
        subscriber_id=None,
        start_date=None,
        end_date=None,
    ):
        self.id = id
        self.type = type
        self.usage_value = usage_value
        self.subscriber_id = subscriber_id
        self.start_date = start_date
        self.end_date = end_date

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("type must be a string")
        self.__type = value

    @property
    def usage_value(self):
        return self.__usage_value

    @usage_value.setter
    def usage_value(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("usage_value must be an integer")
        self.__usage_value = value

    @property
    def subscriber_id(self):
        return self.__subscriber_id

    @subscriber_id.setter
    def subscriber_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("subscriber_id must be an integer")
        self.__subscriber_id = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("start_date must be a datetime object")
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("end_date must be a datetime object")
        self.__end_date = value

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "usage_value": self.usage_value,
            "subscriber_id": self.subscriber_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }
