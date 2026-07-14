from __future__ import annotations

import pandas as pd

from backend.analyzers.outlier_analyzer import OutlierAnalyzer
from backend.core.base_engine import BaseEngine
from backend.core.quality_config import (
    DUPLICATE_COLUMN_WEIGHT,
    DUPLICATE_ROW_WEIGHT,
    EXCELLENT_SCORE,
    FAIR_SCORE,
    GOOD_SCORE,
    MISSING_VALUE_WEIGHT,
    OUTLIER_WEIGHT,
)
from backend.models.quality_report import QualityReport


class QualityEngine(BaseEngine):
    """
    Performs quality analysis on tabular datasets.
    """

    def __init__(self) -> None:
        super().__init__()
        self.outlier_analyzer = OutlierAnalyzer()

    def analyze(
        self,
        df: pd.DataFrame,
    ) -> QualityReport:
        """
        Analyze a dataset and generate a quality report.
        """

        start = self.log_start("Quality Analysis")

        report = QualityReport()

        report.total_rows = len(df)
        report.total_columns = len(df.columns)

        # ---------------------------------------------------------
        # Missing Values
        # ---------------------------------------------------------

        report.missing_values = int(
            df.isna().sum().sum()
        )

        report.missing_value_summary = (
            self._analyze_missing_values(df)
        )

        # ---------------------------------------------------------
        # Duplicate Rows
        # ---------------------------------------------------------

        report.duplicate_rows = int(
            df.duplicated().sum()
        )

        report.duplicate_row_summary = (
            self._analyze_duplicate_rows(df)
        )

        # ---------------------------------------------------------
        # Duplicate Columns
        # ---------------------------------------------------------

        report.duplicate_columns = len(
            self._find_duplicate_columns(df)
        )

        report.duplicate_column_summary = (
            self._analyze_duplicate_columns(df)
        )

        # ---------------------------------------------------------
        # Data Types
        # ---------------------------------------------------------

        report.data_type_summary = (
            self._analyze_data_types(df)
        )

        # ---------------------------------------------------------
        # Outliers
        # ---------------------------------------------------------

        report.outlier_summary = (
            self.outlier_analyzer.analyze(df)
        )

        # ---------------------------------------------------------
        # Quality Score
        # ---------------------------------------------------------

        report.quality_score = round(
            self._calculate_quality_score(
                report,
            ),
            2,
        )

        report.quality_grade = (
            self._get_quality_grade(
                report.quality_score,
            )
        )

        self.log_finish(
            "Quality Analysis",
            start,
        )

        return report

    # ============================================================
    # Quality Score
    # ============================================================

    def _calculate_quality_score(
        self,
        report: QualityReport,
    ) -> float:
        """
        Calculate the overall quality score.
        """

        if report.total_rows == 0:
            return 100.0

        if report.total_columns == 0:
            return 100.0

        total_cells = (
            report.total_rows
            * report.total_columns
        )

        missing_ratio = (
            report.missing_values
            / total_cells
        )

        duplicate_row_ratio = (
            report.duplicate_rows
            / report.total_rows
        )

        duplicate_column_ratio = (
            report.duplicate_columns
            / report.total_columns
        )

        total_outliers = sum(
            item["count"]
            for item in report.outlier_summary.values()
        )

        numeric_columns = max(
            1,
            len(report.outlier_summary),
        )

        outlier_ratio = (
            total_outliers
            / (
                report.total_rows
                * numeric_columns
            )
        )

        missing_score = max(
            0,
            100
            - (missing_ratio * 100),
        )

        duplicate_row_score = max(
            0,
            100
            - (duplicate_row_ratio * 100),
        )

        duplicate_column_score = max(
            0,
            100
            - (duplicate_column_ratio * 100),
        )

        outlier_score = max(
            0,
            100
            - (outlier_ratio * 100),
        )

        final_score = (
            missing_score
            * MISSING_VALUE_WEIGHT
            + duplicate_row_score
            * DUPLICATE_ROW_WEIGHT
            + duplicate_column_score
            * DUPLICATE_COLUMN_WEIGHT
            + outlier_score
            * OUTLIER_WEIGHT
        )

        return final_score

    def _get_quality_grade(
        self,
        score: float,
    ) -> str:
        """
        Convert a score into a quality grade.
        """

        if score >= EXCELLENT_SCORE:
            return "Excellent"

        if score >= GOOD_SCORE:
            return "Good"

        if score >= FAIR_SCORE:
            return "Fair"

        return "Poor"

    # ============================================================
    # Missing Values
    # ============================================================

    def _analyze_missing_values(
        self,
        df: pd.DataFrame,
    ) -> dict[str, dict[str, float | int]]:

        summary = {}

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

    # ============================================================
    # Duplicate Rows
    # ============================================================

    def _analyze_duplicate_rows(
        self,
        df: pd.DataFrame,
    ) -> dict[str, float | int]:

        total_rows = len(df)

        duplicate_count = int(
            df.duplicated().sum()
        )

        percentage = (
            round(
                (duplicate_count / total_rows)
                * 100,
                2,
            )
            if total_rows > 0
            else 0.0
        )

        return {
            "count": duplicate_count,
            "percentage": percentage,
        }

    # ============================================================
    # Duplicate Columns
    # ============================================================

    def _find_duplicate_columns(
        self,
        df: pd.DataFrame,
    ) -> list[str]:

        duplicate_columns = []

        columns = list(df.columns)

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                if df[
                    columns[i]
                ].equals(
                    df[columns[j]]
                ):
                    duplicate_columns.append(
                        columns[j]
                    )

        return duplicate_columns

    def _analyze_duplicate_columns(
        self,
        df: pd.DataFrame,
    ) -> dict[str, list[str]]:

        summary = {}

        columns = list(df.columns)

        for i in range(len(columns)):

            duplicates = []

            for j in range(i + 1, len(columns)):
                if df[
                    columns[i]
                ].equals(
                    df[columns[j]]
                ):
                    duplicates.append(
                        columns[j]
                    )

            if duplicates:
                summary[
                    columns[i]
                ] = duplicates

        return summary

    # ============================================================
    # Data Types
    # ============================================================

    def _analyze_data_types(
        self,
        df: pd.DataFrame,
    ) -> dict[str, str]:

        summary = {}

        for column in df.columns:
            summary[column] = str(
                df[column].dtype
            )

        return summary