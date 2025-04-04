from typing import Optional
from datetime import datetime, date


class Contract:
    __id: Optional[int]
    __created_at: Optional[datetime]
    __contents: Optional[str]
    __title: Optional[str]
    __subscriber: Optional[int]
    __start_date: Optional[date]
    __end_date: Optional[date]
    __is_active: Optional[bool]
    __subscriber_id: Optional[int]

    def __init__(
        self,
        id=None,
        created_at=None,
        contents=None,
        title=None,
        subscriber=None,
        start_date=None,
        end_date=None,
        is_active=True,
        subscriber_id=None,
    ):
        self.id = id
        self.created_at = created_at or datetime.utcnow()
        self.contents = contents
        self.title = title
        self.subscriber = subscriber
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.subscriber_id = subscriber_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("created_at must be a datetime object")
        self.__created_at = value

    @property
    def contents(self):
        return self.__contents

    @contents.setter
    def contents(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("contents must be a string")
        self.__contents = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("title must be a string")
        self.__title = value

    @property
    def subscriber(self):
        return self.__subscriber

    @subscriber.setter
    def subscriber(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("subscriber must be an integer")
        self.__subscriber = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        if value is not None and not isinstance(value, date):
            raise ValueError("start_date must be a date object")
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        if value is not None and not isinstance(value, date):
            raise ValueError("end_date must be a date object")
        self.__end_date = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_active must be a boolean")
        self.__is_active = value

    @property
    def subscriber_id(self):
        return self.__subscriber_id

    @subscriber_id.setter
    def subscriber_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("subscriber_id must be an integer")
        self.__subscriber_id = value

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "contents": self.contents,
            "title": self.title,
            "subscriber": self.subscriber,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_active": self.is_active,
            "subscriber_id": self.subscriber_id,
        }
