import json
import logging
from abc import ABC, abstractmethod
from typing import Type, Optional, List
from pydantic import BaseModel, ValidationError
import typer
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import inspect
import subprocess
import os
import shutil


class ReportEngine(ABC):
    def __init__(self, input_model: Type[BaseModel]):
        """
        Abstract base class for defining report engines.
        """
        if not input_model or not issubclass(input_model, BaseModel):
            raise ValueError("The input model must be a valid Pydantic model.")
        
        self.input_model = input_model
        self.app = typer.Typer(help=f"CLI for {self.__class__.__name__}")
        self.app.command("generate-report")(self._generate_report_cli)

    def _validate_config(self, config: dict) -> None:
        """
        Validate the input configuration using the defined Pydantic model.
        """
        try:
            self.input_model(**config)
        except ValidationError as e:
            raise ValueError(f"Invalid configuration: {e}")

    @abstractmethod
    def run_report(self, input_config: dict) -> bytes:
        """
        Abstract method for generating a report. Must be implemented by subclasses.
        """
        pass

    def generate_report(self, input_config: dict, output_file: str) -> None:
        """
        Validate the input configuration and write the generated report to a file.
        """
        self._validate_config(input_config)
        report_data = self.run_report(input_config)
        with open(output_file, "wb") as f:
            f.write(report_data)

    def _generate_report_cli(
        self,
        config_file: Path = typer.Option(
            None, "--config-file", "-c", help="Path to the JSON configuration file."
        ),
        output_file: str = typer.Option(
            ..., "--output-file", "-o", help="Path to the output file."
        ),
    ):
        """
        CLI command for generating a report.
        """
        if config_file:
            with open(config_file, "r") as f:
                input_config = json.load(f)
        else:
            raise ValueError("A config file is required.")
        
        self.generate_report(input_config, output_file)
        typer.echo(f"Report generated at {output_file}.")

    def run_cli(self):
        """
        Run the CLI application.
        """
        self.app()


    def create_docker_image(
        self,
        image_name: str,
        base_image: str = "python:3.9-slim",
        dockerfile_path: str = "Dockerfile",
        temp_build_dir: str = "temp_build",
        entry_script_name: str = "entrypoint.py",
    ):
        """
        Creates a Docker image for the report engine using Jinja2 templates.

        Args:
            image_name (str): Name of the Docker image to build.
            base_image (str): Base Docker image to use.
            dockerfile_path (str): Path to save the generated Dockerfile.
            temp_build_dir (str): Temporary build directory to act as the Docker context.
            entry_script_name (str): Name of the entrypoint script to be created.
        """
        # Ensure the temporary build directory exists
        temp_build_path = Path(temp_build_dir)
        if temp_build_path.exists():
            shutil.rmtree(temp_build_path)  # Clear old build directory
        temp_build_path.mkdir()

        # Jinja2 setup
        env = Environment(loader=FileSystemLoader(str(Path(__file__).parent / "templates")))
        docker_template = env.get_template("Dockerfile.jinja")
        entry_template = env.get_template("entrypoint.jinja")

        # Detect the module and class where the subclass is defined
        subclass_file = inspect.getfile(self.__class__)  # File where the subclass is defined
        module_name = Path(subclass_file).stem          # Module name (without .py)
        class_name = self.__class__.__name__

        # Detect the file where the abstract ReportEngine class is defined
        base_class_file = inspect.getfile(type(self))   # File where ReportEngine is defined
        base_class_filename = Path(base_class_file).name

        # Write requirements.txt
        requirements = ["pydantic", "typer", "jinja2"]
        with open(temp_build_path / "requirements.txt", "w") as f:
            f.write("\n".join(requirements))

        # Generate entrypoint.py
        entry_script_content = entry_template.render(module_name=module_name, class_name=class_name)
        with open(temp_build_path / entry_script_name, "w") as f:
            f.write(entry_script_content)

        # Copy all required files to the temporary build directory
        shutil.copy2(subclass_file, temp_build_path / Path(subclass_file).name)
        shutil.copy2(base_class_file, temp_build_path / base_class_filename)
        shutil.copy2(__file__, temp_build_path / Path(__file__).name)

        # Generate Dockerfile in the temporary build directory
        dockerfile_content = docker_template.render(
            base_image=base_image,
            files_to_copy=["requirements.txt", entry_script_name, 
                        Path(subclass_file).name, Path(__file__).name],
            entry_script_name=entry_script_name,
        )
        with open(temp_build_path / dockerfile_path, "w") as f:
            f.write(dockerfile_content)

        # Build Docker image using the temporary build directory as context
        build_command = [
            "docker", "build", "-t", image_name, "-f", str(temp_build_path / dockerfile_path), str(temp_build_path)
        ]
        try:
            subprocess.run(build_command, check=True)
            logging.info(f"Docker image '{image_name}' created successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to build Docker image: {e}")
            raise
        finally:
            # Clean up temporary build directory (optional)
            shutil.rmtree(temp_build_path)