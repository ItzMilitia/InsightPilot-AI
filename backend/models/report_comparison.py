"""
Enterprise Report Comparison Model.

Represents the machine-readable comparison between two generated
InsightPilot AI reports.

The model stores only comparison results and contains no business
logic. Comparison calculations are performed by the
ReportComparisonService.

Author:
    InsightPilot AI

Version:
    v0.8.9
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import UTC
from datetime import datetime
from typing import Any

from backend.models.comparison_summary import ComparisonSummary


@dataclass(slots=True)
class ReportComparison:
    """
    Represents the comparison between two ReportContext
    instances.

    The model stores comparison results for each report section
    (quality, profiling, correlation, rules, insights,
    recommendations, etc.) and is designed to scale as new
    engines are added to InsightPilot AI.

    It is designed to support:

    - Human-readable summaries
    - JSON serialization
    - Registry persistence
    - Future database storage
    """

    # ------------------------------------------------------
    # Report Identity
    # ------------------------------------------------------

    baseline_report_id: str

    comparison_report_id: str

    baseline_version: str

    comparison_version: str

    # ------------------------------------------------------
    # Overall Quality
    # ------------------------------------------------------

    quality_score_before: float = 0.0

    quality_score_after: float = 0.0

    quality_score_delta: float = 0.0

    grade_before: str = ""

    grade_after: str = ""

    # ------------------------------------------------------
    # Quality Metrics
    # ------------------------------------------------------

    missing_value_delta: int = 0

    duplicate_row_delta: int = 0

    duplicate_column_delta: int = 0

    outlier_delta: int = 0

    # ------------------------------------------------------
    # Section Changes
    # ------------------------------------------------------

    section_changes: dict[str, dict[str, Any]] = field(
        default_factory=dict
    )

    # ------------------------------------------------------
    # Findings
    # ------------------------------------------------------

    improvements: list[str] = field(
        default_factory=list
    )

    regressions: list[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    summary: ComparisonSummary = field(
        default_factory=ComparisonSummary
    )

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    generated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ======================================================
    # Convenience Properties
    # ======================================================

    @property
    def has_improvements(self) -> bool:
        """
        Returns True when improvements were detected.
        """
        return bool(self.improvements)

    @property
    def has_regressions(self) -> bool:
        """
        Returns True when regressions were detected.
        """
        return bool(self.regressions)

    @property
    def has_grade_change(self) -> bool:
        """
        Returns True if the report grade changed.
        """
        return self.grade_before != self.grade_after

    @property
    def has_quality_change(self) -> bool:
        """
        Returns True if the quality score changed.
        """
        return self.quality_score_delta != 0.0

    @property
    def is_identical(self) -> bool:
        """
        Returns True if no meaningful differences exist.
        """
        return (
            not self.has_quality_change
            and not self.has_grade_change
            and not self.section_changes
            and not self.improvements
            and not self.regressions
        )

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Convert this comparison into a serializable dictionary.

        Returns
        -------
        dict[str, Any]
            Serialized representation.
        """
        data = asdict(self)

        data["generated_at"] = self.generated_at.isoformat()

        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ReportComparison":
        """
        Create a ReportComparison from serialized data.

        Parameters
        ----------
        data:
            Serialized dictionary.

        Returns
        -------
        ReportComparison
        """
        payload = dict(data)

        payload["summary"] = ComparisonSummary.from_dict(
            payload.get("summary", {})
        )

        payload["generated_at"] = datetime.fromisoformat(
            payload["generated_at"]
        )

        return cls(**payload)

    # ======================================================
    # Utility Methods
    # ======================================================

    def copy(self) -> "ReportComparison":
        """
        Create a deep copy of this comparison.

        Returns
        -------
        ReportComparison
        """
        return ReportComparison.from_dict(
            self.to_dict()
        )