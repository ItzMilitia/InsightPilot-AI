from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class QualityReport:
    """
    Stores the results of a data quality analysis.
    """

    quality_score: float = 100.0

    total_rows: int = 0
    total_columns: int = 0

    missing_values: int = 0

    missing_value_summary: dict[str, dict[str, float | int]] = field(
        default_factory=dict
    )

    duplicate_rows: int = 0

    duplicate_row_summary: dict[str, float | int] = field(
        default_factory=dict
    )

    duplicate_columns: int = 0

    duplicate_column_summary: dict[str, list[str]] = field(
        default_factory=dict
    )

    data_type_summary: dict[str, str] = field(
        default_factory=dict
    )

    recommendations: list[str] = field(default_factory=list)