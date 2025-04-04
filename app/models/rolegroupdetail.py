from typing import Optional


class RoleGroupDetail:
    __role_group_id: Optional[int]
    __function_id: Optional[int]

    def __init__(self, role_group_id=None, function_id=None):
        self.role_group_id = role_group_id
        self.function_id = function_id

    @property
    def role_group_id(self):
        return self.__role_group_id

    @role_group_id.setter
    def role_group_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("role_group_id must be an integer")
        self.__role_group_id = value

    @property
    def function_id(self):
        return self.__function_id

    @function_id.setter
    def function_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("function_id must be an integer")
        self.__function_id = value

    def to_dict(self):
        return {"role_group_id": self.role_group_id, "function_id": self.function_id}
