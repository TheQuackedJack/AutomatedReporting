# test_sales_report_engine.py

import logging
from typing import List
from pydantic import BaseModel, Field
from report_engine import ReportEngine

class SalesReportInputModel(BaseModel):
    report_title: str = Field(..., description="The title of the sales report.")
    sales_data: List[float] = Field(..., description="A list of sales figures.")
    include_summary: bool = Field(
        default=True, description="Whether to include a summary section."
    )

class SalesReportEngine(ReportEngine):
    def __init__(self):
        super().__init__(input_model=SalesReportInputModel)

    def run_report(self, input_config: dict) -> bytes:
        """
        Generates a sales report based on the input configuration.
        """
        # Validate and parse the input configuration using the input model
        config = self.input_model(**input_config)

        # Start building the report content
        report_lines = [f"Report Title: {config.report_title}", "-" * 40]

        # Add sales data
        report_lines.append("Sales Data:")
        for idx, sale in enumerate(config.sales_data, start=1):
            report_lines.append(f"  Item {idx}: ${sale:.2f}")

        # Optionally include a summary
        if config.include_summary:
            total_sales = sum(config.sales_data)
            average_sales = (
                total_sales / len(config.sales_data) if config.sales_data else 0
            )
            report_lines.append("-" * 40)
            report_lines.append(f"Total Sales: ${total_sales:.2f}")
            report_lines.append(f"Average Sale: ${average_sales:.2f}")

        # Join the lines and encode the content as bytes
        report_content = "\n".join(report_lines)
        return report_content.encode("utf-8")

if __name__ == "__main__":
    # Configure logging to display messages
    logging.basicConfig(level=logging.INFO)

    # Instantiate the report engine
    report_engine = SalesReportEngine()

    # Run the CLI
    report_engine.run_cli()
