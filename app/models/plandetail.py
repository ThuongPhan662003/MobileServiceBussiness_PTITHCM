from typing import Optional


class PlanDetail:
    __plan_id: Optional[int]
    __object_type: Optional[str]
    __duration: Optional[int]

    def __init__(self, plan_id=None, object_type=None, duration=None):
        self.plan_id = plan_id
        self.object_type = object_type
        self.duration = duration

    @property
    def plan_id(self):
        return self.__plan_id

    @plan_id.setter
    def plan_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("plan_id must be an integer")
        self.__plan_id = value

    @property
    def object_type(self):
        return self.__object_type

    @object_type.setter
    def object_type(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("object_type must be a string")
        self.__object_type = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("duration must be an integer")
        self.__duration = value

    def to_dict(self):
        return {
            "plan_id": self.plan_id,
            "object_type": self.object_type,
            "duration": self.duration,
        }
