"""
Comparison Summary Model.

This module defines the human-readable summary generated after comparing
two report versions. The model is intentionally data-only and contains
no business logic, following the architectural principles of
InsightPilot AI.

Author:
    InsightPilot AI

Version:
    v0.8.9
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ComparisonSummary:
    """
    Human-readable summary of a report comparison.

    This model stores presentation-ready comparison results that can be
    rendered by HTML, PDF, JSON, or future reporting engines.

    Attributes
    ----------
    executive_summary:
        High-level summary describing the overall comparison.

    improvements:
        List of detected improvements.

    regressions:
        List of detected regressions.

    recommendations:
        Recommended actions based on the comparison.
    """

    executive_summary: str = ""

    improvements: list[str] = field(default_factory=list)

    regressions: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the model into a serializable dictionary.

        Returns
        -------
        dict[str, Any]
            Dictionary representation of this summary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComparisonSummary":
        """
        Create a ComparisonSummary from a dictionary.

        Parameters
        ----------
        data:
            Serialized dictionary.

        Returns
        -------
        ComparisonSummary
            Deserialized ComparisonSummary instance.
        """
        return cls(
            executive_summary=data.get("executive_summary", ""),
            improvements=list(data.get("improvements", [])),
            regressions=list(data.get("regressions", [])),
            recommendations=list(data.get("recommendations", [])),
        )

    def copy(self) -> "ComparisonSummary":
        """
        Create a deep copy of this summary.

        Returns
        -------
        ComparisonSummary
            Independent copy of the current object.
        """
        return ComparisonSummary.from_dict(self.to_dict())

    def __len__(self) -> int:
        """
        Return the total number of comparison findings.

        Returns
        -------
        int
            Total number of improvements and regressions.
        """
        return len(self.improvements) + len(self.regressions)

    @property
    def has_improvements(self) -> bool:
        """
        Determine whether improvements were detected.

        Returns
        -------
        bool
            True if at least one improvement exists.
        """
        return bool(self.improvements)

    @property
    def has_regressions(self) -> bool:
        """
        Determine whether regressions were detected.

        Returns
        -------
        bool
            True if at least one regression exists.
        """
        return bool(self.regressions)

    @property
    def is_empty(self) -> bool:
        """
        Determine whether the summary contains any findings.

        Returns
        -------
        bool
            True if there are no improvements, regressions,
            or recommendations.
        """
        return not (
            self.improvements
            or self.regressions
            or self.recommendations
        )