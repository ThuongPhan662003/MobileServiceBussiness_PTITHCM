from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
from app.forms.service_forms.service_forms import ServiceForm
from app.services.service_service import ServiceService
from flask_login import login_required
from app.utils.decorator import required

service_bp = Blueprint("service_bp", __name__, url_prefix="/services")


def build_tree(services):
    nodes = {
        s.id: {
            "id": s.id,
            "name": s.service_name,
            "parent_id": s.parent_id,
            "children": [],
        }
        for s in services
    }
    root = []
    for s in services:
        node = nodes[s.id]
        if s.parent_id:
            parent = nodes.get(s.parent_id)
            if parent:
                parent["children"].append(node)
        else:
            root.append(node)
    return root


@service_bp.route("/", methods=["GET"])
def service_list():
    all_services = ServiceService.get_all()
    service_tree = build_tree(all_services)
    service_flat = all_services
    return render_template(
        "services/service_list.html",
        service_tree=service_tree,
        flat_services=service_flat,
    )


@login_required
@service_bp.route("/create", methods=["POST"])
@required
def service_create():
    try:
        data = request.get_json()
        print("[REQUEST DATA]", data)

        result = ServiceService.create_service(data)
        print("[SERVICE RESULT]", result)

        if result.get("success") is True:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": result.get("message", "Tạo dịch vụ thành công."),
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": result.get("message", "Tạo dịch vụ thất bại."),
                        "error": result.get("error", None),
                    }
                ),
                400,
            )

    except Exception as e:
        print("[EXCEPTION]", str(e))
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Đã xảy ra lỗi khi xử lý yêu cầu.",
                    "error": str(e),
                }
            ),
            500,
        )


@login_required
@service_bp.route("/<int:service_id>", methods=["PUT"])
@required
def service_edit(service_id):
    data = request.get_json()
    result = ServiceService.update_service(service_id, data)

    if result.get("success"):
        return (
            jsonify(
                {
                    "success": True,
                    "message": result.get("message", "Cập nhật dịch vụ thành công."),
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "success": False,
                "error": True,
                "message": result.get("message", "Cập nhật dịch vụ thất bại."),
            }
        ),
        400,
    )


@login_required
@service_bp.route("/<int:service_id>", methods=["DELETE"])
@required
def service_delete(service_id):
    result = ServiceService.delete_service(service_id)
    if result.get("success"):
        return jsonify({"message": "Service deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


# ----------------------------
# API JSON (nếu cần)
# ----------------------------


@service_bp.route("/<int:service_id>", methods=["GET"])
def get_service_by_id(service_id):
    service = ServiceService.get_service_by_id(service_id)
    print(service)
    if service:
        return jsonify(service.to_dict()), 200
    return jsonify({"error": "Service not found"}), 404
