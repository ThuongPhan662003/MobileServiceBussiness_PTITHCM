from flask import Blueprint, request, jsonify, render_template
from app.services.staff_service import StaffService


staff_bp = Blueprint("staff", __name__, url_prefix="/staffs")

@staff_bp.route("/", methods=["GET"])
def get_all_staffs():
    # Kiểm tra xem có tham số tìm kiếm không
    if any(key in request.args for key in ["full_name", "account_id", "gender", "is_active", "role"]):
        filters = request.args.to_dict()  # Lấy tất cả các tham số tìm kiếm từ query string
        staffs = StaffService.search_staffs(filters)  # Gọi hàm tìm kiếm từ service
    else:
        staffs = StaffService.get_all_staffs()  # Nếu không có tham số tìm kiếm, lấy tất cả nhân viên
    
    return render_template("Staff/staff.html", staffs=staffs)


@staff_bp.route("/<int:staff_id>", methods=["GET"])
def get_staff_by_id(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)
    if staff:
        return jsonify(staff.to_dict()), 200
    return jsonify({"error": "Staff not found"}), 404

@staff_bp.route("/create", methods=["POST"])
def create_staff():
    data = request.form.to_dict() 
    result = StaffService.create_staff(data)
    print(result)
    if result.get("success"):
        return jsonify({"message": "Staff created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@staff_bp.route("/update/<int:staff_id>", methods=["POST"])
def update_staff(staff_id):
    data = request.form.to_dict()
    result = StaffService.update_staff(staff_id, data)
    print(result)
    if result.get("success"):
        return jsonify({"message": "Staff updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@staff_bp.route("/lock/<int:staff_id>", methods=["POST"])
def lock_staff(staff_id):
    result = StaffService.delete_staff(staff_id)
    if result.get("success"):
        return jsonify({"message": "Staff deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400

