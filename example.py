# example.py

import logging
import os
import shutil
from pydantic import BaseModel, Field
from report_engine import ReportEngine

# Pydantic models
class ReportInputModel(BaseModel):
    title: str
    content: str

class ReportDistributionModel(BaseModel):
    target_folder: str
    output_path: str = Field(..., description="Path where the report will be saved.")

# Implementation class
class SimpleTextReportEngine(ReportEngine):
    def __init__(self):
        super().__init__(ReportInputModel, ReportDistributionModel)

    def run(self, report_config: dict):
        try:
            self._validate_config(self.input_model, report_config)
            logging.info("Generating report...")

            # Use a temporary output path during generation
            temp_output_path = "./temp_report.txt"

            # Generate the report
            with open(temp_output_path, "w") as f:
                f.write(f"Title: {report_config['title']}\n\n")
                f.write(report_config['content'])
            logging.info(f"Report successfully generated at {temp_output_path}")

            # Store the temporary output path for use in distribution
            self.temp_output_path = temp_output_path
        except Exception as e:
            logging.error(f"Failed to generate report: {e}")
            raise

    def distribute(self, distribution_config: dict):
        try:
            self._validate_config(self.distribution_model, distribution_config)
            logging.info("Distributing report...")

            output_path = distribution_config.get('output_path')
            target_folder = distribution_config.get('target_folder')

            if not hasattr(self, 'temp_output_path'):
                raise ValueError("No report generated to distribute.")

            # Ensure the target folder exists
            os.makedirs(target_folder, exist_ok=True)

            # Move the report to the desired output path within the target folder
            final_output_path = os.path.join(target_folder, output_path)
            shutil.move(self.temp_output_path, final_output_path)
            logging.info(f"Report successfully moved to {final_output_path}")
        except Exception as e:
            logging.error(f"Failed to distribute report: {e}")
            raise
