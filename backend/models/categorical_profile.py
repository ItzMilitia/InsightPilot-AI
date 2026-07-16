from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CategoricalProfile:
    """
    Statistical profile for a single categorical/text column.
    """

    column_name: str
    dtype: str

    count: int = 0
    missing_count: int = 0
    missing_percentage: float = 0.0

    empty_string_count: int = 0
    whitespace_count: int = 0

    unique_values: int = 0
    distinct_percentage: float = 0.0

    most_frequent_value: str | None = None
    most_frequent_count: int = 0
    most_frequent_percentage: float = 0.0

    least_frequent_value: str | None = None
    least_frequent_count: int = 0

    average_length: float = 0.0
    minimum_length: int = 0
    maximum_length: int = 0