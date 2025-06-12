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

    # @staticmethod
    # def check_login_by_username_and_password(username, password):
    #     try:

    #         def run(cursor, conn):
    #             print("username", username)
    #             print("password", password)

    #             # Gọi stored procedure có OUT
    #             cursor.execute(
    #                 "CALL sp_account_check_login(%s, %s, @p_status, @p_message)",
    #                 (username, password),
    #             )

    #             # Lấy dữ liệu người dùng (acc)
    #             acc = cursor.fetchone()
    #             print("acc", acc)

    #             # Lấy OUT parameter
    #             cursor.execute("SELECT @p_status AS status, @p_message AS message")
    #             result = cursor.fetchone()
    #             print("Kết quả OUT:", result)

    #             return acc, result

    #         acc, result = db_instance.execute_with_connection(run)

    #         if result:
    #             status = result.get("status")
    #             message = result.get("message")

    #             if status == 1:
    #                 if acc:
    #                     print("kết quả", acc)
    #                     user_info = dict(acc)
    #                     user_info["role_type"] = acc.get("role_type")
    #                     user = AccountRepository.get_by_id(
    #                         user_info["account_id"]
    #                     )  # vẫn dùng execute()
    #                     user_info["account_id"] = user
    #                     return {"success": True, "message": message, "data": user_info}
    #                 else:
    #                     return {"success": True, "message": message, "data": None}
    #             else:
    #                 return {"success": False, "message": message}

    #         return {"success": False, "message": "Không thể xác thực tài khoản"}

    #     except Exception as e:
    #         print(f"Lỗi khi đăng nhập: {e}")
    #         return {"success": False, "message": str(e)}
    @staticmethod
    def check_login_by_username_and_password(username, password):
        try:

            result = db_instance.execute(
                "CALL sp_get_user_info_with_roles(%s,%s)",
                (username, password),
                fetchone=True,
            )
            print("kết quả", result)
            if result:
                re = result
                message = result.get("message")
                account_id = result.get("account_id")
                if account_id:
                    acc = AccountRepository.get_by_id(
                        result.get("account_id")
                    )  # vẫn dùng execute()
                    print("tài khoản", type(acc), acc.to_dict())
                    re["account_id"] = acc
                    if result.get("role_name") == "Thuê bao":
                        return {"success": True, "message": message, "data": re}
                    else:
                        acc = AccountRepository.get_by_id(
                            result.get("account_id")
                        )  # vẫn dùng execute()
                        return {"success": True, "message": message, "data": re}
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
            if result:
                account = Account()
                account.id = result.get("id")
                account.username = result.get("username")
                account.password = result.get("password")
                account.is_active = True if result.get("is_active") else False
                print("tien", account.to_dict())
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
            result = db_instance.execute(
                "CALL create_account_from_phone(%s)",
                (phone_number,),  # ✅ phải là tuple
                fetchone=True,
                commit=True,
            )

            # In ra kết quả trả về để kiểm tra
            print("Kết quả trả về từ stored procedure:", result)

            # Kiểm tra kết quả trả về và lấy account_id
            if result:
                # In chi tiết kết quả để kiểm tra cấu trúc dữ liệu trả về
                print("Chi tiết kết quả:", result)
                account_id = result.get("id")

                if account_id is not None:
                    return account_id
                else:
                    return {"error": "Không thể lấy account_id từ stored procedure"}
            else:
                return {"error": "Không có kết quả từ stored procedure"}

        except Exception as e:
            print(f"❌ Lỗi khi tạo account từ số điện thoại: {e}")
            return {"error": str(e)}

    @staticmethod
    def update_password_by_email_or_phone(identifier, hashed_password):
        try:
            sql = "CALL sp_accounts_update_password_by_username(%s, %s)"
            db_instance.execute(sql, (identifier, hashed_password), commit=True)

            return {
                "success": True,
                "message": "✅ Cập nhật mật khẩu thành công",
                "data": {"username": identifier},
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Cập nhật mật khẩu thất bại: {str(e)}",
                "data": None,
            }
