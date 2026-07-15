from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class NumericProfile:
    """
    Statistical profile for a single numeric column.
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


@dataclass(slots=True)
class ProfilingReport:
    """
    Complete numeric profiling report.
    """

    total_numeric_columns: int = 0

    profiles: list[NumericProfile] = field(
        default_factory=list
    )