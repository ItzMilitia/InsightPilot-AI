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

        self.log_finish(
            "Quality Analysis",
            start,
        )

        return report

    def _analyze_missing_values(
        self,
        df: pd.DataFrame,
    ) -> dict[str, dict[str, float | int]]:
        """
        Generate per-column missing value statistics.
        """

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