from typing import Optional

from . import *


class Network:
    __id: Optional[int]
    __network_name: Optional[str]
    __display_name: Optional[str]
    __country_id: Optional["Country"]

    def __init__(self, id=None, network_name=None, display_name=None, country_id=None):
        self.id = id
        self.network_name = network_name
        self.display_name = display_name
        self.country_id = country_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def network_name(self):
        return self.__network_name

    @network_name.setter
    def network_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("network_name must be a string")
        self.__network_name = value

    @property
    def display_name(self):
        return self.__display_name

    @display_name.setter
    def display_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("display_name must be a string")
        self.__display_name = value

    @property
    def country_id(self):
        return self.__country_id

    @country_id.setter
    def country_id(self, value):
        # if value is not None and not isinstance(value, int):
        #     raise ValueError("country_id must be an integer")
        self.__country_id = value

    def to_dict(self):
        return {
            "id": self.id,
            "network_name": self.network_name,
            "display_name": self.display_name,
            "country_id": self.country_id.to_dict(),
        }
