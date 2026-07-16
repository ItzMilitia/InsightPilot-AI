from __future__ import annotations

import pandas as pd

from backend.core.base_engine import BaseEngine
from backend.config.settings import settings
from backend.models.correlation_report import (
    CorrelationPair,
    CorrelationReport,
)
from backend.config import settings


class CorrelationEngine(BaseEngine):
    """
    Performs correlation analysis on numeric columns.
    """

    SUPPORTED_METHODS = {
        "pearson",
        "spearman",
        "kendall",
    }

    def analyze(
        self,
        df: pd.DataFrame,
        method: str = "pearson",
        threshold: float | None = None,
    ) -> CorrelationReport:
        """
        Analyze correlations between numeric columns.
        """

        start = self.log_start("Correlation Analysis")

        self._validate_method(method)

        report = CorrelationReport(method=method)

        numeric_df = df.select_dtypes(include="number")

        if threshold is None:
            threshold = settings.correlation_threshold

        if method is None:
            method = settings.default_correlation_method

        if numeric_df.shape[1] < 2:
            self.log_finish(
                "Correlation Analysis",
                start,
            )
            return report

        correlation_matrix = numeric_df.corr(method=method)

        report.matrix = correlation_matrix.round(4).to_dict()

        (
            report.strong_positive,
            report.strong_negative,
        ) = self._find_correlated_pairs(
            correlation_matrix,
            method,
            threshold,
        )

        report.recommendations = (
            self._generate_recommendations(
                report,
            )
        )

        self.log_finish(
            "Correlation Analysis",
            start,
        )

        return report

    # ============================================================
    # Validation
    # ============================================================

    def _validate_method(
        self,
        method: str,
    ) -> None:

        method = method.lower()

        if method not in self.SUPPORTED_METHODS:
            raise ValueError(
                f"Unsupported correlation method: '{method}'. "
                f"Supported methods: "
                f"{sorted(self.SUPPORTED_METHODS)}"
            )

    # ============================================================
    # Correlation Pair Detection
    # ============================================================

    def _find_correlated_pairs(
        self,
        matrix: pd.DataFrame,
        method: str,
        threshold: float,
    ) -> tuple[
        list[CorrelationPair],
        list[CorrelationPair],
    ]:

        positive: list[CorrelationPair] = []
        negative: list[CorrelationPair] = []

        columns = list(matrix.columns)

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                value = float(
                    matrix.iloc[i, j]
                )

                pair = CorrelationPair(
                    column_x=columns[i],
                    column_y=columns[j],
                    method=method,
                    coefficient=round(value, 4),
                )

                if value >= threshold:
                    positive.append(pair)

                elif value <= -threshold:
                    negative.append(pair)

        return positive, negative

    # ============================================================
    # Recommendations
    # ============================================================

    def _generate_recommendations(
        self,
        report: CorrelationReport,
    ) -> list[str]:

        recommendations: list[str] = []

        for pair in report.strong_positive:

            recommendations.append(
                f"'{pair.column_x}' and "
                f"'{pair.column_y}' have a strong "
                f"positive correlation "
                f"({pair.coefficient}). "
                f"Consider removing one of them "
                f"to reduce multicollinearity."
            )

        for pair in report.strong_negative:

            recommendations.append(
                f"'{pair.column_x}' and "
                f"'{pair.column_y}' have a strong "
                f"negative correlation "
                f"({pair.coefficient}). "
                f"Review whether both features "
                f"are required."
            )

        if not recommendations:
            recommendations.append(
                "No strong correlations were detected."
            )

        return recommendations