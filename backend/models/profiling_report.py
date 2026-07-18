"""
Enterprise Profiling Report Model.

Represents the complete output of the profiling engine.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from backend.models.categorical_profile import CategoricalProfile
from backend.models.datetime_profile import DatetimeProfile


# ==========================================================
# Numeric Profile
# ==========================================================

@dataclass(slots=True)
class NumericProfile:
    """
    Statistical profile for a numeric column.
    """

    column_name: str

    dtype: str

    count: int = 0

    missing_count: int = 0

    missing_percentage: float = 0.0

    mean: float | None = None

    median: float | None = None

    mode: float | int | None = None

    minimum: float | int | None = None

    maximum: float | int | None = None

    value_range: float | int | None = None

    variance: float | None = None

    standard_deviation: float | None = None

    skewness: float | None = None

    kurtosis: float | None = None

    q1: float | None = None

    q2: float | None = None

    q3: float | None = None

    interquartile_range: float | None = None


# ==========================================================
# Profiling Summary
# ==========================================================

@dataclass(slots=True)
class ProfilingSummary:
    """
    Overall profiling statistics.
    """

    total_columns: int = 0

    numeric_columns: int = 0

    categorical_columns: int = 0

    datetime_columns: int = 0

    boolean_columns: int = 0

    text_columns: int = 0


# ==========================================================
# Memory Profile
# ==========================================================

@dataclass(slots=True)
class MemoryProfile:
    """
    Dataset memory usage.
    """

    total_memory: str | None = None

    average_column_memory: str | None = None


# ==========================================================
# Profiling Report
# ==========================================================

@dataclass(slots=True)
class ProfilingReport:
    """
    Complete dataset profiling report.
    """

    summary: ProfilingSummary = field(
        default_factory=ProfilingSummary
    )

    numeric_profiles: list[NumericProfile] = field(
        default_factory=list
    )

    categorical_profiles: list[CategoricalProfile] = field(
        default_factory=list
    )

    datetime_profiles: list[DatetimeProfile] = field(
        default_factory=list
    )

    high_cardinality_columns: list[str] = field(
        default_factory=list
    )

    memory: MemoryProfile = field(
        default_factory=MemoryProfile
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert report into a serializable dictionary.
        """

        return asdict(self)