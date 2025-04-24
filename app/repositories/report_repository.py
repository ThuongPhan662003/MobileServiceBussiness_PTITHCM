from app.database import db_instance


class ReportRepository:
    @staticmethod
    def get_revenue_report(start_date, end_date, plan_code=None, service_id=None):
        try:
            print("dữ liệu", start_date, end_date, plan_code, service_id)
            result = db_instance.execute(
                "CALL sp_revenue_report_by_date_range (%s, %s,%s, %s)",
                (start_date, end_date, plan_code, service_id),
                fetchall=True,
            )
            print("kết quả", result)
            reports = []

            print("SP result:", result)
            for row in result[0]:  # lấy từ fetchall=True nên cần duyệt result[0]
                report = {
                    "payment_day": row.get("payment_day"),
                    "total_payments": row.get("total_payments"),
                    "total_revenue": row.get("total_revenue"),
                    "unique_subscribers": row.get("unique_subscribers"),
                    "plan_code": row.get("plan_code"),
                    "service_id": row.get("service_id"),
                }
                reports.append(report)

            return reports

        except Exception as e:
            print(f"Lỗi khi gọi báo cáo doanh thu: {e}")
            return []
