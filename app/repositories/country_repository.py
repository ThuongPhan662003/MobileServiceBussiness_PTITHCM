# country repositorie
from app.database import db_instance
from app.models.country import Country


class CountryRepository:
    @staticmethod
    def get_all():
        try:
            result = db_instance.execute("SELECT * FROM v_countries", fetchall=True)
            countries = []
            print("kết quả", result)
            for row in result[0]:
                country = Country()
                country.id = row.get("id")
                country.country_name = row.get("country_name")
                # country.networks sẽ được xử lý ở nơi khác nếu cần
                countries.append(country.to_dict())

            return countries
        except Exception as e:
            print(f"Lỗi khi lấy danh sách quốc gia: {e}")
            return []

    @staticmethod
    def get_by_id(country_id):
        try:
            result = db_instance.execute(
                "CALL GetCountryById(%s)", (country_id,), fetchone=True
            )
            if result:
                country = Country()
                country.id = result.get("id")
                country.country_name = result.get("country_name")
                print("country", country.to_dict())
                return country
            return None
        except Exception as e:
            print(f"Lỗi khi lấy quốc gia theo ID: {e}")
            return None

    @staticmethod
    def insert(data: Country):
        try:
            result = db_instance.execute(
                "CALL AddCountry(%s)", (data.country_name,), fetchone=True, commit=True
            )

            if result.get("error"):
                return {
                    "success": False,
                    "error": True,
                    "message": result.get(
                        "message", "Đã xảy ra lỗi khi thêm quốc gia."
                    ),
                }

            return {
                "success": True,
                "error": False,
                "message": result.get("message", "Thêm quốc gia thành công."),
            }

        except Exception as e:
            return {
                "success": False,
                "error": True,
                "message": f"Lỗi hệ thống khi thêm quốc gia: {str(e)}",
            }

    # @staticmethod
    # def update(country_id, data: Country):
    #     try:
    #         result = db_instance.execute(
    #             "CALL UpdateCountry(%s, %s)",
    #             (country_id, data.country_name),
    #             fetchone=True,
    #         )
    #         if result.get("error"):
    #             print(f"Lỗi từ stored procedure (update): {result['error']}")
    #             return result["error"]
    #         return True
    #     except Exception as e:
    #         print(f"Lỗi khi cập nhật quốc gia: {e}")
    #         return False

    @staticmethod
    def delete(country_id):
        try:
            result = db_instance.execute(
                "CALL DeleteCountry(%s)", (country_id,), fetchone=True, commit=True
            )
            if result.get("error"):
                print(f"Lỗi từ stored procedure (delete): {result['error']}")
                return result["error"]
            return True
        except Exception as e:
            print(f"Lỗi khi xóa quốc gia: {e}")
            return False
