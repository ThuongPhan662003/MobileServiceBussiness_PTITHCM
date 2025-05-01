from typing import Optional, List


class Service:
    __id: Optional[int]
    __service_name: Optional[str]
    __parent_id: Optional[int]
    __coverage_area: Optional[bool]

    def __init__(self, id=None, service_name=None, parent_id=None, coverage_area=False):
        self.id = id
        self.service_name = service_name
        self.parent_id = parent_id
        self.coverage_area = coverage_area

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def service_name(self):
        return self.__service_name

    @service_name.setter
    def service_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("service_name must be a string")
        self.__service_name = value

    @property
    def parent_id(self):
        return self.__parent_id

    @parent_id.setter
    def parent_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("parent_id must be an integer")
        self.__parent_id = value

    @property
    def coverage_area(self):
        return self.__coverage_area

    @coverage_area.setter
    def coverage_area(self, value):
        if value is not None and not isinstance(value, bool):
            raise ValueError("coverage_area must be a boolean")
        self.__coverage_area = value

    def to_dict(self):
        return {
            "id": self.id,
            "service_name": self.service_name,
            "parent_id": self.parent_id,
            "coverage_area": self.coverage_area,
        }
