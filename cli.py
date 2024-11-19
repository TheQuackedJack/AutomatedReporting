# cli.py

import typer
import logging
import sys
import json
from report_engine import ReportEngine  # Import the base class for loading
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

app = typer.Typer()

@app.callback(invoke_without_command=True)
def run_workflow(
    pickle_file: str = typer.Argument(..., help="Path to the pickled ReportEngine file."),
    report_config_file: str = typer.Argument(..., help="Path to the report configuration JSON file."),
    distribution_config_file: str = typer.Argument(..., help="Path to the distribution configuration JSON file.")
):
    """
    Run the full workflow: load the engine, generate a report, and distribute it.

    Args:
        pickle_file (str): Path to the pickled ReportEngine file.
        report_config_file (str): Path to the report configuration JSON file.
        distribution_config_file (str): Path to the distribution configuration JSON file.
    """
    try:
        # Load the engine
        if not os.path.exists(pickle_file):
            logging.error(f"Pickle file '{pickle_file}' not found. Please provide a valid pickle file.")
            sys.exit(1)
        try:
            engine = ReportEngine.load_from_file(pickle_file)
            logging.info(f"Loaded ReportEngine from {pickle_file}.")
        except Exception as e:
            logging.error(f"Failed to load the engine from '{pickle_file}': {e}")
            sys.exit(1)

        # Load configurations from the provided JSON files
        try:
            with open(report_config_file, 'r') as f:
                report_config_dict = json.load(f)
        except FileNotFoundError:
            logging.error(f"Report configuration file '{report_config_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in report configuration file: {e}")
            sys.exit(1)

        try:
            with open(distribution_config_file, 'r') as f:
                distribution_config_dict = json.load(f)
        except FileNotFoundError:
            logging.error(f"Distribution configuration file '{distribution_config_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in distribution configuration file: {e}")
            sys.exit(1)

        # Run the workflow
        logging.info("Running the report generation...")
        engine.run(report_config_dict)
        logging.info("Report generation completed.")

        logging.info("Distributing the report...")
        engine.distribute(distribution_config_dict)
        logging.info("Report distribution completed.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
