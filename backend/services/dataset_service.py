from __future__ import annotations

from pathlib import Path

import pandas as pd

from backend.models.dataset_report import (
    ColumnTypeSummary,
    DatasetFileInfo,
    DatasetPreview,
    DatasetReport,
    DatasetStructure,
)


class DatasetService:
    """
    Builds a DatasetReport from a pandas DataFrame.

    This service is responsible for converting raw dataset
    information into the structured DatasetReport model used
    throughout the reporting pipeline.

    No analysis or business rules are executed here.
    """

    def build(
        self,
        df: pd.DataFrame,
        *,
        file_name: str | None = None,
        file_path: str | None = None,
        encoding: str | None = None,
    ) -> DatasetReport:
        """
        Build a complete DatasetReport.
        """

        report = DatasetReport()

        report.file = self._build_file_info(
            df=df,
            file_name=file_name,
            file_path=file_path,
            encoding=encoding,
        )

        report.structure = self._build_structure(df)

        report.column_types = self._build_column_summary(df)

        report.preview = self._build_preview(df)

        report.metadata = {
            "engine": "DatasetService",
            "version": "8.3",
        }

        return report

    # ==========================================================
    # File Information
    # ==========================================================

    def _build_file_info(
        self,
        *,
        df: pd.DataFrame,
        file_name: str | None,
        file_path: str | None,
        encoding: str | None,
    ) -> DatasetFileInfo:

        info = DatasetFileInfo()

        info.name = file_name or ""

        info.path = file_path

        info.encoding = encoding

        if file_name:
            info.file_format = Path(file_name).suffix.lstrip(".").lower()

        memory_mb = (
            df.memory_usage(deep=True).sum()
            / (1024 * 1024)
        )

        info.memory_usage = f"{memory_mb:.2f} MB"

        if file_path:
            try:
                size_mb = (
                    Path(file_path).stat().st_size
                    / (1024 * 1024)
                )
                info.file_size = f"{size_mb:.2f} MB"
            except OSError:
                info.file_size = None

        return info

    # ==========================================================
    # Dataset Structure
    # ==========================================================

    def _build_structure(
        self,
        df: pd.DataFrame,
    ) -> DatasetStructure:

        return DatasetStructure(
            total_rows=len(df),
            total_columns=len(df.columns),
            total_cells=df.shape[0] * df.shape[1],
        )

    # ==========================================================
    # Column Type Summary
    # ==========================================================

    def _build_column_summary(
        self,
        df: pd.DataFrame,
    ) -> ColumnTypeSummary:

        summary = ColumnTypeSummary()

        for dtype in df.dtypes:

            if pd.api.types.is_bool_dtype(dtype):
                summary.boolean += 1

            elif pd.api.types.is_numeric_dtype(dtype):
                summary.numeric += 1

            elif pd.api.types.is_datetime64_any_dtype(dtype):
                summary.datetime += 1

            elif pd.api.types.is_string_dtype(dtype):
                summary.text += 1

            elif (
                pd.api.types.is_categorical_dtype(dtype)
                or dtype == "category"
            ):
                summary.categorical += 1

            else:
                summary.other += 1

        return summary

    # ==========================================================
    # Dataset Preview
    # ==========================================================

    def _build_preview(
        self,
        df: pd.DataFrame,
        max_rows: int = 5,
    ) -> DatasetPreview:

        preview = DatasetPreview(
            max_rows=max_rows,
        )

        preview.rows = (
            df.head(max_rows)
            .where(pd.notna(df.head(max_rows)), None)
            .to_dict(orient="records")
        )

        return preview