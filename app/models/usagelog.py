from typing import Optional
from datetime import datetime
from datetime import datetime, date


class UsageLog:
    __id: Optional[int]
    __type: Optional[str]
    __usage_value: Optional[int]
    __subscriber_id: Optional["Subscriber"]
    __start_date: Optional[datetime]
    __end_date: Optional[datetime]
    __by_from: Optional[str]
    __to: Optional[str]
    __contents: Optional[str]

    def __init__(
        self,
        id=None,
        type=None,
        usage_value=None,
        subscriber_id=None,
        start_date=None,
        end_date=None,
        by_from=None,
        to=None,
        contents=None,
    ):
        self.id = id
        self.type = type
        self.usage_value = usage_value
        self.subscriber_id = subscriber_id
        self.start_date = start_date
        self.end_date = end_date
        self.by_from = by_from
        self.to = to
        self.contents = contents

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
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("subscriber_id must be an integer")
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
        if value is not None:
            if isinstance(value, datetime):
                self.__end_date = value
            elif isinstance(value, date):
                self.__end_date = datetime.combine(value, datetime.min.time())
            else:
                raise ValueError("end_date must be a datetime or date object")
        else:
            self.__end_date = None

    @property
    def by_from(self):
        return self.__by_from

    @by_from.setter
    def by_from(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("by_from must be a string")
        self.__by_from = value

    @property
    def to(self):
        return self.__to

    @to.setter
    def to(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("to must be a string")
        self.__to = value

    @property
    def contents(self):
        return self.__contents

    @contents.setter
    def contents(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("contents must be a string")
        self.__contents = value

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "usage_value": self.usage_value,
            "subscriber_id": self.subscriber_id,  # không gọi to_dict()
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "by_from": self.by_from,
            "to": self.to,
            "contents": self.contents,
        }
