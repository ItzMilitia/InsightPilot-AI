from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class QualityReport:
    """
    Stores the results of a data quality analysis.
    """

    # Overall score (calculated in Sprint 3.7)
    quality_score: float = 100.0

    # Dataset metadata
    total_rows: int = 0
    total_columns: int = 0

    # -----------------------------
    # Missing Values
    # -----------------------------
    missing_values: int = 0

    missing_value_summary: dict[str, dict[str, float | int]] = field(
        default_factory=dict
    )

    # -----------------------------
    # Duplicate Rows
    # -----------------------------
    duplicate_rows: int = 0

    duplicate_row_summary: dict[str, float | int] = field(
        default_factory=dict
    )

    # -----------------------------
    # Duplicate Columns
    # -----------------------------
    duplicate_columns: int = 0

    duplicate_column_summary: dict[str, list[str]] = field(
        default_factory=dict
    )

    # -----------------------------
    # Data Types
    # -----------------------------
    data_type_summary: dict[str, str] = field(
        default_factory=dict
    )

    # -----------------------------
    # Outliers (Sprint 3.6)
    # -----------------------------
    outlier_summary: dict[str, dict[str, float | int]] = field(
        default_factory=dict
    )

    # -----------------------------
    # Recommendations
    # -----------------------------
    recommendations: list[str] = field(
        default_factory=list
    )