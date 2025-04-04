from typing import Optional


class RoleGroup:
    __id: Optional[int]
    __role_name: Optional[str]

    def __init__(self, id=None, role_name=None):
        self.id = id
        self.role_name = role_name

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def role_name(self):
        return self.__role_name

    @role_name.setter
    def role_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("role_name must be a string")
        self.__role_name = value

    def to_dict(self):
        return {"id": self.id, "role_name": self.role_name}
