from flask import Blueprint, json, render_template, request, jsonify
from app.services.rolegroup_service import RoleGroupService
from app.services.staff_service import StaffService
from flask_login import login_required
from app.utils.decorator import required

role_group_bp = Blueprint("role_group", __name__, url_prefix="/role_groups")


@login_required
@role_group_bp.route("/", methods=["GET"])
@required
def get_all_role_groups():
    role_groups = RoleGroupService.get_all_role_groups()
    # return jsonify(role_groups), 200
    return render_template("admin_home/role.html", role_groups=role_groups)


@login_required
@role_group_bp.route("/staffsByRoleGroup/<int:role_group_id>", methods=["GET"])
@required
def get_staffs_by_role_group(role_group_id):
    try:
        # Gọi RoleGroupService để lấy danh sách nhân viên
        staffs = RoleGroupService.get_staffs_by_role_group(role_group_id)
        # Trả về danh sách nhân viên dưới dạng JSON
        return jsonify(staffs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@login_required
@role_group_bp.route("/AddstaffsByRoleGroup", methods=["POST"])
@required
def add_staffs_by_role_group():
    try:
        data = request.get_json()
        role_group_id = data.get("role_group_id")
        account_ids_csv = data.get("account_ids")  # dạng "3,5,7,10"

        if not role_group_id or not account_ids_csv:
            return jsonify({"error": "Thiếu role_group_id hoặc account_ids"}), 400

        # Gọi stored procedure trong service layer
        result = RoleGroupService.add_accounts_to_role_group(
            role_group_id, account_ids_csv
        )

        return jsonify({"success": True, "message": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@login_required
@role_group_bp.route("/functions/<int:role_group_id>", methods=["GET"])
@required
def get_role_group_functions(role_group_id):
    try:
        result = RoleGroupService.get_role_group_functions(role_group_id)
        return (
            jsonify(
                {
                    "assigned_functions": result["assigned_functions"],
                    "unassigned_functions": result["unassigned_functions"],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@login_required
@role_group_bp.route(
    "/remove_function/<int:role_group_id>/<int:function_id>", methods=["DELETE"]
)
@required
def remove_function_from_role_group(role_group_id, function_id):
    try:

        print("role_group_id", role_group_id)
        print("function_id", function_id)
        # Gọi phương thức service để xóa chức năng
        result = RoleGroupService.remove_function_from_role_group(
            role_group_id, function_id
        )
        print("result", result)
        if result["status"] == "success":
            return jsonify({"message": result["message"]}), 200  # Thành công
        else:
            return jsonify({"error": result["message"]}), 400  # Thất bại
    except Exception as e:
        # Xử lý lỗi nếu có
        print(f"Lỗi khi xóa chức năng: {e}")
        return jsonify({"error": "Có lỗi xảy ra khi xóa chức năng"}), 500


@login_required
@role_group_bp.route("/add_funcs/<int:role_id>", methods=["POST"])
@required
def add_functions_to_role_group(role_id):
    print("role_id", role_id)
    try:
        # Lấy chuỗi permission_ids từ request
        permission_ids = request.json.get("permission_ids", "")
        print("permission_ids", permission_ids)

        # Kiểm tra nếu permission_ids không phải chuỗi JSON hợp lệ
        if not permission_ids:
            return jsonify({"error": "permission_ids không thể trống."}), 400

        # Đảm bảo permission_ids là chuỗi JSON hợp lệ
        if permission_ids.startswith("[") and permission_ids.endswith("]"):
            # Nếu permission_ids là chuỗi JSON hợp lệ
            try:
                # Chuyển chuỗi permission_ids thành danh sách
                permission_ids_list = json.loads(permission_ids)
                print("permission_ids_list", permission_ids_list)

                # Kiểm tra nếu permission_ids_list là danh sách hợp lệ
                if not isinstance(permission_ids_list, list):
                    return (
                        jsonify({"error": "permission_ids phải là một danh sách."}),
                        400,
                    )

            except json.JSONDecodeError:
                return (
                    jsonify({"error": "permission_ids không phải chuỗi JSON hợp lệ."}),
                    400,
                )
        else:
            return jsonify({"error": "permission_ids phải có định dạng "}), 400

        # Gọi service để thêm chức năng vào nhóm quyền
        result = RoleGroupService.add_functions_to_role_group(
            role_id, permission_ids_list
        )

        if result:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Có lỗi khi thêm quyền vào nhóm quyền."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@login_required
@role_group_bp.route("/<int:role_group_id>", methods=["GET"])
@required
def get_role_group_by_id(role_group_id):
    role_group = RoleGroupService.get_role_group_by_id(role_group_id)
    if role_group:
        return jsonify(role_group.to_dict()), 200
    return jsonify({"error": "Role group not found"}), 404


@login_required
@role_group_bp.route(
    "/remove_staff/role_group=<int:role_group_id>&account_id=<int:account_id>",
    methods=["DELETE"],
)
@required
def remove_staff_from_role_group(role_group_id, account_id):
    try:
        print("reomoce")
        result = RoleGroupService.remove_staff_from_group(role_group_id, account_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@login_required
@role_group_bp.route(
    "/get_staffs_not_in_role_group/<int:role_group_id>", methods=["GET"]
)
@required
def get_staffs_not_in_role_group(role_group_id):
    staffs = RoleGroupService.get_staffs_not_in_role_group(role_group_id)
    return jsonify(staffs), 200


@login_required
@role_group_bp.route("/", methods=["POST"])
@required
def create_role_group():
    data = request.get_json()
    result = RoleGroupService.create_role_group(data)
    if result.get("success"):
        return jsonify({"message": "Role group created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@login_required
@role_group_bp.route("/<int:role_group_id>", methods=["PUT"])
@required
def update_role_group(role_group_id):
    data = request.get_json()
    result = RoleGroupService.update_role_group(role_group_id, data)
    if result.get("success"):
        return jsonify({"message": "Role group updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@role_group_bp.route("/<int:role_group_id>", methods=["DELETE"])
@required
def delete_role_group(role_group_id):
    result = RoleGroupService.delete_role_group(role_group_id)
    if result.get("success"):
        return jsonify({"message": "Role group deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
