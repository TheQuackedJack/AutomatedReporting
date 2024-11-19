# report_engine.py

import pickle
import logging
from abc import ABC, abstractmethod
from pydantic import BaseModel

# Abstract base class with pickling functionality
class ReportEngine(ABC):
    def __init__(self, input_model: BaseModel = None, distribution_model: BaseModel = None):
        self.input_model = input_model
        self.distribution_model = distribution_model

    def _validate_config(self, model, config):
        """Validate a configuration against a Pydantic model."""
        if model:
            try:
                model(**config)
                logging.info("Configuration validation successful.")
            except Exception as e:
                logging.error(f"Configuration validation failed: {e}")
                raise

    @abstractmethod
    def run(self, report_config: dict):
        """Create an output based on the configuration."""
        pass

    @abstractmethod
    def distribute(self, distribution_config: dict):
        """Distribute the report to a specific location."""
        pass

    def save_to_file(self, file_path: str):
        """Pickle the engine and save it to a file."""
        try:
            with open(file_path, "wb") as f:
                pickle.dump(self, f)
            logging.info(f"Report engine successfully saved to {file_path}")
        except Exception as e:
            logging.error(f"Failed to save report engine: {e}")
            raise

    @staticmethod
    def load_from_file(file_path: str):
        """Load a pickled engine from a file."""
        try:
            with open(file_path, "rb") as f:
                engine = pickle.load(f)
            logging.info(f"Report engine successfully loaded from {file_path}")
            return engine
        except Exception as e:
            logging.error(f"Failed to load report engine: {e}")
            raise
