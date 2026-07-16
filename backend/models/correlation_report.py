from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CorrelationPair:
    """
    Represents a correlated pair of numeric features.
    """

    column_x: str
    column_y: str

    method: str

    coefficient: float


@dataclass(slots=True)
class CorrelationReport:
    """
    Stores the results of correlation analysis.
    """

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

    recommendations: list[str] = field(
        default_factory=list
    )

    highly_correlated_pairs: list[CorrelationPair] = field(
        default_factory=list
    )