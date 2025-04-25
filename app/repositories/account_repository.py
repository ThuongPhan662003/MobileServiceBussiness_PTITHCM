from app.database import db_instance
from app.models.account import Account


class AccountRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_accounts", fetchall=True)
            print(result)
            accounts = []

            for row in result:
                account = Account()
                account.id = row.get("id")
                account.username = row.get("username")
                account.password = row.get("password")
                account.is_active = True if row.get("is_active") else False
                accounts.append(account.to_dict())

            return accounts
        except Exception as e:
            print(f"Lỗi khi lấy danh sách account: {e}")
            return []

    @staticmethod
    # def check_login_by_username_and_password(username, password):
    #     try:
    #         print("username", username)
    #         print("password", password)

    #         # Gọi stored procedure với IN và OUT parameters
    #         acc = db_instance.execute(
    #             "CALL sp_account_check_login(%s, %s, @p_status, @p_message)",
    #             (username, password),
    #             fetchone=True,
    #         )
    #         print("acc", acc)

    #         # Truy vấn lấy kết quả OUT
    #         result = db_instance.execute(
    #             "SELECT @p_status AS status, @p_message AS message;", fetchone=True
    #         )
    #         print("Kết quả OUT:", result)

    #         # Kiểm tra kết quả OUT
    #         if result:
    #             status = result.get("status")
    #             message = result.get("message")

    #             # Nếu status == 1 là thành công → lấy account
    #             if status == 1:
    #                 user = AccountRepository.get_by_id(acc["account_id"])
    #                 print("AccountRepository.get_by_id(username)", user.to_dict())

    #                 return {"success": True, "message": message, "data": user}
    #             else:
    #                 # Trường hợp tài khoản sai hoặc bị vô hiệu hóa
    #                 return {"success": False, "message": message}

    #         return {"success": False, "message": "Không thể xác thực tài khoản"}

    #     except Exception as e:
    #         print(f"Lỗi khi đăng nhập: {e}")
    #         return {"success": False, "message": str(e)}
    def check_login_by_username_and_password(username, password):
        try:
            print("username", username)
            print("password", password)

            # Gọi stored procedure (có trả ra dữ liệu nếu đăng nhập thành công)
            acc = db_instance.execute(
                "CALL sp_account_check_login(%s, %s, @p_status, @p_message)",
                (username, password),
                fetchone=True,  # acc có thể là subscriber hoặc staff tùy loại
            )
            print("acc", acc)

            # Lấy kết quả OUT từ stored procedure
            result = db_instance.execute(
                "SELECT @p_status AS status, @p_message AS message;", fetchone=True
            )
            print("Kết quả OUT:", result)

            if result:
                status = result.get("status")
                message = result.get("message")

                if status == 1:
                    # Nếu đăng nhập thành công và có trả dữ liệu acc
                    if acc:
                        print("kết quả", acc)
                        user_info = dict(acc)
                        user_info["role_type"] = acc.get(
                            "role_type"
                        )  # 'subscriber' hoặc 'staff'
                        user = AccountRepository.get_by_id(user_info["account_id"])
                        print("người dùng", user_info)
                        user_info["account_id"] = user
                        return {"success": True, "message": message, "data": user_info}
                    else:
                        return {
                            "success": True,
                            "message": message,
                            "data": None,  # Không có dữ liệu user cụ thể
                        }
                else:
                    return {"success": False, "message": message}

            return {"success": False, "message": "Không thể xác thực tài khoản"}

        except Exception as e:
            print(f"Lỗi khi đăng nhập: {e}")
            return {"success": False, "message": str(e)}

    @staticmethod
    def get_by_id(account_id):
        try:
            result = db_instance.execute(
                "CALL GetAccountById(%s)", (account_id,), fetchone=True
            )
            print("resulr login", result)
            if result:
                account = Account()
                account.id = result.get("id")
                account.username = result.get("username")
                account.password = result.get("password")
                account.is_active = True if result.get("is_active") else False
                print("account", account.to_dict())
                return account
            return None
        except Exception as e:
            print(f"Lỗi khi lấy account theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Account):
        try:
            print("khonae", data.username)
            result = db_instance.execute(
                "CALL CreateAccount(%s, %s)",
                (data.username, data.password),
                fetchone=True,
                commit=True,
            )
            print("insert", result)
            if not result.get("success"):
                print(f"Lỗi từ stored procedure (insert): {result['message']}")
                return result
            return result
        except Exception as e:
            print(f"Lỗi khi thêm account: {e}")
            return result

    @staticmethod
    def update(account_id, data: Account):
        try:
            result = db_instance.execute(
                "CALL UpdateAccount(%s, %s, %s, %s)",
                (account_id, data.username, data.password, data.is_active),
                fetchone=True,
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (update): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi cập nhật account: {e}")
            return False

    @staticmethod
    def delete(account_id):
        try:
            result = db_instance.execute(
                "CALL DeleteAccount(%s)", (account_id,), fetchone=True
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (delete): {result['error']}")
                return result["error"]
            return result.get("success", False)
        except Exception as e:
            print(f"Lỗi khi xóa account: {e}")
            return False

    @staticmethod
    def create_account_from_phone(phone_number: str):
        try:
            # Gọi stored procedure
            result = db_instance.execute(
                "CALL create_account_from_phone(%s)",  # Gọi stored procedure
                (phone_number,),  # Tham số truyền vào là số điện thoại
                fetchone=True,  # Lấy một dòng duy nhất
                commit=True,  # Commit sau khi thực thi
            )

            # In ra kết quả trả về để kiểm tra
            print("Kết quả trả về từ stored procedure:", result)

            # Kiểm tra kết quả trả về và lấy account_id
            if result and "id" in result:
                return result["id"]  # Trả về account_id
            else:
                return {"error": "Không thể lấy account_id từ stored procedure"}

        except Exception as e:
            print(f"Lỗi khi tạo account từ số điện thoại: {e}")
            return {"error": str(e)}
