"""
Anomaly Report Models

Defines the report models used by the
Anomaly Detection Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AnomalySummary:
    """
    High-level anomaly detection summary.
    """

    algorithm: str = "Not Executed"

    algorithm_version: str = ""

    anomaly_count: int = 0

    anomaly_percentage: float = 0.0

    severity: str = "None"

    confidence_score: float = 0.0

    execution_time: float = 0.0


@dataclass(slots=True)
class AnomalyReport:
    """
    Structured report returned by the
    Anomaly Detection Engine.
    """

    summary: AnomalySummary = field(
        default_factory=AnomalySummary
    )

    detected_rows: list[int] = field(
        default_factory=list
    )

    detected_columns: list[str] = field(
        default_factory=list
    )

    anomaly_scores: list[float] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )