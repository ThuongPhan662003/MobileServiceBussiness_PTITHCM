from typing import Optional
from datetime import datetime, date


class Subscription:
    __id: Optional[int]
    __plan_id: Optional[int]
    __subscriber_id: Optional[int]
    __created_at: Optional[datetime]
    __expiration_date: Optional[datetime]
    __renewal_total: Optional[int]
    __is_renewal: Optional[bool]
    __cancel_at: Optional[datetime]
    __activation_date: Optional[date]

    def __init__(
        self,
        id=None,
        plan_id=None,
        subscriber_id=None,
        created_at=None,
        expiration_date=None,
        renewal_total=0,
        is_renewal=True,
        cancel_at=None,
        activation_date=None,
    ):
        self.id = id
        self.plan_id = plan_id
        self.subscriber_id = subscriber_id
        self.created_at = created_at or datetime.utcnow()
        self.expiration_date = expiration_date or datetime.utcnow()
        self.renewal_total = renewal_total
        self.is_renewal = is_renewal
        self.cancel_at = cancel_at
        self.activation_date = activation_date

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def plan_id(self):
        return self.__plan_id

    @plan_id.setter
    def plan_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("plan_id must be an integer")
        self.__plan_id = value

    @property
    def subscriber_id(self):
        return self.__subscriber_id

    @subscriber_id.setter
    def subscriber_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("subscriber_id must be an integer")
        self.__subscriber_id = value

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("created_at must be datetime")
        self.__created_at = value

    @property
    def expiration_date(self):
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("expiration_date must be datetime")
        self.__expiration_date = value

    @property
    def renewal_total(self):
        return self.__renewal_total

    @renewal_total.setter
    def renewal_total(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("renewal_total must be an integer")
        self.__renewal_total = value

    @property
    def is_renewal(self):
        return self.__is_renewal

    @is_renewal.setter
    def is_renewal(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_renewal must be a boolean")
        self.__is_renewal = value

    @property
    def cancel_at(self):
        return self.__cancel_at

    @cancel_at.setter
    def cancel_at(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("cancel_at must be datetime")
        self.__cancel_at = value

    @property
    def activation_date(self):
        return self.__activation_date

    @activation_date.setter
    def activation_date(self, value):
        if value is not None and not isinstance(value, date):
            raise ValueError("activation_date must be a date")
        self.__activation_date = value

    def to_dict(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "subscriber_id": self.subscriber_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expiration_date": (
                self.expiration_date.isoformat() if self.expiration_date else None
            ),
            "renewal_total": self.renewal_total,
            "is_renewal": self.is_renewal,
            "cancel_at": self.cancel_at.isoformat() if self.cancel_at else None,
            "activation_date": (
                self.activation_date.isoformat() if self.activation_date else None
            ),
        }
