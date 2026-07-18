"""
Enterprise Correlation Report Model.

Represents the complete output of the correlation engine.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any


# ==========================================================
# Correlation Pair
# ==========================================================

@dataclass(slots=True)
class CorrelationPair:
    """
    Represents a correlated pair of features.
    """

    column_x: str

    column_y: str

    method: str

    coefficient: float


# ==========================================================
# Correlation Summary
# ==========================================================

@dataclass(slots=True)
class CorrelationSummary:
    """
    Overall correlation statistics.
    """

    method: str = "pearson"

    threshold: float = 0.80

    total_numeric_columns: int = 0

    total_pairs: int = 0

    strong_positive_count: int = 0

    strong_negative_count: int = 0


# ==========================================================
# Correlation Visualization
# ==========================================================

@dataclass(slots=True)
class CorrelationVisualization:
    """
    Correlation visualization assets.
    """

    heatmap_path: str | None = None


# ==========================================================
# Correlation Report
# ==========================================================

@dataclass(slots=True)
class CorrelationReport:
    """
    Complete correlation analysis report.
    """

    summary: CorrelationSummary = field(
        default_factory=CorrelationSummary
    )

    matrix: dict[str, dict[str, float]] = field(
        default_factory=dict
    )

    strong_positive: list[CorrelationPair] = field(
        default_factory=list
    )

    strong_negative: list[CorrelationPair] = field(
        default_factory=list
    )

    highly_correlated_pairs: list[CorrelationPair] = field(
        default_factory=list
    )

    visualization: CorrelationVisualization = field(
        default_factory=CorrelationVisualization
    )

    recommendations: list[str] = field(
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