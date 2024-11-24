import sys
import os

# Add the src folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from report_engine import ReportEngine
from pydantic import BaseModel
from typing import List


class SalesReportInputModel(BaseModel):
    report_title: str
    sales_data: List[float]
    include_summary: bool = True


class SalesReportEngine(ReportEngine):
    def __init__(self):
        super().__init__(input_model=SalesReportInputModel)

    def run_report(self, input_config: dict) -> bytes:
        """
        Generates a sales report.
        """
        config = self.input_model(**input_config)
        lines = [f"Report Title: {config.report_title}", "-" * 40]
        lines.extend([f"Sale: ${sale:.2f}" for sale in config.sales_data])
        if config.include_summary:
            total = sum(config.sales_data)
            average = total / len(config.sales_data) if config.sales_data else 0
            lines.append(f"Total: ${total:.2f}")
            lines.append(f"Average: ${average:.2f}")
        return "\n".join(lines).encode("utf-8")


if __name__ == "__main__":
    engine = SalesReportEngine()
    engine.create_docker_image(
        image_name="sales-report-engine",
        output_image_path="sales-report-engine.tar"
    )
