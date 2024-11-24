# report_engine_manager.py

import subprocess
from pathlib import Path
import json
import io




class ReportEngineManager:
    def __init__(self, tar_file_dir: str):
        """
        Initialize the manager with paths for tar files.

        Args:
            tar_file_dir (str): Directory where Docker tar files are stored.
        """
        self.tar_file_dir = Path(tar_file_dir)

        # Ensure directory exists
        if not self.tar_file_dir.exists():
            raise FileNotFoundError(f"Tar file directory not found: {self.tar_file_dir}")

    def load_docker_image(self, image_name: str):
        """
        Load a Docker image from a tar file.

        Args:
            image_name (str): The name of the image to load (e.g., 'sales-report-engine').
        """
        tar_file = self.tar_file_dir / f"{image_name}.tar"

        if not tar_file.exists():
            raise FileNotFoundError(f"Docker image tar file not found: {tar_file}")

        # Load the Docker image
        try:
            subprocess.run(["docker", "load", "-i", str(tar_file)], check=True)
            print(f"Docker image '{image_name}' loaded successfully.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to load Docker image: {e}")

    def run_report_engine(self, image_name: str, input_data: dict) -> bytes:
        """
        Run a Docker container for the specified image and input data.

        Args:
            image_name (str): The name of the Docker image to run.
            input_data (dict): The input data for the report engine.

        Returns:
            bytes: The output report data.
        """
        # Convert input data to JSON
        input_json = json.dumps(input_data)

        # Run the Docker container
        try:
            process = subprocess.Popen(
                [
                    "docker", "run",
                    "-i",  # Enable stdin
                    image_name
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout_data, stderr_data = process.communicate(input=input_json.encode('utf-8'))

            if process.returncode != 0:
                raise RuntimeError(f"Failed to run Docker container: {stderr_data.decode('utf-8')}")

            return stdout_data
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to run Docker container: {e}")

