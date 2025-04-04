from typing import Optional, List


class Country:
    __id: Optional[int]
    __country_name: Optional[str]
    __networks: Optional[List]

    def __init__(self, id=None, country_name=None, networks=None):
        self.id = id
        self.country_name = country_name
        self.networks = networks or []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def country_name(self):
        return self.__country_name

    @country_name.setter
    def country_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("country_name must be a string")
        self.__country_name = value

    @property
    def networks(self):
        return self.__networks

    @networks.setter
    def networks(self, value):
        if value is not None and not isinstance(value, list):
            raise ValueError("networks must be a list")
        self.__networks = value

    def to_dict(self):
        return {
            "id": self.id,
            "country_name": self.country_name,
            "networks": [n.to_dict() for n in self.networks] if self.networks else [],
        }
