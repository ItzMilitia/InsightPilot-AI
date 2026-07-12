from __future__ import annotations
from contextlib import nullcontext
from charset_normalizer import from_bytes
from pathlib import Path
from backend.utils.logger import logger
from typing import BinaryIO, ContextManager, Union
from backend.core.exceptions import (
    DatasetReadError,
    EncodingDetectionError,
    UnsupportedFileError,
)

import pandas as pd


FileLike = Union[str, Path, BinaryIO]


class DataEngine:
    """
    Central engine responsible for reading datasets.

    This class provides a single interface for loading data,
    allowing the underlying processing library to be replaced
    in the future (e.g., Polars or DuckDB) without affecting
    the rest of the application.
    """

    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

    def __init__(self) -> None:
        self._backend = "pandas"

    @property
    def backend(self) -> str:
        """Return the active data processing backend."""
        return self._backend

    def _validate_source(self, source: FileLike) -> None:
        """
        Validate the dataset source before processing.
        """

        if source is None:
            raise DatasetReadError("Dataset source cannot be None.")

        if hasattr(source, "name"):
            return

        if isinstance(source, (str, Path)):
            return

        raise DatasetReadError("Invalid dataset source provided.")

    def _prepare_source(self, source: FileLike,) -> ContextManager[BinaryIO]:
        """
        Convert the dataset source into a readable binary stream.
        """

        if isinstance(source, (str, Path)):
            return open(source, "rb")

        return nullcontext(source)
    
    def load_dataset(self, source: FileLike) -> pd.DataFrame:
        """
        Load a dataset from a file path or uploaded file.
        """
        logger.info(
            "Loading dataset: %s",
            getattr(source, "name", source),
        )
        self._validate_source(source)

        extension = self._get_extension(source)
        logger.info("Detected file type: %s", extension)

        readers = {
            ".csv": self._read_csv,
            ".xlsx": self._read_excel,
            ".xls": self._read_excel,
        }

        reader = readers.get(extension)

        if reader is None:
            raise UnsupportedFileError(
                f"Unsupported file type: '{extension}'. "
                f"Supported formats: {sorted(self.SUPPORTED_EXTENSIONS)}"
            )

        with self._prepare_source(source) as prepared_source:
            df = reader(prepared_source)

            logger.info(
                "Dataset loaded successfully. Rows=%d Columns=%d",
                len(df),
                len(df.columns),
            )

            return df

    def _read_csv(self, source: FileLike) -> pd.DataFrame:
        encoding = self._detect_encoding(source)
        try:
            return pd.read_csv(
                source,
                encoding=encoding
            )

        except Exception as e:
            logger.exception("Failed to read CSV dataset.")

            raise DatasetReadError(
                "Failed to read CSV dataset."
            ) from e

    def _read_excel(self, source: FileLike) -> pd.DataFrame:
        """Read an Excel dataset."""
        try:
            return pd.read_excel(source)

        except Exception as e:
            logger.exception("Failed to read Excel dataset.")

            raise DatasetReadError(
                "Failed to read Excel dataset."
            ) from e

    @staticmethod
    def _get_extension(source: FileLike) -> str:
        """
        Extract the file extension from a path or uploaded file.
        """

        if hasattr(source, "name"):
            return Path(source.name).suffix.lower()

        return Path(source).suffix.lower()
    
    def _detect_encoding(self, source: FileLike) -> str:
        """
        Detect the encoding of a CSV file.
        """
        sample = source.read(10000)

        result = from_bytes(sample).best()

        source.seek(0)

        if result is None:
            raise EncodingDetectionError(
                "Unable to detect the file encoding."
            )

        encoding = result.encoding.lower()

        if encoding == "ascii":
            return "utf-8"

        logger.info("Detected encoding: %s", encoding)

        return encoding