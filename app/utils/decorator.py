from functools import wraps

from flask import abort, session
from flask_login import current_user


def required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Tên hàm view đang được gọi:", f.__name__)

        # Ví dụ: Nếu tên hàm là 'hello', thì chặn lại
        # if f.__name__ == "hello":
        #     return "Bạn không được phép gọi hàm này", 403

        return f(*args, **kwargs)

    return decorated_function


def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session["role_type"] and session["role_type"] not in allowed_roles:
                abort(403, description="Bạn không có quyền truy cập.")
            return f(*args, **kwargs)

        return wrapper

    return decorator
