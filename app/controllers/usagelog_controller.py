from flask import Blueprint, request, jsonify, render_template
from app.services.usagelog_service import UsageLogService
from flask_login import login_required
from app.utils.decorator import required


usagelog_bp = Blueprint("usagelog", __name__, url_prefix="/usagelogs")


@login_required
@usagelog_bp.route("/", methods=["GET"])
@required
def get_all_usagelogs():
    try:
        tinnhan_logs = UsageLogService.get_logs_by_type("TINNHAN")
        cuocgoi_logs = UsageLogService.get_logs_by_type("CUOCGOI")
        dulieu_logs = UsageLogService.get_logs_by_type("DULIEU")
        return (
            render_template(
                "UsagelogHistory/index.html",
                tinnhan_logs=tinnhan_logs,
                cuocgoi_logs=cuocgoi_logs,
                dulieu_logs=dulieu_logs,
                active_tab="tinnhan",  # Mặc định là tab Tin nhắn
            ),
            200,
        )
    except Exception as e:
        print(f"Lỗi trong get_all_usagelogs: {e}")
        return (
            render_template(
                "UsagelogHistory/index.html", error=str(e), active_tab="tinnhan"
            ),
            500,
        )


@login_required
@usagelog_bp.route("/<int:log_id>", methods=["GET"])
@required
def get_usagelog_by_id(log_id):
    try:
        usagelog = UsageLogService.get_usagelog_by_id(log_id)
        if usagelog:
            return jsonify(usagelog.to_dict()), 200
        return jsonify({"error": "Usage log not found"}), 404
    except Exception as e:
        print(f"Lỗi trong get_usagelog_by_id: {e}")
        return jsonify({"error": str(e)}), 500


@usagelog_bp.route("/", methods=["POST"])
@login_required
@required
def create_usagelog():
    try:
        data = request.get_json()
        log_type = data.get("type")
        result = UsageLogService.add_usagelog(log_type, data)

        if result.get("success"):
            return (
                jsonify(
                    {
                        "status_code": 201,
                        "data": None,
                        "message": "Usage log created successfully",
                        "error": None,
                    }
                ),
                201,
            )

        return (
            jsonify(
                {
                    "status_code": 400,
                    "data": None,
                    "message": "Failed to create usage log",
                    "error": result.get("error"),
                }
            ),
            400,
        )

    except Exception as e:
        print(f"Lỗi trong create_usagelog: {e}")
        return (
            jsonify(
                {
                    "status_code": 500,
                    "data": None,
                    "message": "Server error occurred",
                    "error": str(e),
                }
            ),
            500,
        )


@login_required
@usagelog_bp.route("/history", methods=["GET"])
@required
def usage_log_history():
    try:
        tinnhan_logs = UsageLogService.get_logs_by_type("TINNHAN")
        cuocgoi_logs = UsageLogService.get_logs_by_type("CUOCGOI")
        dulieu_logs = UsageLogService.get_logs_by_type("DULIEU")
        return (
            render_template(
                "UsagelogHistory/index.html",
                tinnhan_logs=tinnhan_logs,
                cuocgoi_logs=cuocgoi_logs,
                dulieu_logs=dulieu_logs,
                active_tab="tinnhan",  # Mặc định là tab Tin nhắn
            ),
            200,
        )
    except Exception as e:
        print(f"Lỗi trong usage_log_history: {e}")
        return (
            render_template(
                "UsagelogHistory/index.html", error=str(e), active_tab="tinnhan"
            ),
            500,
        )


@login_required
@usagelog_bp.route("/search/<string:log_type>", methods=["POST"])
@required
def search_usagelogs(log_type):
    try:
        data = request.form
        subscriber_id = data.get("subscriber_id")
        start_date = data.get("start_date")
        logs = UsageLogService.search_usagelogs(
            log_type.upper(), subscriber_id, start_date
        )
        tinnhan_logs = (
            logs
            if log_type.upper() == "TINNHAN"
            else UsageLogService.get_logs_by_type("TINNHAN")
        )
        cuocgoi_logs = (
            logs
            if log_type.upper() == "CUOCGOI"
            else UsageLogService.get_logs_by_type("CUOCGOI")
        )
        dulieu_logs = (
            logs
            if log_type.upper() == "DULIEU"
            else UsageLogService.get_logs_by_type("DULIEU")
        )
        return (
            render_template(
                "UsagelogHistory/index.html",
                tinnhan_logs=tinnhan_logs,
                cuocgoi_logs=cuocgoi_logs,
                dulieu_logs=dulieu_logs,
                active_tab=log_type.lower(),  # Đặt tab hiện tại dựa trên log_type
            ),
            200,
        )
    except Exception as e:
        print(f"Lỗi trong search_usagelogs: {e}")
        return (
            render_template(
                "UsagelogHistory/index.html", error=str(e), active_tab=log_type.lower()
            ),
            500,
        )


@login_required
@usagelog_bp.route("/add/<string:log_type>", methods=["POST"])
@required
def add_usagelog(log_type):
    try:
        data = request.form
        result = UsageLogService.add_usagelog(log_type.upper(), data)
        if result.get("success"):
            return usage_log_history()  # Gọi lại history, mặc định tab Tin nhắn
        else:
            tinnhan_logs = UsageLogService.get_logs_by_type("TINNHAN")
            cuocgoi_logs = UsageLogService.get_logs_by_type("CUOCGOI")
            dulieu_logs = UsageLogService.get_logs_by_type("DULIEU")
            return (
                render_template(
                    "UsagelogHistory/index.html",
                    tinnhan_logs=tinnhan_logs,
                    cuocgoi_logs=cuocgoi_logs,
                    dulieu_logs=dulieu_logs,
                    error=result.get("error"),
                    active_tab=log_type.lower(),  # Giữ tab hiện tại
                ),
                400,
            )
    except Exception as e:
        print(f"Lỗi trong add_usagelog: {e}")
        return (
            render_template(
                "UsagelogHistory/index.html", error=str(e), active_tab=log_type.lower()
            ),
            500,
        )


@login_required
@usagelog_bp.route("/reset/<string:log_type>", methods=["GET"])
@required
def reset_usagelogs(log_type):
    try:
        tinnhan_logs = UsageLogService.get_logs_by_type("TINNHAN")
        cuocgoi_logs = UsageLogService.get_logs_by_type("CUOCGOI")
        dulieu_logs = UsageLogService.get_logs_by_type("DULIEU")
        return (
            render_template(
                "UsagelogHistory/index.html",
                tinnhan_logs=tinnhan_logs,
                cuocgoi_logs=cuocgoi_logs,
                dulieu_logs=dulieu_logs,
                active_tab=log_type.lower(),  # Đặt tab hiện tại dựa trên log_type
            ),
            200,
        )
    except Exception as e:
        print(f"Lỗi trong reset_usagelogs: {e}")
        return (
            render_template(
                "UsagelogHistory/index.html", error=str(e), active_tab=log_type.lower()
            ),
            500,
        )
