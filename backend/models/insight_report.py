"""
Enterprise Insight Report Model.

Represents AI-generated insights produced by the Insight Engine.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any


# ==========================================================
# Insight
# ==========================================================

@dataclass(slots=True)
class Insight:
    """
    Represents a single AI-generated insight.
    """

    id: str

    title: str

    category: str

    severity: str

    confidence: float = 1.0

    description: str = ""

    business_impact: str | None = None

    recommendation: str | None = None

    affected_columns: list[str] = field(
        default_factory=list
    )

    source_engine: str = "InsightEngine"

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


# ==========================================================
# Insight Summary
# ==========================================================

@dataclass(slots=True)
class InsightSummary:
    """
    Summary statistics for generated insights.
    """

    total_insights: int = 0

    critical: int = 0

    warning: int = 0

    informational: int = 0


# ==========================================================
# Insight Report
# ==========================================================

@dataclass(slots=True)
class InsightReport:
    """
    Collection of AI-generated insights.
    """

    summary: InsightSummary = field(
        default_factory=InsightSummary
    )

    insights: list[Insight] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert report into a serializable dictionary.
        """

        return asdict(self)