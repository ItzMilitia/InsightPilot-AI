from __future__ import annotations

import pandas as pd

from backend.core.base_engine import BaseEngine
from backend.models.categorical_profile import CategoricalProfile
from backend.models.datetime_profile import DatetimeProfile
from backend.models.profiling_report import (
    NumericProfile,
    ProfilingReport,
)


class ProfilingEngine(BaseEngine):
    """
    Generates statistical profiles for numeric and categorical columns.
    """

    def analyze(
        self,
        df: pd.DataFrame,
    ) -> ProfilingReport:

        start = self.log_start("Profiling Analysis")

        report = ProfilingReport()

        # ---------------------------------------------------------
        # Numeric Columns
        # ---------------------------------------------------------

        numeric_df = df.select_dtypes(include="number")

        report.total_numeric_columns = len(
            numeric_df.columns
        )

        for column in numeric_df.columns:

            profile = self._profile_numeric_column(
                column,
                numeric_df[column],
            )

            report.numeric_profiles.append(profile)

        # ---------------------------------------------------------
        # Categorical Columns
        # ---------------------------------------------------------

        categorical_df = df.select_dtypes(
            include=["object", "category", "string"]
        )

        for column in categorical_df.columns:

            profile = self._profile_categorical_column(
                column,
                categorical_df[column],
            )

            report.categorical_profiles.append(profile)

        self.log_finish(
            "Profiling Analysis",
            start,
        )

        return report

    # ============================================================
    # Numeric Profiling
    # ============================================================

    def _profile_numeric_column(
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
            round(missing / total * 100, 2)
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
            profile.maximum - profile.minimum
        )

        profile.variance = float(cleaned.var())
        profile.standard_deviation = float(cleaned.std())

        profile.skewness = float(cleaned.skew())
        profile.kurtosis = float(cleaned.kurt())

        profile.q1 = float(cleaned.quantile(0.25))
        profile.q2 = float(cleaned.quantile(0.50))
        profile.q3 = float(cleaned.quantile(0.75))

        profile.interquartile_range = (
            profile.q3 - profile.q1
        )

        return profile

    # ============================================================
    # Categorical Profiling
    # ============================================================

    def _profile_categorical_column(
        self,
        column: str,
        series: pd.Series,
    ) -> CategoricalProfile:

        profile = CategoricalProfile(
            column_name=column,
            dtype=str(series.dtype),
        )

        total = len(series)

        profile.count = int(series.count())

        profile.missing_count = int(series.isna().sum())

        profile.missing_percentage = (
            round(profile.missing_count / total * 100, 2)
            if total > 0
            else 0.0
        )

        cleaned = series.dropna().astype(str)

        if cleaned.empty:
            return profile

        profile.empty_string_count = int(
            (cleaned == "").sum()
        )

        profile.whitespace_count = int(
            (cleaned.str.strip() == "").sum()
        )

        profile.unique_values = int(
            cleaned.nunique()
        )

        profile.distinct_percentage = (
            round(
                profile.unique_values
                / len(cleaned)
                * 100,
                2,
            )
            if len(cleaned) > 0
            else 0.0
        )

        frequencies = cleaned.value_counts()

        if not frequencies.empty:

            profile.most_frequent_value = frequencies.index[0]
            profile.most_frequent_count = int(
                frequencies.iloc[0]
            )

            profile.most_frequent_percentage = round(
                frequencies.iloc[0]
                / len(cleaned)
                * 100,
                2,
            )

            profile.least_frequent_value = frequencies.index[-1]
            profile.least_frequent_count = int(
                frequencies.iloc[-1]
            )

        lengths = cleaned.str.len()

        profile.average_length = round(
            float(lengths.mean()),
            2,
        )

        profile.minimum_length = int(lengths.min())
        profile.maximum_length = int(lengths.max())

        return profile
    
    datetime_df = df.select_dtypes(
        include=["datetime", "datetimetz"]
    )

    for column in datetime_df.columns:
        profile = self._profile_datetime_column(
            column,
            datetime_df[column],
        )

        report.datetime_profiles.append(profile)

    def _profile_datetime_column(
        self,
        column: str,
        series: pd.Series,
    ) -> DatetimeProfile:

        profile = DatetimeProfile(
            column_name=column,
            dtype=str(series.dtype),
        )

        total = len(series)

        profile.count = int(series.count())

        profile.missing_count = int(series.isna().sum())

        profile.missing_percentage = (
            round(profile.missing_count / total * 100, 2)
            if total > 0
            else 0.0
        )

        cleaned = series.dropna()

        if cleaned.empty:
            return profile

        profile.minimum_date = str(cleaned.min())
        profile.maximum_date = str(cleaned.max())

        profile.date_range_days = (
            (cleaned.max() - cleaned.min()).days
        )

        profile.unique_dates = int(cleaned.nunique())

        frequencies = cleaned.value_counts()

        if not frequencies.empty:
            profile.most_frequent_date = str(frequencies.index[0])
            profile.most_frequent_count = int(frequencies.iloc[0])

        return profile