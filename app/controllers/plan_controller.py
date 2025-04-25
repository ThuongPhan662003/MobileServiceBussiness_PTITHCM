from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from app.services.plan_service import PlanService

plan_bp = Blueprint("plan", __name__, url_prefix="/plans")


@plan_bp.route("/", methods=["GET"])
def get_all_plans():
    try:
        plans = PlanService.get_all_plans()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            print("Đặt lại")
            plan_list = []
            for plan in plans:
                plan_list.append(plan.to_dict())
            print(plan_list)
            return jsonify(plan_list), 200

        return render_template("Plan/plan.html", plans=plans)
    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": f"Lỗi khi lấy danh sách gói cước: {str(e)}"}), 500
        flash(f"Lỗi: {str(e)}", "error")
        return render_template("Plan/plan.html", plans=[]), 500


@plan_bp.route("/create", methods=["GET", "POST"])
def create_plan():
    if request.method == "GET":

        return render_template("Plan/create_plan.html", data={})

    if request.method == "POST":
        data = request.form.to_dict()
        # Kiểm tra dữ liệu đầu vào
        errors = []
        if not data.get("code") or len(data.get("code", "").strip()) == 0:
            errors.append("Mã gói cước là bắt buộc")

        if not data.get("code") or len(data.get("code", "")) > 50:

            errors.append("Mã gói cước không được vượt quá 50 ký tự")
        if not data.get("price"):
            errors.append("Giá gói cước là bắt buộc")
        else:
            try:
                price = float(data.get("price"))
                if price <= 0:
                    errors.append("Giá gói cước phải là số dương")
            except ValueError:
                errors.append("Giá gói cước phải là số")

        if not data.get("object_type") or data.get("object_type") not in [
            "TRATRUOC",
            "TRASAU",
        ]:
            errors.append("Hình thức thanh toán phải là TRATRUOC hoặc TRASAU")
        if not data.get("duration"):
            errors.append("Thời hạn là bắt buộc")
        else:
            try:
                duration = int(data.get("duration"))
                if duration <= 0:
                    errors.append("Thời hạn phải là số dương")
            except ValueError:
                errors.append("Thời hạn phải là số nguyên")

        for field in [
            "free_data",
            "free_on_network_a_call",
            "free_on_network_call",
            "free_on_network_SMS",
            "free_off_network_a_call",
            "free_off_network_call",
            "free_off_network_SMS",
            "maximum_on_network_call",
        ]:
            if data.get(field):
                try:
                    value = int(data.get(field))
                    if value < 0:
                        errors.append(
                            f"{field.replace('_', ' ').title()} phải không âm"
                        )
                except ValueError:
                    errors.append(
                        f"{field.replace('_', ' ').title()} phải là số nguyên"
                    )
        for field in ["ON_SMS_cost", "ON_a_call_cost"]:
            if data.get(field):
                try:
                    value = float(data.get(field))
                    if value < 0:
                        errors.append(
                            f"{field.replace('_', ' ').title()} phải không âm"
                        )
                except ValueError:
                    errors.append(f"{field.replace('_', ' ').title()} phải là số")
        for field in ["renewal_syntax", "registration_syntax", "cancel_syntax"]:
            if data.get(field) and len(data.get(field)) > 255:
                errors.append(
                    f"{field.replace('_', ' ').title()} không được vượt quá 255 ký tự"
                )
        if data.get("service_id"):
            try:
                int(data.get("service_id"))
            except ValueError:
                errors.append("ID Dịch vụ phải là số nguyên")
        if data.get("staff_id"):
            try:
                int(data.get("staff_id"))
            except ValueError:
                errors.append("ID Nhân viên phải là số nguyên")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("Plan/create_plan.html", data=data), 400

        # Chuyển đổi dữ liệu
        data["is_active"] = data.get("is_active") == "on"
        data["auto_renew"] = data.get("auto_renew") == "on"
        for field in [
            "free_data",
            "free_on_network_a_call",
            "free_on_network_call",
            "free_on_network_SMS",
            "free_off_network_a_call",
            "free_off_network_call",
            "free_off_network_SMS",
            "maximum_on_network_call",
        ]:
            data[field] = int(data.get(field, 0)) if data.get(field) else 0
        for field in ["ON_SMS_cost", "ON_a_call_cost"]:
            data[field] = float(data.get(field, 0)) if data.get(field) else None
        data["price"] = float(data.get("price")) if data.get("price") else None
        data["service_id"] = (
            int(data.get("service_id")) if data.get("service_id") else None
        )
        data["staff_id"] = int(data.get("staff_id")) if data.get("staff_id") else None

        data["duration"] = int(data.get("duration")) if data.get("duration") else None
        print(data)
        result = PlanService.create_plan(data)
        if result.get("success"):
            flash("Thêm gói cước thành công!", "success")
            return redirect(url_for("plan.get_all_plans"))
        flash(f"Lỗi: {result.get('error')}", "error")
        return render_template("Plan/create_plan.html", data=data), 400


