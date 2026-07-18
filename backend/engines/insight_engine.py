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

        report.summary.total_insights = len(
            report.insights
        )

        report.summary.critical = sum(
            insight.severity.lower() == "critical"
            for insight in report.insights
        )

        report.summary.warning = sum(
            insight.severity.lower() == "warning"
            for insight in report.insights
        )

        report.summary.informational = sum(
            insight.severity.lower() == "info"
            or insight.severity.lower() == "informational"
            for insight in report.insights
        )

        report.metadata = {
            "engine": "InsightEngine",
            "version": "8.2",
        }

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
        summary = quality.summary

        return [
            Insight(
                id="quality_overview",
                title="Dataset Quality Overview",
                category="Quality",
                severity="Info",
                confidence=1.0,
                description=(
                    f"The dataset achieved an overall quality score of "
                    f"{summary.score:.2f} "
                    f"with grade '{summary.grade}'."
                ),
                business_impact=(
                    "Higher quality datasets generally produce more "
                    "reliable analytics and machine learning models."
                ),
                recommendation=(
                    "Review the Quality Report and resolve critical "
                    "data quality issues before downstream analysis."
                ),
                source_engine="QualityEngine",
                metadata={
                    "score": summary.score,
                    "grade": summary.grade,
                    "rows": summary.total_rows,
                    "columns": summary.total_columns,
                },
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

        missing_report = report.quality.missing

        for column_name, stats in missing_report.columns.items():

            percentage = float(stats.get("percentage", 0))
            count = int(stats.get("count", 0))

            if count == 0:
                continue

            if percentage >= 30:
                severity = "Critical"
            elif percentage >= 10:
                severity = "Warning"
            else:
                severity = "Info"

            insights.append(
                Insight(
                    id=f"missing_{column_name}",
                    title=f"Missing Values in '{column_name}'",
                    category="Missing Values",
                    severity=severity,
                    confidence=1.0,
                    description=(
                        f"Column '{column_name}' contains "
                        f"{count} missing values "
                        f"({percentage:.2f}% of the dataset)."
                    ),
                    business_impact=(
                        "Missing values may reduce model accuracy, "
                        "bias statistical analysis, and affect data quality."
                    ),
                    recommendation=(
                        "Consider imputing missing values, removing "
                        "affected rows, or investigating the source "
                        "of missing data."
                    ),
                    affected_columns=[column_name],
                    source_engine="QualityEngine",
                    metadata={
                        "missing_count": count,
                        "missing_percentage": percentage,
                    },
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
                    id=f"profile_{profile.column_name}",
                    title=f"Numeric Profile: {profile.column_name}",
                    category="Profiling",
                    severity="Info",
                    confidence=1.0,
                    description=(
                        f"Column '{profile.column_name}' has "
                        f"mean={profile.mean:.4f}, "
                        f"median={profile.median:.4f}, "
                        f"standard deviation={profile.standard_deviation:.4f}."
                    ),
                    business_impact=(
                        "Understanding feature distributions helps "
                        "identify skewness, anomalies, and potential "
                        "feature engineering opportunities."
                    ),
                    recommendation=(
                        "Review this column for skewness, outliers, "
                        "or normalization before model training."
                    ),
                    affected_columns=[profile.column_name],
                    source_engine="ProfilingEngine",
                    metadata={
                        "mean": profile.mean,
                        "median": profile.median,
                        "std_dev": profile.standard_deviation,
                        "minimum": profile.minimum,
                        "maximum": profile.maximum,
                    },
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

        chart_count = sum(
            len(category.charts)
            for category in report.visualization.categories
        )

        return [
            Insight(
                id="visualization_summary",
                title="Visualization Summary",
                category="Visualization",
                severity="Info",
                confidence=1.0,
                description=(
                    f"{chart_count} chart specifications have been "
                    "generated for exploratory data analysis."
                ),
                business_impact=(
                    "Visual exploration helps identify trends, "
                    "relationships, anomalies, and potential "
                    "data quality issues."
                ),
                recommendation=(
                    "Review the generated visualizations before "
                    "performing detailed statistical analysis "
                    "or machine learning."
                ),
                source_engine="VisualizationEngine",
                metadata={
                    "chart_count": chart_count,
                    "category_count": len(
                        report.visualization.categories
                    ),
                },
            )
        ]