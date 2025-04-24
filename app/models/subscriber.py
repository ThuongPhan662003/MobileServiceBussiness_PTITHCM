from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


class Subscriber:
    __id: Optional[int]
    __phone_number: Optional[str]
    __main_balance: Optional[Decimal]
    __activation_date: Optional[date]
    __expiration_date: Optional[date]
    __is_active: Optional[bool]
    __customer_id: Optional[int]
    __warning_date: Optional[datetime]

    __contracts: Optional[List["Contract"]]
    __subscriptions: Optional[List["Subscription"]]
    __usage_logs: Optional[List["UsageLog"]]
    __subscriber: Optional[str]
    __account_id: Optional["Account"]

    def __init__(
        self,
        id=None,
        phone_number=None,
        main_balance=Decimal("0.00"),
        activation_date=None,
        expiration_date=None,
        is_active=True,
        customer_id=None,
        warning_date=None,
        contracts=None,
        subscriptions=None,
        usage_logs=None,
        subscriber=None,
        account_id=None,
    ):
        self.id = id
        self.phone_number = phone_number
        self.main_balance = main_balance
        self.activation_date = activation_date
        self.expiration_date = expiration_date
        self.is_active = is_active
        self.customer_id = customer_id
        self.warning_date = warning_date
        self.account_id = account_id
        self.contracts = contracts or []
        self.subscriptions = subscriptions or []
        self.usage_logs = usage_logs or []
        self.account_id = account_id
        self.subscriber = subscriber

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("phone_number must be a string")
        self.__phone_number = value

    @property
    def main_balance(self):
        return self.__main_balance

    @main_balance.setter
    def main_balance(self, value):
        if value is not None and not isinstance(value, (Decimal, float, int)):
            raise ValueError("main_balance must be a number")
        self.__main_balance = Decimal(value)

    @property
    def activation_date(self):
        return self.__activation_date

    @activation_date.setter
    def activation_date(self, value):
        if value is not None and not isinstance(value, date):
            raise ValueError("activation_date must be a date")
        self.__activation_date = value

    @property
    def expiration_date(self):
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value):
        if value is not None and not isinstance(value, date):
            raise ValueError("expiration_date must be a date")
        self.__expiration_date = value

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("is_active must be a boolean")
        self.__is_active = value

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("customer_id must be an integer")
        self.__customer_id = value

    @property
    def warning_date(self):
        return self.__warning_date

    @warning_date.setter
    def warning_date(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("warning_date must be a datetime")
        self.__warning_date = value

    @property
    def subscriber_type(self):
        return self.__subscriber_type

    @subscriber_type.setter
    def subscriber_type(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("subscriber_type must be a string")
        self.__subscriber_type = value

    @property
    def account_id(self):
        return self.__account_id

    @account_id.setter
    def account_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("account_id must be an integer")
        self.__account_id = value

    @property
    def contracts(self):
        return self.__contracts

    @contracts.setter
    def contracts(self, value):
        self.__contracts = value

    @property
    def subscriber(self):
        return self.__subscriber

    @subscriber.setter
    def subscriber(self, value):
        # if value is not None and not isinstance(value, list):
        #     raise ValueError("contracts must be a list")
        self.__subscriber = value

    @property
    def account_id(self):
        return self.__account_id

    @account_id.setter
    def account_id(self, value):
        # if value is not None and not isinstance(value, list):
        #     raise ValueError("contracts must be a list")
        self.__account_id = value

    @property
    def subscriber(self):
        return self.__subscriber

    @subscriber.setter
    def subscriber(self, value):
        # if value is not None and not isinstance(value, list):
        #     raise ValueError("contracts must be a list")
        self.__subscriber = value

    @property
    def account_id(self):
        return self.__account_id

    @account_id.setter
    def account_id(self, value):
        # if value is not None and not isinstance(value, list):
        #     raise ValueError("contracts must be a list")
        self.__account_id = value

    @property
    def subscriptions(self):
        return self.__subscriptions

    @subscriptions.setter
    def subscriptions(self, value):
        self.__subscriptions = value

    @property
    def usage_logs(self):
        return self.__usage_logs

    @usage_logs.setter
    def usage_logs(self, value):
        self.__usage_logs = value

    def to_dict(self):
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            # <<<<<<< HEAD
            #             "main_balance": float(self.main_balance) if self.main_balance else 0.0,
            #             "activation_date": self.activation_date.isoformat() if self.activation_date else None,
            #             "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            #             "is_active": self.is_active,
            #             "customer_id": self.customer_id,
            #             "warning_date": self.warning_date.isoformat() if self.warning_date else None,
            #             "contracts": [c.to_dict() for c in self.contracts] if self.contracts else [],
            #             "subscriptions": [s.to_dict() for s in self.subscriptions] if self.subscriptions else [],
            #             "usage_logs": [u.to_dict() for u in self.usage_logs] if self.usage_logs else [],
            #             "subscriber_type": self.subscriber_type,
            #             "account_id": self.account_id,
            # =======
            "main_balance": (
                float(self.main_balance) if self.main_balance is not None else 0.0
            ),
            "activation_date": (
                self.activation_date.isoformat() if self.activation_date else None
            ),
            "expiration_date": (
                self.expiration_date.isoformat() if self.expiration_date else None
            ),
            "is_active": self.is_active,
            "customer_id": self.customer_id.to_dict() if self.customer_id else None,
            "account_id": self.account_id.to_dict() if self.account_id else None,
            "subscriber": self.subscriber.to_dict() if self.subscriber else None,
            "warning_date": (
                self.warning_date.isoformat() if self.warning_date else None
            ),
            "contracts": (
                [c.to_dict() for c in self.contracts] if self.contracts else []
            ),
            "subscriptions": (
                [s.to_dict() for s in self.subscriptions] if self.subscriptions else []
            ),
            "usage_logs": (
                [u.to_dict() for u in self.usage_logs] if self.usage_logs else []
            ),
        }
