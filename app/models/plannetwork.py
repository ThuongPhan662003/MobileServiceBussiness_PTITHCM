from typing import Optional

from . import *

class PlanNetwork:
    __id: Optional[int]
    __network_id: Optional["Network"]
    __plan_id: Optional["Plan"]

    def __init__(self, id=None, network_id=None, plan_id=None):
        self.id = id
        self.network_id = network_id
        self.plan_id = plan_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def network_id(self):
        return self.__network_id

    @network_id.setter
    def network_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("network_id must be an integer")
        self.__network_id = value

    @property
    def plan_id(self):
        return self.__plan_id

    @plan_id.setter
    def plan_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("plan_id must be an integer")
        self.__plan_id = value

    def to_dict(self):
        return {
            "id": self.id,
            "network_id": self.network_id.to_dict(),
            "plan_id": self.plan_id.to_dict(),
        }
