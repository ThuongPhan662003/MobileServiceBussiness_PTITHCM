from app.repositories.function_repository import FunctionRepository


from functools import wraps
from flask import session, redirect, url_for, render_template


def required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Tên hàm view đang được gọi:", f.__name__)

        role_id = session.get("role_id")
        if not role_id:
            return redirect(url_for("auth.login"))  # hoặc một trang đăng nhập

        # Lấy danh sách function user có quyền
        funcs = FunctionRepository.get_funcs_role_group_id(role_id)
        func_list = [func.syntax_name for func in funcs]
        print("hamf", func_list, type(f.__name__))

        if f.__name__ not in func_list:
            return render_template("exceptions/unauthorized.html"), 403

        return f(*args, **kwargs)

    return decorated_function
