from typing import Optional
from decimal import Decimal
from datetime import datetime

from . import *

class Plan:
    __id: Optional[int]
    __code: Optional[str]
    __price: Optional[Decimal]
    __description: Optional[str]
    __service_id: Optional["Service"]
    __is_active: Optional[bool]
    __renewal_syntax: Optional[str]
    __registration_syntax: Optional[str]
    __cancel_syntax: Optional[str]
    __free_data: Optional[int]
    __free_on_network_a_call: Optional[int]
    __free_on_network_call: Optional[int]
    __free_on_network_SMS: Optional[int]
    __free_off_network_a_call: Optional[int]
    __free_off_network_call: Optional[int]
    __free_off_network_SMS: Optional[int]
    __auto_renew: Optional[bool]
    __staff_id: Optional["Staff"]
    __created_at: Optional[datetime]
    __updated_at: Optional[datetime]
    __maximum_on_network_call: Optional[int]

    def __init__(
        self,
        id=None,
        code=None,
        price=None,
        description=None,
        service_id=None,
        is_active=True,
        renewal_syntax=None,
        registration_syntax=None,
        cancel_syntax=None,
        free_data=0,
        free_on_network_a_call=0,
        free_on_network_call=0,
        free_on_network_SMS=0,
        free_off_network_a_call=0,
        free_off_network_call=0,
        free_off_network_SMS=0,
        auto_renew=False,
        staff_id=None,
        created_at=None,
        updated_at=None,
        maximum_on_network_call=0,
    ):
        self.id = id
        self.code = code
        self.price = price
        self.description = description
        self.service_id = service_id
        self.is_active = is_active
        self.renewal_syntax = renewal_syntax
        self.registration_syntax = registration_syntax
        self.cancel_syntax = cancel_syntax
        self.free_data = free_data
        self.free_on_network_a_call = free_on_network_a_call
        self.free_on_network_call = free_on_network_call
        self.free_on_network_SMS = free_on_network_SMS
        self.free_off_network_a_call = free_off_network_a_call
        self.free_off_network_call = free_off_network_call
        self.free_off_network_SMS = free_off_network_SMS
        self.auto_renew = auto_renew
        self.staff_id = staff_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.maximum_on_network_call = maximum_on_network_call

    # --- Properties & Setters ---

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
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value is not None and not isinstance(value, (Decimal, float, int)):
            raise ValueError("price must be a number")
        self.__price = Decimal(value)

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("description must be a string")
        self.__description = value

    @property
    def service_id(self):
        return self.__service_id

    @service_id.setter
    def service_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("service_id must be an integer")
        self.__service_id = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_active must be a boolean")
        self.__is_active = value

    @property
    def renewal_syntax(self):
        return self.__renewal_syntax

    @renewal_syntax.setter
    def renewal_syntax(self, value):
        self.__renewal_syntax = value

    @property
    def registration_syntax(self):
        return self.__registration_syntax

    @registration_syntax.setter
    def registration_syntax(self, value):
        self.__registration_syntax = value

    @property
    def cancel_syntax(self):
        return self.__cancel_syntax

    @cancel_syntax.setter
    def cancel_syntax(self, value):
        self.__cancel_syntax = value

    @property
    def free_data(self):
        return self.__free_data

    @free_data.setter
    def free_data(self, value):
        self.__free_data = int(value)

    @property
    def free_on_network_a_call(self):
        return self.__free_on_network_a_call

    @free_on_network_a_call.setter
    def free_on_network_a_call(self, value):
        self.__free_on_network_a_call = int(value)

    @property
    def free_on_network_call(self):
        return self.__free_on_network_call

    @free_on_network_call.setter
    def free_on_network_call(self, value):
        self.__free_on_network_call = int(value)

    @property
    def free_on_network_SMS(self):
        return self.__free_on_network_SMS

    @free_on_network_SMS.setter
    def free_on_network_SMS(self, value):
        self.__free_on_network_SMS = int(value)

    @property
    def free_off_network_a_call(self):
        return self.__free_off_network_a_call

    @free_off_network_a_call.setter
    def free_off_network_a_call(self, value):
        self.__free_off_network_a_call = int(value)

    @property
    def free_off_network_call(self):
        return self.__free_off_network_call

    @free_off_network_call.setter
    def free_off_network_call(self, value):
        self.__free_off_network_call = int(value)

    @property
    def free_off_network_SMS(self):
        return self.__free_off_network_SMS

    @free_off_network_SMS.setter
    def free_off_network_SMS(self, value):
        self.__free_off_network_SMS = int(value)

    @property
    def auto_renew(self):
        return self.__auto_renew

    @auto_renew.setter
    def auto_renew(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("auto_renew must be a boolean")
        self.__auto_renew = value

    @property
    def staff_id(self):
        return self.__staff_id

    @staff_id.setter
    def staff_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("staff_id must be an integer")
        self.__staff_id = value

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        if not isinstance(value, datetime):
            raise ValueError("created_at must be datetime")
        self.__created_at = value

    @property
    def updated_at(self):
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, value):
        if not isinstance(value, datetime):
            raise ValueError("updated_at must be datetime")
        self.__updated_at = value

    @property
    def maximum_on_network_call(self):
        return self.__maximum_on_network_call

    @maximum_on_network_call.setter
    def maximum_on_network_call(self, value):
        self.__maximum_on_network_call = int(value)

    # --- Export as dict ---

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "price": float(self.price) if self.price else 0,
            "description": self.description,
            "service_id": self.service_id.to_dict(),
            "is_active": self.is_active,
            "renewal_syntax": self.renewal_syntax,
            "registration_syntax": self.registration_syntax,
            "cancel_syntax": self.cancel_syntax,
            "free_data": self.free_data,
            "free_on_network_a_call": self.free_on_network_a_call,
            "free_on_network_call": self.free_on_network_call,
            "free_on_network_SMS": self.free_on_network_SMS,
            "free_off_network_a_call": self.free_off_network_a_call,
            "free_off_network_call": self.free_off_network_call,
            "free_off_network_SMS": self.free_off_network_SMS,
            "auto_renew": self.auto_renew,
            "staff_id": self.staff_id.to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "maximum_on_network_call": self.maximum_on_network_call,
        }
