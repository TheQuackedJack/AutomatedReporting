import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from report_engine_manager import ReportEngineManager

if __name__ == "__main__":
    # Resolve absolute paths
    configs_path = os.path.abspath("configs")
    output_path = os.path.abspath(".")

    # Example usage
    manager = ReportEngineManager(
        tar_file_dir="images",
        config_dir=configs_path
    )

    # Load and run the report engine
    try:
        manager.load_docker_image("sales-report-engine")
        manager.run_report_engine(
            image_name="sales-report-engine",
            config_file_name="config.json",
            output_file=os.path.join(output_path, "report.txt")  # Absolute path for output
        )
    except Exception as e:
        print(f"Error: {e}")
