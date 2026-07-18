"""
Enterprise Visualization Report Model.

Represents the complete output of the visualization engine.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any


# ==========================================================
# Chart Specification
# ==========================================================

@dataclass(slots=True)
class ChartSpec:
    """
    Represents a single generated visualization.
    """

    title: str

    chart_type: str

    x: str | None = None

    y: str | None = None

    description: str | None = None

    image_path: str | None = None

    interactive_path: str | None = None

    data: dict[str, Any] | list[dict[str, Any]] = field(
        default_factory=dict
    )


# ==========================================================
# Chart Category
# ==========================================================

@dataclass(slots=True)
class ChartCategory:
    """
    Logical grouping of charts.
    """

    title: str

    charts: list[ChartSpec] = field(
        default_factory=list
    )


# ==========================================================
# Visualization Summary
# ==========================================================

@dataclass(slots=True)
class VisualizationSummary:
    """
    Overall visualization statistics.
    """

    total_charts: int = 0

    total_categories: int = 0


# ==========================================================
# Visualization Report
# ==========================================================

@dataclass(slots=True)
class VisualizationReport:
    """
    Complete visualization report.
    """

    summary: VisualizationSummary = field(
        default_factory=VisualizationSummary
    )

    categories: list[ChartCategory] = field(
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