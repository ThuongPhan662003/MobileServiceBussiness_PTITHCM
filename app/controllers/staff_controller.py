from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    request,
    jsonify,
    render_template,
    url_for,
)
from app.services.staff_service import StaffService


staff_bp = Blueprint("staff", __name__, url_prefix="/staffs")


@staff_bp.route("/", methods=["GET"])
def get_all_staffs():
    # Kiểm tra xem có tham số tìm kiếm không
    if any(
        key in request.args
        for key in ["full_name", "account_id", "gender", "is_active", "role"]
    ):
        filters = (
            request.args.to_dict()
        )  # Lấy tất cả các tham số tìm kiếm từ query string
        staffs = StaffService.search_staffs(filters)  # Gọi hàm tìm kiếm từ service
    else:
        staffs = (
            StaffService.get_all_staffs()
        )  # Nếu không có tham số tìm kiếm, lấy tất cả nhân viên

    return render_template("Staff/staff.html", staffs=staffs)


# @staff_bp.route("/<int:staff_id>", methods=["GET"])
# def get_staff_by_id(staff_id):
#     staff = StaffService.get_staff_by_id(staff_id)
#     if staff:
#         return jsonify(staff.to_dict()), 200
#     return jsonify({"error": "Staff not found"}), 404


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


@staff_bp.route("/<int:staff_id>", methods=["GET"])
def staff_detail(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)
    print("dữ liệu", staff)
    # if not staff:
    #     abort(404, description="Không tìm thấy nhân viên")
    return render_template("Staff/infor.html", staff=staff)


@staff_bp.route("/edit/<int:staff_id>", methods=["GET", "POST"])
def edit_staff(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)
    if not staff:
        flash("Không tìm thấy nhân viên", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        data = {
            "full_name": request.form.get("full_name"),
            "card_id": request.form.get("card_id"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "gender": request.form.get("gender"),
            "birthday": request.form.get("birthday"),  # YYYY-MM-DD
            "is_active": True if request.form.get("is_active") == "on" else False,
        }
        success = StaffService.update_staff(staff_id, data)
        if success:
            flash("Cập nhật thành công", "success")
            return redirect(url_for("staff.edit_staff", staff_id=staff_id))
        else:
            flash("Cập nhật thất bại", "danger")

    return render_template("staff/edit.html", staff=staff)
