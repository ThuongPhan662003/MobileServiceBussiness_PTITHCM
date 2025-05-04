from functools import wraps


def required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Tên hàm view đang được gọi:", f.__name__)

        # Ví dụ: Nếu tên hàm là 'hello', thì chặn lại
        # if f.__name__ == "hello":
        #     return "Bạn không được phép gọi hàm này", 403

        return f(*args, **kwargs)

    return decorated_function
