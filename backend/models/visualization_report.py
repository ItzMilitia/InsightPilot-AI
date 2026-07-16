from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ChartSpec:
    title: str

    chart_type: str

    x: str | None = None

    y: str | None = None

    data: dict | list = field(
        default_factory=dict
    )


@dataclass(slots=True)
class VisualizationReport:

    charts: list[ChartSpec] = field(
        default_factory=list
    )