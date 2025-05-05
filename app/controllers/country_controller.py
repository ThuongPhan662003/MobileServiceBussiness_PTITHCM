from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.services.country_service import CountryService

country_bp = Blueprint("country", __name__, url_prefix="/countries")


@country_bp.route("/", methods=["GET"])
@login_required
def index():
    print("hi")
    return render_template("countries/countries.html")


@country_bp.route("/get-all", methods=["GET"])
@login_required
def get_all_countries():
    countries = CountryService.get_all_countries()
    return jsonify(countries), 200


@country_bp.route("/<int:country_id>", methods=["GET"])
@login_required
def get_country_by_id(country_id):
    country = CountryService.get_country_by_id(country_id)
    if country:
        return jsonify(country.to_dict()), 200
    return jsonify({"error": "Country not found"}), 404


@country_bp.route("/", methods=["POST"])
@login_required
def create_country():
    data = request.get_json()
    result = CountryService.create_country(data)

    if result.get("success"):
        return (
            jsonify(
                {
                    "success": True,
                    "message": result.get(
                        "message", "Quốc gia đã được tạo thành công."
                    ),
                }
            ),
            201,
        )

    # Trả về lỗi kèm thông điệp rõ ràng
    return (
        jsonify(
            {
                "success": False,
                "error": result.get("error", True),
                "message": result.get("message", "Đã xảy ra lỗi khi tạo quốc gia."),
            }
        ),
        400,
    )


@country_bp.route("/<int:country_id>", methods=["PUT"])
@login_required
def update_country(country_id):
    data = request.get_json()
    result = CountryService.update_country(country_id, data)
    if result.get("success"):
        return jsonify({"message": "Country updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@country_bp.route("/<int:country_id>", methods=["DELETE"])
@login_required
def delete_country(country_id):
    result = CountryService.delete_country(country_id)
    if result.get("success"):
        return jsonify({"message": "Country deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
