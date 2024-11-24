# report_engine.py

import pickle
import json
import logging
from abc import ABC, abstractmethod
from typing import Type, Optional, Any
from pydantic import BaseModel, ValidationError
import typer
from pathlib import Path

class ReportEngine(ABC):
    def __init__(self, input_model: Type[BaseModel]):
        """
        Class for making user-defined report engines.
        """
        if not input_model:
            raise ValueError("There must be an input model.")
        if not issubclass(input_model, BaseModel):
            raise ValueError("The input model must be a Pydantic model.")
        
        self.input_model = input_model
        self.app = typer.Typer(help=f"CLI for {self.__class__.__name__}")
        self.app.command("generate-report")(self._generate_report_cli)
        self.app.command("export-input-model")(self._export_input_model_cli)

    def _validate_config(self, config: dict) -> None:
        """Validate a configuration against the input model."""
        try:
            self.input_model(**config)
            logging.info("Configuration validation successful.")
        except ValidationError as e:
            logging.error(f"Configuration validation failed: {e}")
            raise ValueError(f"Invalid configuration: {e}") from e

    @abstractmethod
    def run_report(self, input_config: dict) -> bytes:
        """User-defined report generation logic. Should return the report bytestream."""
        pass

    def generate_report(self, input_config: dict, output_file: str) -> None:
        """
        Generates the report based on the user-defined report running logic.
        Validates the input and creates the report file.
        """
        self._validate_config(input_config)
        report_contents = self.run_report(input_config)
        with open(output_file, "wb") as report:
            report.write(report_contents)

    def export_input_model(self, output_file: str):
        """
        Exports the input model using pickle to ensure field validators are preserved.
        """
        serialized_model = pickle.dumps(self.input_model)
        with open(output_file, "wb") as f:
            f.write(serialized_model)
        logging.info(f"Input model exported to {output_file}")

    def _generate_report_cli(
        self,
        output_file: str = typer.Option(
            ..., "--output-file", "-o", help="Output file path for the generated report."
        ),
        config_file: Optional[Path] = typer.Option(
            None, "--config-file", "-c", help="Path to JSON file with input configuration."
        ),
    ):
        """
        Generate a report.
        """
        if config_file:
            # Load configuration from JSON file
            with open(config_file, "r", encoding='utf-8') as f:
                input_config = json.load(f)
        else:
            # Collect input parameters interactively
            input_config = self._collect_input_parameters()
        
        try:
            self.generate_report(input_config, output_file)
            typer.echo(f"Report generated and saved to {output_file}")
        except ValueError as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(code=1)

    def _export_input_model_cli(
        self,
        output_file: str = typer.Option(
            ..., "--output-file", "-o", help="Output file path to save the input model."
        ),
    ):
        """
        Export the input model.
        """
        self.export_input_model(output_file)
        typer.echo(f"Input model exported to {output_file}")

    def _collect_input_parameters(self) -> dict:
        """
        Collect input parameters interactively based on the input model fields.
        """
        input_config = {}
        for field_name, field in self.input_model.__fields__.items():
            field_type = field.outer_type_
            prompt = f"{field_name} ({field_type})"
            default = field.default if not field.required else None
            while True:
                value = typer.prompt(prompt, default=default)
                try:
                    # For lists, split the input and convert each item
                    if hasattr(field_type, '__origin__') and field_type.__origin__ == list:
                        item_type = field_type.__args__[0]
                        input_list = [item_type(item.strip()) for item in value.split(',')]
                        input_config[field_name] = input_list
                    else:
                        input_config[field_name] = field_type(value)
                    break
                except ValueError:
                    typer.echo(f"Invalid value for {field_name}. Expected type {field_type}. Please try again.")
        return input_config

    def run_cli(self):
        """
        Runs the Typer CLI application.
        """
        self.app(prog_name=self.__class__.__name__)