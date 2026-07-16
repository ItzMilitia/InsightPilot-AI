from __future__ import annotations

from backend.core.base_engine import BaseEngine

from backend.models.analysis_report import AnalysisReport
from backend.models.insight_report import (
    Insight,
    InsightReport,
)


class InsightEngine(BaseEngine):
    """
    Generates human-readable insights from an AnalysisReport.

    This engine interprets analysis results and produces
    actionable insights without accessing the original dataset.
    """

    def analyze(
        self,
        analysis_report: AnalysisReport,
    ) -> InsightReport:

        start = self.log_start("Insight Generation")

        report = InsightReport()

        report.insights.extend(
            self._generate_quality_insights(
                analysis_report
            )
        )

        report.insights.extend(
            self._generate_missing_value_insights(
                analysis_report
            )
        )

        report.insights.extend(
            self._generate_profiling_insights(
                analysis_report
            )
        )

        report.insights.extend(
            self._generate_correlation_insights(
                analysis_report
            )
        )

        report.insights.extend(
            self._generate_visualization_insights(
                analysis_report
            )
        )

        self.log_finish(
            "Insight Generation",
            start,
        )

        return report

    # ============================================================
    # Quality Insights
    # ============================================================

    def _generate_quality_insights(
        self,
        report: AnalysisReport,
    ) -> list[Insight]:

        quality = report.quality

        return [
            Insight(
                category="Quality",
                severity="Info",
                title=f"Dataset Quality: {quality.quality_grade}",
                description=(
                    f"The dataset achieved a quality score of "
                    f"{quality.quality_score:.2f}."
                ),
                recommendation=(
                    "Review the quality report before "
                    "performing downstream analytics."
                ),
            )
        ]

    # ============================================================
    # Missing Value Insights
    # ============================================================

    def _generate_missing_value_insights(
        self,
        report: AnalysisReport,
    ) -> list[Insight]:

        insights: list[Insight] = []

        for column, values in (
            report.quality.missing_value_summary.items()
        ):

            insights.append(
                Insight(
                    category="Missing Values",
                    severity="Warning",
                    title=f"Missing values detected in '{column}'",
                    description=(
                        f"{values['percentage']}% of the values "
                        f"are missing."
                    ),
                    recommendation=(
                        "Consider imputing missing values "
                        "before model training."
                    ),
                )
            )

        return insights

    # ============================================================
    # Profiling Insights
    # ============================================================

    def _generate_profiling_insights(
        self,
        report: AnalysisReport,
    ) -> list[Insight]:

        insights: list[Insight] = []

        for profile in report.profiling.numeric_profiles:

            insights.append(
                Insight(
                    category="Profiling",
                    severity="Info",
                    title=f"Numeric Profile: {profile.column_name}",
                    description=(
                        f"Mean={profile.mean}, "
                        f"Median={profile.median}, "
                        f"Std Dev={profile.standard_deviation}"
                    ),
                    recommendation=(
                        "Review the distribution for "
                        "possible skewness or outliers."
                    ),
                )
            )

        return insights

    # ============================================================
    # Correlation Insights
    # ============================================================

    def _generate_correlation_insights(
        self,
        report: AnalysisReport,
    ) -> list[Insight]:

        insights: list[Insight] = []

        for pair in report.correlation.strong_positive:

            insights.append(
                Insight(
                    category="Correlation",
                    severity="Warning",
                    title="Strong Positive Correlation",
                    description=(
                        f"{pair.column_x} and "
                        f"{pair.column_y} have correlation "
                        f"{pair.coefficient}."
                    ),
                    recommendation=(
                        "Consider removing one feature "
                        "to reduce multicollinearity."
                    ),
                )
            )

        for pair in report.correlation.strong_negative:

            insights.append(
                Insight(
                    category="Correlation",
                    severity="Info",
                    title="Strong Negative Correlation",
                    description=(
                        f"{pair.column_x} and "
                        f"{pair.column_y} have correlation "
                        f"{pair.coefficient}."
                    ),
                    recommendation=(
                        "Verify whether both variables "
                        "are required for analysis."
                    ),
                )
            )

        return insights

    # ============================================================
    # Visualization Insights
    # ============================================================

    def _generate_visualization_insights(
        self,
        report: AnalysisReport,
    ) -> list[Insight]:

        chart_count = len(
            report.visualization.charts
        )

        return [
            Insight(
                category="Visualization",
                severity="Info",
                title="Visualization Summary",
                description=(
                    f"{chart_count} chart specifications "
                    "have been generated."
                ),
                recommendation=(
                    "Use the visualization module "
                    "to explore the dataset."
                ),
            )
        ]