"""
Enterprise Report Comparison Service.

Compares two ReportContext instances and produces a
ReportComparison describing all detected differences.

Business logic belongs exclusively in this service.

Author
------
InsightPilot AI

Version
-------
v0.8.9
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from backend.models.comparison_summary import ComparisonSummary
from backend.models.report_comparison import ReportComparison
from backend.models.report_context import ReportContext

from backend.services.comparison_utils import (
    calculate_delta,
    compare_dictionary,
    compare_lists,
)


class ReportComparisonService:
    """
    Service responsible for comparing two reports.
    """

    def __init__(self) -> None:
        """
        Initialize the comparison service.
        """

        pass

    # ======================================================
    # Public API
    # ======================================================

    def compare(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> ReportComparison:
        """
        Compare two ReportContext instances.

        Parameters
        ----------
        baseline:
            Original report.

        comparison:
            Newly generated report.

        Returns
        -------
        ReportComparison
            Complete comparison object.
        """

        self._validate_context(baseline)
        self._validate_context(comparison)

        report = ReportComparison(
            baseline_report_id=baseline.metadata.report_id,
            comparison_report_id=comparison.metadata.report_id,
            baseline_version=baseline.metadata.version,
            comparison_version=comparison.metadata.version,
        )

        # ==================================================
        # KPI Summary
        # ==================================================

        report.quality_score_before = (
            baseline.quality.summary.score
        )

        report.quality_score_after = (
            comparison.quality.summary.score
        )

        report.quality_score_delta = calculate_delta(
            baseline.quality.summary.score,
            comparison.quality.summary.score,
        )

        report.grade_before = (
            baseline.quality.summary.grade
        )

        report.grade_after = (
            comparison.quality.summary.grade
        )

        report.missing_value_delta = int(
            calculate_delta(
                baseline.quality.missing.total_missing,
                comparison.quality.missing.total_missing,
            )
        )

        report.duplicate_row_delta = int(
            calculate_delta(
                baseline.quality.duplicates.duplicate_rows,
                comparison.quality.duplicates.duplicate_rows,
            )
        )

        report.duplicate_column_delta = int(
            calculate_delta(
                baseline.quality.duplicates.duplicate_columns,
                comparison.quality.duplicates.duplicate_columns,
            )
        )

        report.outlier_delta = int(
            calculate_delta(
                len(
                    baseline.quality.outliers.columns
                ),
                len(
                    comparison.quality.outliers.columns
                ),
            )
        )

        # ==================================================
        # Section Comparisons
        # ==================================================

        section_changes: dict[str, Any] = {}

        section_changes["quality"] = (
            self._compare_quality(
                baseline,
                comparison,
            )
        )

        section_changes["profiling"] = (
            self._compare_profiling(
                baseline,
                comparison,
            )
        )

        report.section_changes = section_changes

        section_changes["rules"] = self._compare_rules(
            baseline,
            comparison,
        )

        section_changes["insights"] = (
            self._compare_insights(
                baseline,
                comparison,
            )
        )

        section_changes["recommendations"] = (
            self._compare_recommendations(
                baseline,
                comparison,
            )
        )

        section_changes["dataset"] = (
            self._compare_dataset(
                baseline,
                comparison,
            )
        )

        section_changes["correlation"] = (
            self._compare_correlation(
                baseline,
                comparison,
            )
        )

        section_changes["visualization"] = (
            self._compare_visualization(
                baseline,
                comparison,
            )
        )

        section_changes["metadata"] = (
            self._compare_metadata(
                baseline,
                comparison,
            )
        )

        report.section_changes = section_changes

        report.summary = self._build_summary(
            report
        )

        return report

    # ======================================================
    # Validation
    # ======================================================

    @staticmethod
    def _validate_context(
        context: ReportContext,
    ) -> None:
        """
        Validate a report context.

        Parameters
        ----------
        context:
            Report context to validate.

        Raises
        ------
        ValueError
            If the supplied context is invalid.
        """

        if context is None:
            raise ValueError(
                "ReportContext cannot be None."
            )

        if context.metadata is None:
            raise ValueError(
                "Report metadata is missing."
            )

        if context.quality is None:
            raise ValueError(
                "QualityReport is missing."
            )

        if context.profiling is None:
            raise ValueError(
                "ProfilingReport is missing."
            )
        
        # ======================================================
    # Quality Comparison
    # ======================================================

    def _compare_quality(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare two QualityReport objects.
        """

        before = baseline.quality
        after = comparison.quality

        return {
            "summary": compare_dictionary(
                asdict(before.summary),
                asdict(after.summary),
            ),
            "missing": {
                "delta": calculate_delta(
                    before.missing.total_missing,
                    after.missing.total_missing,
                ),
                "columns": compare_dictionary(
                    before.missing.columns,
                    after.missing.columns,
                ),
            },
            "duplicates": {
                "row_delta": calculate_delta(
                    before.duplicates.duplicate_rows,
                    after.duplicates.duplicate_rows,
                ),
                "column_delta": calculate_delta(
                    before.duplicates.duplicate_columns,
                    after.duplicates.duplicate_columns,
                ),
            },
            "outliers": compare_dictionary(
                before.outliers.columns,
                after.outliers.columns,
            ),
            "recommendations": compare_lists(
                before.recommendations,
                after.recommendations,
            ),
        }

    # ======================================================
    # Profiling Comparison
    # ======================================================

    def _compare_profiling(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare two ProfilingReport objects.
        """

        before = baseline.profiling
        after = comparison.profiling

        return {
            "summary": compare_dictionary(
                asdict(before.summary),
                asdict(after.summary),
            ),
            "numeric_profiles": {
                "before": len(before.numeric_profiles),
                "after": len(after.numeric_profiles),
                "delta": calculate_delta(
                    len(before.numeric_profiles),
                    len(after.numeric_profiles),
                ),
            },
            "categorical_profiles": {
                "before": len(before.categorical_profiles),
                "after": len(after.categorical_profiles),
                "delta": calculate_delta(
                    len(before.categorical_profiles),
                    len(after.categorical_profiles),
                ),
            },
            "datetime_profiles": {
                "before": len(before.datetime_profiles),
                "after": len(after.datetime_profiles),
                "delta": calculate_delta(
                    len(before.datetime_profiles),
                    len(after.datetime_profiles),
                ),
            },
            "high_cardinality_columns": compare_lists(
                before.high_cardinality_columns,
                after.high_cardinality_columns,
            ),
            "memory": compare_dictionary(
                asdict(before.memory),
                asdict(after.memory),
            ),
        }

        # ======================================================
    # Rules Comparison
    # ======================================================

    def _compare_rules(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare RuleReport objects.
        """

        before = baseline.rules
        after = comparison.rules

        return {
            "overall_status": {
                "before": before.overall_status,
                "after": after.overall_status,
            },
            "total_rules": {
                "before": before.total_rules,
                "after": after.total_rules,
                "delta": calculate_delta(
                    before.total_rules,
                    after.total_rules,
                ),
            },
            "passed_rules": {
                "before": before.passed_rules,
                "after": after.passed_rules,
                "delta": calculate_delta(
                    before.passed_rules,
                    after.passed_rules,
                ),
            },
            "failed_rules": {
                "before": before.failed_rules,
                "after": after.failed_rules,
                "delta": calculate_delta(
                    before.failed_rules,
                    after.failed_rules,
                ),
            },
            "warning_rules": {
                "before": before.warning_rules,
                "after": after.warning_rules,
                "delta": calculate_delta(
                    before.warning_rules,
                    after.warning_rules,
                ),
            },
        }

    # ======================================================
    # Insight Comparison
    # ======================================================

    def _compare_insights(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare InsightReport objects.
        """

        before = baseline.insights
        after = comparison.insights

        return {
            "summary": compare_dictionary(
                asdict(before.summary),
                asdict(after.summary),
            ),
            "insights": compare_lists(
                before.insights,
                after.insights,
                key=lambda insight: insight.id,
            ),
        }

    # ======================================================
    # Recommendation Comparison
    # ======================================================

    def _compare_recommendations(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare RecommendationReport objects.
        """

        before = baseline.recommendations
        after = comparison.recommendations

        return {
            "summary": compare_dictionary(
                asdict(before.summary),
                asdict(after.summary),
            ),
            "recommendations": compare_lists(
                before.recommendations,
                after.recommendations,
                key=lambda recommendation: recommendation.id,
            ),
        }

    # ======================================================
    # Dataset Comparison
    # ======================================================

    def _compare_dataset(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare dataset metadata.
        """

        return compare_dictionary(
            asdict(baseline.dataset),
            asdict(comparison.dataset),
        )

    # ======================================================
    # Correlation Comparison
    # ======================================================

    def _compare_correlation(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare correlation reports.
        """

        return compare_dictionary(
            asdict(baseline.correlation),
            asdict(comparison.correlation),
        )

    # ======================================================
    # Visualization Comparison
    # ======================================================

    def _compare_visualization(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare visualization reports.
        """

        return compare_dictionary(
            asdict(baseline.visualization),
            asdict(comparison.visualization),
        )

    # ======================================================
    # Metadata Comparison
    # ======================================================

    def _compare_metadata(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> dict[str, Any]:
        """
        Compare report metadata.
        """

        before = baseline.metadata
        after = comparison.metadata

        return {
            "report_id": {
                "before": before.report_id,
                "after": after.report_id,
            },
            "version": {
                "before": before.version,
                "after": after.version,
            },
            "title": {
                "before": before.title,
                "after": after.title,
            },
            "report_type": {
                "before": before.report_type,
                "after": after.report_type,
            },
            "dataset_name": {
                "before": before.dataset_name,
                "after": after.dataset_name,
            },
            "execution_time": {
                "before": before.execution_time,
                "after": after.execution_time,
                "delta": calculate_delta(
                    before.execution_time,
                    after.execution_time,
                ),
            },
            "tags": compare_lists(
                before.tags,
                after.tags,
            ),
            "metadata": compare_dictionary(
                before.metadata,
                after.metadata,
            ),
        }
    
        # ======================================================
    # Summary Builder
    # ======================================================

    def _build_summary(
        self,
        report: ReportComparison,
    ) -> ComparisonSummary:
        """
        Build a human-readable comparison summary.
        """

        improvements = self._build_improvements(report)
        regressions = self._build_regressions(report)

        recommendations: list[str] = []

        if report.quality_score_delta > 0:
            recommendations.append(
                "Dataset quality has improved."
            )

        elif report.quality_score_delta < 0:
            recommendations.append(
                "Investigate quality regressions."
            )

        if report.missing_value_delta > 0:
            recommendations.append(
                "Missing values increased."
            )

        elif report.missing_value_delta < 0:
            recommendations.append(
                "Missing values decreased."
            )

        if report.duplicate_row_delta > 0:
            recommendations.append(
                "Duplicate rows increased."
            )

        elif report.duplicate_row_delta < 0:
            recommendations.append(
                "Duplicate rows decreased."
            )

        if report.outlier_delta > 0:
            recommendations.append(
                "More outlier columns detected."
            )

        elif report.outlier_delta < 0:
            recommendations.append(
                "Outlier count reduced."
            )

        executive_summary = (
            f"Quality Score "
            f"{report.quality_score_before:.2f}"
            f" → "
            f"{report.quality_score_after:.2f}"
            f" "
            f"({report.quality_score_delta:+.2f})"
        )

        return ComparisonSummary(
            executive_summary=executive_summary,
            improvements=improvements,
            regressions=regressions,
            recommendations=recommendations,
        )

    # ======================================================
    # Improvements
    # ======================================================

    def _build_improvements(
        self,
        report: ReportComparison,
    ) -> list[str]:
        """
        Build improvement list.
        """

        improvements: list[str] = []

        if report.quality_score_delta > 0:
            improvements.append(
                "Quality score increased."
            )

        if report.missing_value_delta < 0:
            improvements.append(
                "Missing values reduced."
            )

        if report.duplicate_row_delta < 0:
            improvements.append(
                "Duplicate rows reduced."
            )

        if report.duplicate_column_delta < 0:
            improvements.append(
                "Duplicate columns reduced."
            )

        if report.outlier_delta < 0:
            improvements.append(
                "Outlier count reduced."
            )

        return improvements

    # ======================================================
    # Regressions
    # ======================================================

    def _build_regressions(
        self,
        report: ReportComparison,
    ) -> list[str]:
        """
        Build regression list.
        """

        regressions: list[str] = []

        if report.quality_score_delta < 0:
            regressions.append(
                "Quality score decreased."
            )

        if report.missing_value_delta > 0:
            regressions.append(
                "Missing values increased."
            )

        if report.duplicate_row_delta > 0:
            regressions.append(
                "Duplicate rows increased."
            )

        if report.duplicate_column_delta > 0:
            regressions.append(
                "Duplicate columns increased."
            )

        if report.outlier_delta > 0:
            regressions.append(
                "Outlier count increased."
            )

        return regressions