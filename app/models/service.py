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

    # # -----------------------------
    # # CRUD operations in memory
    # # -----------------------------

    # @staticmethod
    # def get_service_by_id(
    #     service_id: int, services: List["Service"]
    # ) -> Optional["Service"]:
    #     return next((s for s in services if s.id == service_id), None)

    # @staticmethod
    # def create_service(
    #     service_list: List["Service"],
    #     new_id: int,
    #     service_name: str,
    #     parent_id: Optional[int],
    #     coverage_area: bool,
    # ) -> "Service":
    #     new_service = Service(
    #         id=new_id,
    #         service_name=service_name,
    #         parent_id=parent_id,
    #         coverage_area=coverage_area,
    #     )
    #     service_list.append(new_service)
    #     return new_service

    # @staticmethod
    # def update_service(
    #     service_id: int,
    #     services: List["Service"],
    #     service_name=None,
    #     parent_id=None,
    #     coverage_area=None,
    # ) -> Optional["Service"]:
    #     service = Service.get_service_by_id(service_id, services)
    #     if not service:
    #         return None
    #     if service_name is not None:
    #         service.service_name = service_name
    #     if parent_id is not None:
    #         service.parent_id = parent_id
    #     if coverage_area is not None:
    #         service.coverage_area = coverage_area
    #     return service

    # @staticmethod
    # def delete_service(service_id: int, services: List["Service"]) -> bool:
    #     service = Service.get_service_by_id(service_id, services)
    #     if service:
    #         services.remove(service)
    #         return True
    #     return False
