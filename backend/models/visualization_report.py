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

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ChartSpec":
        """
        Deserialize ChartSpec.
        """

        return cls(
            title=data.get(
                "title",
                "",
            ),
            chart_type=data.get(
                "chart_type",
                "",
            ),
            x=data.get(
                "x",
            ),
            y=data.get(
                "y",
            ),
            description=data.get(
                "description",
            ),
            image_path=data.get(
                "image_path",
            ),
            interactive_path=data.get(
                "interactive_path",
            ),
            data=data.get(
                "data",
                {},
            ),
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

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ChartCategory":
        """
        Deserialize ChartCategory.
        """

        return cls(
            title=data.get(
                "title",
                "",
            ),
            charts=[
                ChartSpec.from_dict(chart)
                for chart in data.get(
                    "charts",
                    [],
                )
            ],
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

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "VisualizationSummary":
        """
        Deserialize VisualizationSummary.
        """

        return cls(**data)


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
    
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "VisualizationReport":
        """
        Deserialize VisualizationReport.
        """

        return cls(
            summary=VisualizationSummary.from_dict(
                data.get(
                    "summary",
                    {},
                )
            ),
            categories=[
                ChartCategory.from_dict(category)
                for category in data.get(
                    "categories",
                    [],
                )
            ],
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )