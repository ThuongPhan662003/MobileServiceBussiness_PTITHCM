from app.repositories.report_repository import ReportRepository


class ReportService:
    @staticmethod
    def get_filtered_revenue(start_date, end_date, plan_code=None, service_id=None):
        return ReportRepository.get_revenue_report(
            start_date, end_date, plan_code, service_id
        )
