from __future__ import annotations

import pandas as pd

from backend.core.base_engine import BaseEngine
from backend.models.visualization_report import (
    ChartCategory,
    ChartSpec,
    VisualizationReport,
)
from backend.config.settings import settings


class VisualizationEngine(BaseEngine):
    """
    Generates visualization specifications for the frontend.

    This engine prepares reusable chart specifications without
    depending on Streamlit, Matplotlib, Plotly, or Seaborn.
    """

    def analyze(
        self,
        df: pd.DataFrame,
    ) -> VisualizationReport:

        start = self.log_start("Visualization Analysis")

        report = VisualizationReport()

        categories: list[ChartCategory] = []

        # ---------------------------------------------------------
        # Data Quality
        # ---------------------------------------------------------

        quality_category = ChartCategory(
            title="Data Quality"
        )

        quality_category.charts.extend(
            self._generate_missing_chart(df)
        )

        if quality_category.charts:
            categories.append(quality_category)

        # ---------------------------------------------------------
        # Dataset Overview
        # ---------------------------------------------------------

        overview_category = ChartCategory(
            title="Dataset Overview"
        )

        overview_category.charts.extend(
            self._generate_dtype_chart(df)
        )

        if overview_category.charts:
            categories.append(overview_category)

        # ---------------------------------------------------------
        # Numeric Analysis
        # ---------------------------------------------------------

        numeric_category = ChartCategory(
            title="Numeric Analysis"
        )

        if settings.generate_histograms:
            numeric_category.charts.extend(
                self._generate_histograms(df)
            )

        if settings.generate_boxplots:
            numeric_category.charts.extend(
                self._generate_boxplots(df)
            )

        if numeric_category.charts:
            categories.append(numeric_category)

        # ---------------------------------------------------------
        # Correlation
        # ---------------------------------------------------------

        if settings.generate_heatmap:

            correlation_category = ChartCategory(
                title="Correlation"
            )

            correlation_category.charts.extend(
                self._generate_heatmap(df)
            )

            if correlation_category.charts:
                categories.append(
                    correlation_category
                )

        report.categories = categories

        report.summary.total_categories = len(
            categories
        )

        report.summary.total_charts = sum(
            len(category.charts)
            for category in categories
        )

        report.metadata = {
            "engine": "VisualizationEngine",
            "version": "8.2",
        }

        self.log_finish(
            "Visualization Analysis",
            start,
        )

        return report

    # ============================================================
    # Missing Values
    # ============================================================

    def _generate_missing_chart(
        self,
        df: pd.DataFrame,
    ) -> list[ChartSpec]:

        missing = (
            df.isna()
            .sum()
            .loc[lambda x: x > 0]
        )

        if missing.empty:
            return []

        return [
            ChartSpec(
                title="Missing Values",
                chart_type="bar",
                x="column",
                y="missing_count",
                data={
                    "column": missing.index.tolist(),
                    "missing_count": missing.tolist(),
                },
            )
        ]

    # ============================================================
    # Data Types
    # ============================================================

    def _generate_dtype_chart(
        self,
        df: pd.DataFrame,
    ) -> list[ChartSpec]:

        numeric = len(
            df.select_dtypes(include="number").columns
        )

        categorical = len(
            df.select_dtypes(
                include=["object", "category", "string"]
            ).columns
        )

        datetime = len(
            df.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns
        )

        return [
            ChartSpec(
                title="Data Types",
                chart_type="pie",
                data={
                    "Numeric": numeric,
                    "Categorical": categorical,
                    "Datetime": datetime,
                },
            )
        ]

    # ============================================================
    # Histograms
    # ============================================================

    def _generate_histograms(
        self,
        df: pd.DataFrame,
    ) -> list[ChartSpec]:

        charts: list[ChartSpec] = []

        numeric_df = df.select_dtypes(
            include="number"
        )

        for column in numeric_df.columns:

            charts.append(
                ChartSpec(
                    title=f"{column} Histogram",
                    chart_type="histogram",
                    x=column,
                    data=numeric_df[column]
                    .dropna()
                    .tolist(),
                )
            )

        return charts

    # ============================================================
    # Box Plots
    # ============================================================

    def _generate_boxplots(
        self,
        df: pd.DataFrame,
    ) -> list[ChartSpec]:

        charts: list[ChartSpec] = []

        numeric_df = df.select_dtypes(
            include="number"
        )

        for column in numeric_df.columns:

            charts.append(
                ChartSpec(
                    title=f"{column} Box Plot",
                    chart_type="boxplot",
                    y=column,
                    data=numeric_df[column]
                    .dropna()
                    .tolist(),
                )
            )

        return charts

    # ============================================================
    # Correlation Heatmap
    # ============================================================

    def _generate_heatmap(
        self,
        df: pd.DataFrame,
    ) -> list[ChartSpec]:

        numeric_df = df.select_dtypes(
            include="number"
        )

        if len(numeric_df.columns) < 2:
            return []

        matrix = (
            numeric_df
            .corr(method="pearson")
            .round(4)
            .to_dict()
        )

        return [
            ChartSpec(
                title="Correlation Heatmap",
                chart_type="heatmap",
                data=matrix,
            )
        ]