@plan_bp.route("/update/<int:plan_id>", methods=["GET", "POST"])
def update_plan(plan_id):
    plan = PlanService.get_plan_by_id(plan_id)
    if not plan:
        flash("Gói cước không tồn tại!", "error")
        return redirect(url_for("plan.get_all_plans"))

    if request.method == "GET":
        return render_template(
            "Plan/update_plan.html", plan=plan.to_dict(), plan_id=plan_id
        )

    if request.method == "POST":
        data = request.form.to_dict()
        # Kiểm tra dữ liệu đầu vào
        errors = []
        if not data.get("code") or len(data.get("code", "").strip()) == 0:
            errors.append("Mã gói cước là bắt buộc")

        if not data.get("code") or len(data.get("code", "")) > 50:

            errors.append("Mã gói cước không được vượt quá 50 ký tự")
        if not data.get("price"):
            errors.append("Giá gói cước là bắt buộc")
        else:
            try:
                price = float(data.get("price"))
                if price <= 0:
                    errors.append("Giá gói cước phải là số dương")
            except ValueError:
                errors.append("Giá gói cước phải là số")

        if not data.get("object_type") or data.get("object_type") not in [
            "TRATRUOC",
            "TRASAU",
        ]:
            errors.append("Hình thức thanh toán phải là TRATRUOC hoặc TRASAU")
        if not data.get("duration"):
            errors.append("Thời hạn là bắt buộc")
        else:
            try:
                duration = int(data.get("duration"))
                if duration <= 0:
                    errors.append("Thời hạn phải là số dương")
            except ValueError:
                errors.append("Thời hạn phải là số nguyên")

        for field in [
            "free_data",
            "free_on_network_a_call",
            "free_on_network_call",
            "free_on_network_SMS",
            "free_off_network_a_call",
            "free_off_network_call",
            "free_off_network_SMS",
            "maximum_on_network_call",
        ]:
            if data.get(field):
                try:
                    value = int(data.get(field))
                    if value < 0:
                        errors.append(
                            f"{field.replace('_', ' ').title()} phải không âm"
                        )
                except ValueError:
                    errors.append(
                        f"{field.replace('_', ' ').title()} phải là số nguyên"
                    )
        for field in ["ON_SMS_cost", "ON_a_call_cost"]:
            if data.get(field):
                try:
                    value = float(data.get(field))
                    if value < 0:
                        errors.append(
                            f"{field.replace('_', ' ').title()} phải không âm"
                        )
                except ValueError:
                    errors.append(f"{field.replace('_', ' ').title()} phải là số")
        for field in ["renewal_syntax", "registration_syntax", "cancel_syntax"]:
            if data.get(field) and len(data.get(field)) > 255:
                errors.append(
                    f"{field.replace('_', ' ').title()} không được vượt quá 255 ký tự"
                )
        if data.get("service_id"):
            try:
                int(data.get("service_id"))
            except ValueError:
                errors.append("ID Dịch vụ phải là số nguyên")
        if data.get("staff_id"):
            try:
                int(data.get("staff_id"))
            except ValueError:
                errors.append("ID Nhân viên phải là số nguyên")

        if errors:
            for error in errors:
                flash(error, "error")
            return (
                render_template("Plan/update_plan.html", plan=data, plan_id=plan_id),
                400,
            )

        # Chuyển đổi dữ liệu
        data["is_active"] = data.get("is_active") == "on"
        data["auto_renew"] = data.get("auto_renew") == "on"
        for field in [
            "free_data",
            "free_on_network_a_call",
            "free_on_network_call",
            "free_on_network_SMS",
            "free_off_network_a_call",
            "free_off_network_call",
            "free_off_network_SMS",
            "maximum_on_network_call",
        ]:
            data[field] = int(data.get(field, 0)) if data.get(field) else 0
        for field in ["ON_SMS_cost", "ON_a_call_cost"]:
            data[field] = float(data.get(field, 0)) if data.get(field) else None
        data["price"] = float(data.get("price")) if data.get("price") else None
        data["service_id"] = (
            int(data.get("service_id")) if data.get("service_id") else None
        )
        data["staff_id"] = int(data.get("staff_id")) if data.get("staff_id") else None

        data["duration"] = int(data.get("duration")) if data.get("duration") else None

        result = PlanService.update_plan(plan_id, data)
        if result.get("success"):
            flash("Cập nhật gói cước thành công!", "success")
            return redirect(url_for("plan.get_all_plans"))
        flash(f"Lỗi: {result.get('error')}", "error")
        return render_template("Plan/update_plan.html", plan=data, plan_id=plan_id), 400


@plan_bp.route("/lock/<int:plan_id>", methods=["POST"])
def lock_plan(plan_id):
    result = PlanService.lock_plan(plan_id)
    if result.get("success"):
        flash("Khóa gói cước thành công!", "success")

        return jsonify({"success": True})
    flash(f"Lỗi: {result.get('error')}", "error")
    return jsonify({"error": result.get("error")}), 400


@plan_bp.route("/search", methods=["POST"])
def search_plans():
    try:
        data = request.get_json()

        print(f"Search data: {data}")  # Log dữ liệu đầu vào
        code = data.get("code") or None
        price = data.get("price") or None
        is_active = data.get("is_active")
        object_type = data.get("object_type")

        # Chuyển object_type thành None nếu là chuỗi rỗng hoặc không xác định
        if not object_type or object_type.strip() == "":
            object_type = None

        # Chuyển đổi is_active

        if is_active == "" or is_active is None:
            is_active = None
        else:
            is_active = int(is_active)  # Chuyển thành int (0 hoặc 1)

        # Chuyển đổi price
        if price:
            try:
                price = float(price)
            except ValueError:
                return jsonify({"error": "Giá phải là số"}), 400

        plans = PlanService.search_plans(code, price, is_active, object_type)
        print(f"Search results: {plans}")  # Log kết quả
        return jsonify(plans)
    except Exception as e:
        print(f"Search error: {str(e)}")  # Log lỗi

        return jsonify({"error": f"Lỗi khi tìm kiếm: {str(e)}"}), 500
