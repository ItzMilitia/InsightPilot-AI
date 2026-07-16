from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DatetimeProfile:
    """
    Statistical profile for a datetime column.
    """

    column_name: str
    dtype: str

    count: int = 0

    missing_count: int = 0
    missing_percentage: float = 0.0

    minimum_date: str | None = None
    maximum_date: str | None = None

    date_range_days: int = 0

    unique_dates: int = 0

    most_frequent_date: str | None = None
    most_frequent_count: int = 0