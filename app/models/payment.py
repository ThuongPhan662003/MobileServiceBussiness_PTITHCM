from typing import Optional
from decimal import Decimal
from datetime import datetime


class Payment:
    __id: Optional[int]
    __subscription_id: Optional[int]
    __payment_date: Optional[datetime]
    __total_amount: Optional[Decimal]
    __payment_method: Optional[str]
    __is_paid: Optional[bool]
    __due_date: Optional[datetime]

    def __init__(
        self,
        id=None,
        subscription_id=None,
        payment_date=None,
        total_amount=None,
        payment_method=None,
        is_paid=False,
        due_date=None,
    ):
        self.id = id
        self.subscription_id = subscription_id
        self.payment_date = payment_date or datetime.utcnow()
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.is_paid = is_paid
        self.due_date = due_date

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def subscription_id(self):
        return self.__subscription_id

    @subscription_id.setter
    def subscription_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("subscription_id must be an integer")
        self.__subscription_id = value

    @property
    def payment_date(self):
        return self.__payment_date

    @payment_date.setter
    def payment_date(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("payment_date must be a datetime object")
        self.__payment_date = value

    @property
    def total_amount(self):
        return self.__total_amount

    @total_amount.setter
    def total_amount(self, value):
        if value is not None and not isinstance(value, (Decimal, float, int)):
            raise ValueError("total_amount must be a number or Decimal")
        self.__total_amount = Decimal(value)

    @property
    def payment_method(self):
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("payment_method must be a string")
        self.__payment_method = value

    @property
    def is_paid(self):
        return self.__is_paid

    @is_paid.setter
    def is_paid(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_paid must be a boolean")
        self.__is_paid = value

    @property
    def due_date(self):
        return self.__due_date

    @due_date.setter
    def due_date(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("due_date must be a datetime object")
        self.__due_date = value

    def to_dict(self):
        return {
            "id": self.id,
            "subscription_id": self.subscription_id,
            "payment_date": (
                self.payment_date.isoformat() if self.payment_date else None
            ),
            "total_amount": (
                float(self.total_amount) if self.total_amount is not None else None
            ),
            "payment_method": self.payment_method,
            "is_paid": self.is_paid,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }
