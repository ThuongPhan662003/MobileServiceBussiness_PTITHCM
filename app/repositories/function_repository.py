from app.database import db_instance
from app.models.function import Function


class FunctionRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_functions", fetchall=True)
            functions = []

            for row in result:
                func = Function()
                func.id = row.get("id")
                func.function_name = row.get("function_name")
                func.syntax_name = row.get("syntax_name")
                functions.append(func.to_dict())

            return functions
        except Exception as e:
            print(f"Lỗi khi lấy danh sách function: {e}")
            return []

    @staticmethod
    def get_by_id(function_id):
        try:
            result = db_instance.execute(
                "CALL GetFunctionById(%s)", (function_id,), fetchone=True
            )
            if result:
                func = Function()
                func.id = result.get("id")
                func.function_name = result.get("function_name")
                func.syntax_name = result.get("syntax_name")
                return func
            return None
        except Exception as e:
            print(f"Lỗi khi lấy function theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Function):
        try:
            result = db_instance.execute(
                "CALL AddFunction(%s, %s)",
                (data.function_name, data.syntax_name),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi thêm function: {result['error']}")
                return False
            return result.get("success", False)
        except Exception as e:
            print(f"Lỗi khi thêm function: {e}")
            return False

    @staticmethod
    def update(function_id, data: Function):
        try:
            result = db_instance.execute(
                "CALL UpdateFunction(%s, %s, %s)",
                (function_id, data.function_name, data.syntax_name),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi khi cập nhật function: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật function: {e}")
            return False

    @staticmethod
    def delete(function_id):
        try:
            result = db_instance.execute(
                "CALL DeleteFunction(%s)", (function_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi khi xóa function: {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa function: {e}")
            return False

    @staticmethod
    def get_funcs_role_group_id(role_group_id):
        try:
            result = db_instance.execute(
                "CALL sp_get_functions_by_rolegroup_id(%s) ",
                (role_group_id),
                fetchall=True,
            )
            functions = []
            print("kết quả,", result[0])
            for row in result[0]:
                print("roww", row)
                func = Function()
                func.id = row.get("id")
                func.function_name = row.get("function_name")
                func.syntax_name = row.get("syntax_name")
                print("hàm", row.get("function_name"))
                functions.append(func)

            return functions
        except Exception as e:
            print(f"Lỗi khi lấy danh sách function: {e}")
            return []
