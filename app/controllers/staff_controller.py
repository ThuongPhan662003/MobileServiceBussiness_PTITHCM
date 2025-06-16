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
from app.services.account_service import AccountService
from app.services.staff_service import StaffService
from flask_login import login_required
from app.utils.decorator import required
from app.utils.email_sender import send_reset_email
from app.utils.utils import generate_random_password

staff_bp = Blueprint("staff", __name__, url_prefix="/staffs")


@login_required
@staff_bp.route("/", methods=["GET"])
# @required
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


@staff_bp.route("/<int:staff_id>", methods=["GET"])
def get_staff_by_id(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)
    if staff:
        return jsonify(staff), 200
    return jsonify({"error": "Staff not found"}), 404


@login_required
@staff_bp.route("/create", methods=["POST"])
# @required
def create_staff():
    data = request.form.to_dict()
    result = StaffService.create_staff(data)
    print(result)
    if result.get("success"):
        return jsonify({"message": "Staff created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@login_required
@staff_bp.route("/update/<int:staff_id>", methods=["POST"])
# @required
def update_staff(staff_id):
    data = request.form.to_dict()
    result = StaffService.update_staff(staff_id, data)
    print(result)
    if result.get("success"):
        return jsonify({"message": "Staff updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@staff_bp.route("/lock/<int:staff_id>", methods=["POST"])
# @required
def lock_staff(staff_id):
    result = StaffService.delete_staff(staff_id)
    if result.get("success"):
        return jsonify({"message": "Staff deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@staff_bp.route("/detail/<int:staff_id>", methods=["GET"])
# @required
def staff_detail(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)
    print("dữ liệu", staff)
    # if not staff:
    #     abort(404, description="Không tìm thấy nhân viên")
    return render_template("Staff/infor.html", staff=staff)


@login_required
@staff_bp.route("/edit/<int:staff_id>", methods=["GET", "POST"])
def edit_staff(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)
    print("meo")
    if request.method == "POST":
        print("dau")
        # Cập nhật thông tin nhân viên
        phone = request.form.get("phone")
        email = request.form.get("email")
        data = {"phone": phone, "email": email}

        result = StaffService.update_info_staff(staff_id, data)
        if result and result.get("success") == 1:
            flash(result.get("message", "Cập nhật thành công!"), "success")
        else:
            flash(
                result.get(
                    "message", "Có lỗi xảy ra khi cập nhật thông tin nhân viên."
                ),
                "error",
            )
        return redirect(url_for("staff.staff_detail", staff_id=staff_id))

    return render_template("Staff/edit_staff.html", staff=staff)


# @login_required
# @staff_bp.route("/accounts/edit/<int:staff_id>", methods=["GET", "POST"])
# @required
# def edit_account(staff_id):
#     staff = StaffService.get_staff_by_id(staff_id)
#     account = AccountService.get_account_by_id(staff["account_id"]["id"])
#     if request.method == "POST":
#         new_password = request.form.get("new_password")
#         data = {"password": new_password}
#         result = StaffService.update_account(staff_id, data)
#         if result and result.get("success") == 1:
#             flash(result.get("message", "Cập nhật thành công!"), "success")
#         else:
#             flash(
#                 result.get("message", "Có lỗi xảy ra khi cập nhật tài khoản."),
#                 "error",
#             )

#         return redirect(url_for("staff.staff_detail", staff_id=staff_id))

#     return render_template("Staff/edit_account.html", account=account)


@login_required
@staff_bp.route(
    "/accounts/edit/<int:staff_id>",methods=["POST"]
)
# @required
def edit_account_of_staff(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)
    account = AccountService.get_account_by_id(staff["account_id"]["id"])

    try:
        new_password = generate_random_password()
        data = {"password": new_password}
        result = StaffService.update_account(staff_id, data)

        if result and result.get("success") == 1:
            send_reset_email(staff.get("email"), staff.get("full_name"), new_password)
            return jsonify({"message": "Đã gửi mật khẩu mới qua email!"}), 200
        else:
            return jsonify({"error": result.get("message", "Cập nhật thất bại.")}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
