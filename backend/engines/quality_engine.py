from __future__ import annotations

import pandas as pd

from backend.core.base_engine import BaseEngine
from backend.models.quality_report import QualityReport


class QualityEngine(BaseEngine):
    """
    Performs quality analysis on tabular datasets.
    """

    def analyze(self, df: pd.DataFrame) -> QualityReport:
        """
        Analyze a dataset and generate a quality report.
        """

        start = self.log_start("Quality Analysis")

        report = QualityReport()

        report.total_rows = len(df)
        report.total_columns = len(df.columns)

        report.missing_values = int(
            df.isna().sum().sum()
        )

        report.missing_value_summary = self._analyze_missing_values(df)

        report.duplicate_rows = int(
            df.duplicated().sum()
        )

        report.duplicate_row_summary = self._analyze_duplicate_rows(df)

        report.duplicate_columns = len(
            self._find_duplicate_columns(df)
        )

        report.duplicate_column_summary = self._analyze_duplicate_columns(df)

        report.data_type_summary = self._analyze_data_types(df)

        self.log_finish(
            "Quality Analysis",
            start,
        )

        return report

    def _analyze_missing_values(
        self,
        df: pd.DataFrame,
    ) -> dict[str, dict[str, float | int]]:

        summary: dict[str, dict[str, float | int]] = {}

        total_rows = len(df)

        if total_rows == 0:
            return summary

        missing_counts = df.isna().sum()

        for column, count in missing_counts.items():

            if count == 0:
                continue

            summary[column] = {
                "count": int(count),
                "percentage": round(
                    (count / total_rows) * 100,
                    2,
                ),
            }

        return summary

    def _analyze_duplicate_rows(
        self,
        df: pd.DataFrame,
    ) -> dict[str, float | int]:

        total_rows = len(df)

        duplicate_count = int(df.duplicated().sum())

        percentage = (
            round((duplicate_count / total_rows) * 100, 2)
            if total_rows > 0
            else 0.0
        )

        return {
            "count": duplicate_count,
            "percentage": percentage,
        }

    def _find_duplicate_columns(
        self,
        df: pd.DataFrame,
    ) -> list[str]:

        duplicate_columns: list[str] = []

        columns = list(df.columns)

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                if df[columns[i]].equals(df[columns[j]]):
                    duplicate_columns.append(columns[j])

        return duplicate_columns

    def _analyze_duplicate_columns(
        self,
        df: pd.DataFrame,
    ) -> dict[str, list[str]]:

        summary: dict[str, list[str]] = {}

        columns = list(df.columns)

        for i in range(len(columns)):

            duplicates: list[str] = []

            for j in range(i + 1, len(columns)):

                if df[columns[i]].equals(df[columns[j]]):
                    duplicates.append(columns[j])

            if duplicates:
                summary[columns[i]] = duplicates

        return summary

    def _analyze_data_types(
        self,
        df: pd.DataFrame,
    ) -> dict[str, str]:
        """
        Generate a mapping of each column to its pandas data type.
        """

        summary: dict[str, str] = {}

        for column in df.columns:
            summary[column] = str(df[column].dtype)

        return summary