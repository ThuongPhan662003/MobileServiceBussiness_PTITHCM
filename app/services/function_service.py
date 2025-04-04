from app.repositories.function_repository import FunctionRepository
from app.models.function import Function


class FunctionService:
    @staticmethod
    def get_all_functions():
        return FunctionRepository.get_all()

    @staticmethod
    def get_function_by_id(function_id):
        return FunctionRepository.get_by_id(function_id)

    @staticmethod
    def create_function(data: dict):
        try:
            func = Function(
                function_name=data.get("function_name"),
                syntax_name=data.get("syntax_name"),
            )
            result = FunctionRepository.insert(func)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_function(function_id, data: dict):
        try:
            func = Function(
                function_name=data.get("function_name"),
                syntax_name=data.get("syntax_name"),
            )
            result = FunctionRepository.update(function_id, func)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_function(function_id):
        try:
            result = FunctionRepository.delete(function_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
