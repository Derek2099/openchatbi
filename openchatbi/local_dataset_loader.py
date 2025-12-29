"""Local dataset loader using pandas for reading various file formats."""

import logging
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class LocalDataset(BaseModel):
    """Configuration for a local dataset."""

    name: str = Field(description="Dataset name/identifier")
    path: str = Field(description="Path to the dataset file")
    description: str = Field(default="", description="Description of the dataset")
    file_type: str = Field(default="csv", description="File type: csv, excel, parquet, json")
    options: dict[str, Any] = Field(default_factory=dict, description="Pandas read options")

    def load(self) -> pd.DataFrame:
        """Load the dataset using pandas.

        Returns:
            pd.DataFrame: Loaded dataset

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file type is not supported
            Exception: If there's an error reading the file
        """
        file_path = Path(self.path)

        if not file_path.exists():
            raise FileNotFoundError(f"Dataset file not found: {self.path}")

        try:
            if self.file_type.lower() == "csv":
                return pd.read_csv(file_path, **self.options)
            elif self.file_type.lower() in ["excel", "xlsx", "xls"]:
                return pd.read_excel(file_path, **self.options)
            elif self.file_type.lower() == "parquet":
                return pd.read_parquet(file_path, **self.options)
            elif self.file_type.lower() == "json":
                return pd.read_json(file_path, **self.options)
            else:
                raise ValueError(f"Unsupported file type: {self.file_type}")
        except Exception as e:
            logger.error(f"Error loading dataset {self.name} from {self.path}: {e}")
            raise


class LocalDatasetManager:
    """Manager for local datasets."""

    def __init__(self, datasets_config: list[dict[str, Any]] = None):
        """Initialize the local dataset manager.

        Args:
            datasets_config: List of dataset configurations
        """
        self.datasets: dict[str, LocalDataset] = {}

        if datasets_config:
            for config in datasets_config:
                dataset = LocalDataset(**config)
                self.datasets[dataset.name] = dataset

    def add_dataset(self, dataset: LocalDataset) -> None:
        """Add a dataset to the manager.

        Args:
            dataset: LocalDataset instance to add
        """
        self.datasets[dataset.name] = dataset

    def get_dataset(self, name: str) -> pd.DataFrame:
        """Get a loaded dataset by name.

        Args:
            name: Dataset name

        Returns:
            pd.DataFrame: Loaded dataset

        Raises:
            KeyError: If dataset name not found
        """
        if name not in self.datasets:
            raise KeyError(f"Dataset '{name}' not found. Available datasets: {list(self.datasets.keys())}")

        return self.datasets[name].load()

    def list_datasets(self) -> list[dict[str, str]]:
        """List all available datasets with their descriptions.

        Returns:
            List of dataset information dictionaries
        """
        return [
            {
                "name": dataset.name,
                "path": dataset.path,
                "description": dataset.description,
                "file_type": dataset.file_type,
            }
            for dataset in self.datasets.values()
        ]

    def get_dataset_info(self, name: str) -> dict[str, Any]:
        """Get information about a dataset without loading it.

        Args:
            name: Dataset name

        Returns:
            Dictionary with dataset metadata

        Raises:
            KeyError: If dataset name not found
        """
        if name not in self.datasets:
            raise KeyError(f"Dataset '{name}' not found. Available datasets: {list(self.datasets.keys())}")

        dataset = self.datasets[name]
        file_path = Path(dataset.path)

        info = {
            "name": dataset.name,
            "path": dataset.path,
            "description": dataset.description,
            "file_type": dataset.file_type,
            "exists": file_path.exists(),
        }

        if file_path.exists():
            info["file_size"] = file_path.stat().st_size

        return info

    def load_all_datasets(self) -> dict[str, pd.DataFrame]:
        """Load all datasets.

        Returns:
            Dictionary mapping dataset names to DataFrames
        """
        loaded = {}
        for name in self.datasets:
            try:
                loaded[name] = self.get_dataset(name)
                logger.info(f"Successfully loaded dataset: {name}")
            except Exception as e:
                logger.error(f"Failed to load dataset {name}: {e}")

        return loaded
