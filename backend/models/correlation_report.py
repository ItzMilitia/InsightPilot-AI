from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CorrelationPair:
    column_x: str
    column_y: str

    method: str

    coefficient: float


@dataclass(slots=True)
class CorrelationReport:

    method: str

    matrix: dict[str, dict[str, float]] = field(
        default_factory=dict
    )

    strong_positive: list[CorrelationPair] = field(
        default_factory=list
    )

    strong_negative: list[CorrelationPair] = field(
        default_factory=list
    )