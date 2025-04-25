from app.repositories.country_repository import CountryRepository
from app.models.country import Country


class CountryService:
    @staticmethod
    def get_all_countries():
        return CountryRepository.get_all()

    @staticmethod
    def get_country_by_id(country_id):
        return CountryRepository.get_by_id(country_id)

    @staticmethod
    def create_country(data: dict):
        try:
            country = Country(country_name=data.get("country_name"))
            result = CountryRepository.insert(country)

            # Đồng nhất định dạng trả về
            return {
                "success": result.get("success", False),
                "error": result.get("error", not result.get("success", False)),
                "message": result.get("message", "Không rõ thông báo"),
            }

        except Exception as e:
            print(f"[Service] Lỗi khi tạo quốc gia: {e}")
            return {
                "success": False,
                "error": True,
                "message": f"Lỗi hệ thống khi tạo quốc gia: {str(e)}",
            }

    @staticmethod
    def update_country(country_id, data: dict):
        try:
            country = Country(country_name=data.get("country_name"))
            result = CountryRepository.update(country_id, country)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_country(country_id):
        try:
            result = CountryRepository.delete(country_id)
            if result is True:
                return {"success": True}
            else:
                return {"error": result}
        except Exception as e:
            return {"error": str(e)}
