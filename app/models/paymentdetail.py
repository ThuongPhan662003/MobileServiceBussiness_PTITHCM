from typing import Optional
from decimal import Decimal

from . import *

class PaymentDetail:
    __id: Optional[int]
    __payment_id: Optional["Payment"]
    __free_data: Optional[Decimal]
    __free_ON_a_call: Optional[Decimal]
    __free_OffN_a_call: Optional[Decimal]
    __free_ON_call: Optional[Decimal]
    __free_OffN_call: Optional[Decimal]
    __free_ON_SMS: Optional[int]
    __free_OffN_SMS: Optional[int]
    __ON_a_call_cost: Optional[Decimal]
    __ON_SMS_cost: Optional[Decimal]

    def __init__(
        self,
        id=None,
        payment_id=None,
        free_data=None,
        free_ON_a_call=None,
        free_OffN_a_call=None,
        free_ON_call=None,
        free_OffN_call=None,
        free_ON_SMS=None,
        free_OffN_SMS=None,
        ON_a_call_cost=None,
        ON_SMS_cost=None,
    ):
        self.id = id
        self.payment_id = payment_id
        self.free_data = free_data
        self.free_ON_a_call = free_ON_a_call
        self.free_OffN_a_call = free_OffN_a_call
        self.free_ON_call = free_ON_call
        self.free_OffN_call = free_OffN_call
        self.free_ON_SMS = free_ON_SMS
        self.free_OffN_SMS = free_OffN_SMS
        self.ON_a_call_cost = ON_a_call_cost
        self.ON_SMS_cost = ON_SMS_cost

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def payment_id(self):
        return self.__payment_id

    @payment_id.setter
    def payment_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("payment_id must be an integer")
        self.__payment_id = value

    @property
    def free_data(self):
        return self.__free_data

    @free_data.setter
    def free_data(self, value):
        self.__free_data = Decimal(value)

    @property
    def free_ON_a_call(self):
        return self.__free_ON_a_call

    @free_ON_a_call.setter
    def free_ON_a_call(self, value):
        self.__free_ON_a_call = Decimal(value)

    @property
    def free_OffN_a_call(self):
        return self.__free_OffN_a_call

    @free_OffN_a_call.setter
    def free_OffN_a_call(self, value):
        self.__free_OffN_a_call = Decimal(value)

    @property
    def free_ON_call(self):
        return self.__free_ON_call

    @free_ON_call.setter
    def free_ON_call(self, value):
        self.__free_ON_call = Decimal(value)

    @property
    def free_OffN_call(self):
        return self.__free_OffN_call

    @free_OffN_call.setter
    def free_OffN_call(self, value):
        self.__free_OffN_call = Decimal(value)

    @property
    def free_ON_SMS(self):
        return self.__free_ON_SMS

    @free_ON_SMS.setter
    def free_ON_SMS(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("free_ON_SMS must be an integer")
        self.__free_ON_SMS = value

    @property
    def free_OffN_SMS(self):
        return self.__free_OffN_SMS

    @free_OffN_SMS.setter
    def free_OffN_SMS(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("free_OffN_SMS must be an integer")
        self.__free_OffN_SMS = value

    @property
    def ON_a_call_cost(self):
        return self.__ON_a_call_cost

    @ON_a_call_cost.setter
    def ON_a_call_cost(self, value):
        self.__ON_a_call_cost = Decimal(value)

    @property
    def ON_SMS_cost(self):
        return self.__ON_SMS_cost

    @ON_SMS_cost.setter
    def ON_SMS_cost(self, value):
        self.__ON_SMS_cost = Decimal(value)

    def to_dict(self):
        return {
            "id": self.id,
            "payment_id": self.payment_id.to_dict(),
            "free_data": float(self.free_data) if self.free_data is not None else None,
            "free_ON_a_call": (
                float(self.free_ON_a_call) if self.free_ON_a_call is not None else None
            ),
            "free_OffN_a_call": (
                float(self.free_OffN_a_call)
                if self.free_OffN_a_call is not None
                else None
            ),
            "free_ON_call": (
                float(self.free_ON_call) if self.free_ON_call is not None else None
            ),
            "free_OffN_call": (
                float(self.free_OffN_call) if self.free_OffN_call is not None else None
            ),
            "free_ON_SMS": self.free_ON_SMS,
            "free_OffN_SMS": self.free_OffN_SMS,
            "ON_a_call_cost": (
                float(self.ON_a_call_cost) if self.ON_a_call_cost is not None else None
            ),
            "ON_SMS_cost": (
                float(self.ON_SMS_cost) if self.ON_SMS_cost is not None else None
            ),
        }
