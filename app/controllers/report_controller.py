from flask import Blueprint, jsonify, render_template, request

from app.services.plan_service import PlanService
from app.services.report_service import ReportService
from app.services.service_service import ServiceService
from flask_login import login_required
from app.utils.decorator import required

report_bp = Blueprint("report_bp", __name__, url_prefix="/reports")


@login_required
@report_bp.route("/revenue", methods=["GET"])
@required
def revenue_report_view():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
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
        "reports/revenue_chart.html",
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


@login_required
@report_bp.route("/revenue/data", methods=["GET"])
@required
def revenue_data_api():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    plan_code = request.args.get("plan_code") or None
    service_id = request.args.get("service_id", type=int)
    chart_type = request.args.get("chart_type", "bar")

    data = ReportService.get_filtered_revenue(
        start_date, end_date, plan_code, service_id
    )

    chart_labels = [row["payment_day"] for row in data]
    chart_values = [row["total_revenue"] for row in data]

    return jsonify(
        {
            "chart_type": chart_type,
            "labels": chart_labels,
            "values": chart_values,
            "table": data,
        }
    )
