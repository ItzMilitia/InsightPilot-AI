from __future__ import annotations

import pandas as pd

from backend.core.base_engine import BaseEngine
from backend.models.profiling_report import (
    NumericProfile,
    ProfilingReport,
)


class ProfilingEngine(BaseEngine):
    """
    Generates statistical profiles for numeric columns.
    """

    def analyze(
        self,
        df: pd.DataFrame,
    ) -> ProfilingReport:

        start = self.log_start("Profiling Analysis")

        report = ProfilingReport()

        numeric_df = df.select_dtypes(
            include="number"
        )

        report.total_numeric_columns = len(
            numeric_df.columns
        )

        for column in numeric_df.columns:

            series = numeric_df[column]

            profile = self._profile_column(
                column,
                series,
            )

            report.profiles.append(profile)

        self.log_finish(
            "Profiling Analysis",
            start,
        )

        return report

    def _profile_column(
        self,
        column: str,
        series: pd.Series,
    ) -> NumericProfile:

        missing = int(series.isna().sum())

        cleaned = series.dropna()

        profile = NumericProfile(
            column_name=column,
            dtype=str(series.dtype),
        )

        profile.count = int(cleaned.count())

        profile.missing_count = missing

        total = len(series)

        profile.missing_percentage = (
            round(
                missing / total * 100,
                2,
            )
            if total > 0
            else 0.0
        )

        if cleaned.empty:
            return profile

        mode = cleaned.mode()

        profile.mean = float(cleaned.mean())

        profile.median = float(cleaned.median())

        profile.mode = (
            mode.iloc[0]
            if not mode.empty
            else None
        )

        profile.minimum = cleaned.min()

        profile.maximum = cleaned.max()

        profile.value_range = (
            profile.maximum
            - profile.minimum
        )

        profile.variance = float(
            cleaned.var()
        )

        profile.standard_deviation = float(
            cleaned.std()
        )

        profile.skewness = float(
            cleaned.skew()
        )

        profile.kurtosis = float(
            cleaned.kurt()
        )

        profile.q1 = float(
            cleaned.quantile(0.25)
        )

        profile.q2 = float(
            cleaned.quantile(0.50)
        )

        profile.q3 = float(
            cleaned.quantile(0.75)
        )

        profile.interquartile_range = (
            profile.q3 - profile.q1
        )

        return profile