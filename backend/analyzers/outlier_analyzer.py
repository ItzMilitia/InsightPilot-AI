from __future__ import annotations

import pandas as pd


class OutlierAnalyzer:
    """
    Detects outliers in numeric columns using the
    Interquartile Range (IQR) method.
    """

    def analyze(
        self,
        df: pd.DataFrame,
    ) -> dict[str, dict[str, float | int]]:
        """
        Analyze all numeric columns and return
        structured outlier statistics.
        """

        summary: dict[str, dict[str, float | int]] = {}

        if df.empty:
            return summary

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns

        total_rows = len(df)

        for column in numeric_columns:

            series = df[column].dropna()

            # Skip columns with insufficient data
            if len(series) < 4:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            outlier_mask = (
                (series < lower_bound)
                | (series > upper_bound)
            )

            outlier_count = int(outlier_mask.sum())

            if outlier_count == 0:
                continue

            summary[column] = {
                "count": outlier_count,
                "percentage": round(
                    (outlier_count / total_rows) * 100,
                    2,
                ),
                "lower_bound": round(
                    float(lower_bound),
                    2,
                ),
                "upper_bound": round(
                    float(upper_bound),
                    2,
                ),
            }

        return summary