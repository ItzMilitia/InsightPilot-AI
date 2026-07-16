from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Insight:
    """
    Represents a single AI-generated insight.
    """

    category: str
    severity: str
    title: str
    description: str
    recommendation: str


@dataclass(slots=True)
class InsightReport:
    """
    Collection of insights generated from AnalysisReport.
    """

    insights: list[Insight] = field(
        default_factory=list
    )