from flask import Blueprint, render_template, request, session
from flask_login import current_user
from flask_login import login_required
from app.utils.decorator import required
from app.services.plan_service import PlanService
from app.services.report_service import ReportService
from app.services.service_service import ServiceService
from datetime import datetime, timedelta


admin_main_bp = Blueprint("admin_main_bp", __name__, url_prefix="/admin")


@login_required
@admin_main_bp.route("/")
@login_required
def index():
    today = datetime.today().date()
    default_start_date = (
        today - timedelta(days=30)
    ).isoformat()  # Mặc định từ 30 ngày trước
    default_end_date = today.isoformat()

    # Lấy ngày từ request hoặc dùng mặc định
    start_date = request.args.get("start_date") or default_start_date
    end_date = request.args.get("end_date") or default_end_date

    plan_code = request.args.get("plan_code") or None
    service_id = request.args.get("service_id", type=int)
    chart_type = request.args.get("chart_type", "bar")

    data = ReportService.get_filtered_revenue(
        start_date, end_date, plan_code, service_id
    )

    plan_codes = PlanService.get_all_codes()
    services = ServiceService.get_all_services()

    chart_labels = [row["payment_day"] for row in data]
    chart_values = [row["total_revenue"] for row in data]

    return render_template(
        "admin_home/index.html",
        data=data,
        chart_labels=chart_labels,
        chart_values=chart_values,
        chart_type=chart_type,
        plan_codes=plan_codes,
        services=services,
        filters={
            "start_date": start_date,
            "end_date": end_date,
            "plan_code": plan_code,
            "service_id": service_id,
            "chart_type": chart_type,
        },
    )
