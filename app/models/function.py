from typing import Optional, List


class Function:
    __id: Optional[int]
    __function_name: Optional[str]
    __syntax_name: Optional[str]

    def __init__(self, id=None, function_name=None, syntax_name=None):
        self.id = id
        self.function_name = function_name
        self.syntax_name = syntax_name

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("id must be an integer")
        self.__id = value

    @property
    def function_name(self):
        return self.__function_name

    @function_name.setter
    def function_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("function_name must be a string")
        self.__function_name = value

    @property
    def syntax_name(self):
        return self.__syntax_name

    @syntax_name.setter
    def syntax_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("syntax_name must be a string")
        self.__syntax_name = value

    def to_dict(self):
        return {
            "id": self.id,
            "function_name": self.function_name,
            "syntax_name": self.syntax_name,
        }

    # @staticmethod
    # def get_functions_by_role_group_not_exist(
    #     role_group_id: int, all_functions: List, role_group_details: List
    # ):
    #     """
    #     Trả về:
    #         - Các function KHÔNG thuộc role_group_id
    #         - Các function ĐÃ thuộc role_group_id

    #     all_functions: List[Function]
    #     role_group_details: List[RoleGroupDetail]
    #     """
    #     if not all(isinstance(f, Function) for f in all_functions):
    #         raise ValueError("all_functions must be a list of Function objects")
    #     if not all(isinstance(r, RoleGroupDetail) for r in role_group_details):
    #         raise ValueError(
    #             "role_group_details must be a list of RoleGroupDetail objects"
    #         )

    #     exist_function_ids = [
    #         detail.function_id
    #         for detail in role_group_details
    #         if detail.role_group_id == role_group_id
    #     ]

    #     avai_results = []
    #     exist_results = []

    #     for f in all_functions:
    #         if f.id in exist_function_ids:
    #             exist_results.append(f)
    #         else:
    #             avai_results.append(f)

    #     return {"avai_results": avai_results, "exist_result": exist_results}
