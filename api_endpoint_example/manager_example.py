# manager_example.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from report_engine_manager import ReportEngineManager

if __name__ == "__main__":
    # Example usage
    manager = ReportEngineManager(
        tar_file_dir="images"
    )

    # Load and run the report engine
    try:
        manager.load_docker_image("sales-report-engine")
        # Example input data
        input_data = {
            "report_title": "Monthly Sales Report",
            "sales_data": [1000.0, 2000.0, 1500.0],
            "include_summary": True
        }
        report_bytes = manager.run_report_engine(
            image_name="sales-report-engine",
            input_data=input_data
        )
        # Output the report
        report_text = report_bytes.decode('utf-8')
        print(report_text)
    except Exception as e:
        print(f"Error: {e}")
