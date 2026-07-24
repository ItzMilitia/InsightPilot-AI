"""
Enterprise Quality Report Model.

Represents the complete output of the data quality engine.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any


# ==========================================================
# Overall Quality Summary
# ==========================================================

@dataclass(slots=True)
class QualitySummary:
    """
    Overall dataset quality metrics.
    """

    score: float = 100.0

    grade: str = "Excellent"

    total_rows: int = 0

    total_columns: int = 0

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "QualitySummary":

        return cls(**data)


# ==========================================================
# Missing Values
# ==========================================================

@dataclass(slots=True)
class MissingValueReport:
    """
    Missing value statistics.
    """

    total_missing: int = 0

    columns: dict[str, dict[str, float | int]] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "MissingValueReport":

        return cls(
            total_missing=data.get(
                "total_missing",
                0,
            ),
            columns=dict(
                data.get(
                    "columns",
                    {},
                )
            ),
        )


# ==========================================================
# Duplicate Information
# ==========================================================

@dataclass(slots=True)
class DuplicateReport:
    """
    Duplicate row and column information.
    """

    duplicate_rows: int = 0

    duplicate_columns: int = 0

    row_summary: dict[str, float | int] = field(
        default_factory=dict
    )

    column_summary: dict[str, list[str]] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "DuplicateReport":

        return cls(
            duplicate_rows=data.get(
                "duplicate_rows",
                0,
            ),
            duplicate_columns=data.get(
                "duplicate_columns",
                0,
            ),
            row_summary=dict(
                data.get(
                    "row_summary",
                    {},
                )
            ),
            column_summary=dict(
                data.get(
                    "column_summary",
                    {},
                )
            ),
        )


# ==========================================================
# Data Types
# ==========================================================

@dataclass(slots=True)
class DataTypeReport:
    """
    Data type consistency summary.
    """

    summary: dict[str, str] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "DataTypeReport":

        return cls(
            summary=dict(
                data.get(
                    "summary",
                    {},
                )
            ),
        )


# ==========================================================
# Outlier Information
# ==========================================================

@dataclass(slots=True)
class OutlierReport:
    """
    Outlier detection summary.
    """

    columns: dict[str, dict[str, float | int]] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "OutlierReport":

        return cls(
            columns=dict(
                data.get(
                    "columns",
                    {},
                )
            ),
        )


# ==========================================================
# Quality Report
# ==========================================================

@dataclass(slots=True)
class QualityReport:
    """
    Complete data quality report.
    """

    summary: QualitySummary = field(
        default_factory=QualitySummary
    )

    missing: MissingValueReport = field(
        default_factory=MissingValueReport
    )

    duplicates: DuplicateReport = field(
        default_factory=DuplicateReport
    )

    data_types: DataTypeReport = field(
        default_factory=DataTypeReport
    )

    outliers: OutlierReport = field(
        default_factory=OutlierReport
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
    
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "QualityReport":

        return cls(
            summary=QualitySummary.from_dict(
                data.get(
                    "summary",
                    {},
                )
            ),
            missing=MissingValueReport.from_dict(
                data.get(
                    "missing",
                    {},
                )
            ),
            duplicates=DuplicateReport.from_dict(
                data.get(
                    "duplicates",
                    {},
                )
            ),
            data_types=DataTypeReport.from_dict(
                data.get(
                    "data_types",
                    {},
                )
            ),
            outliers=OutlierReport.from_dict(
                data.get(
                    "outliers",
                    {},
                )
            ),
            recommendations=list(
                data.get(
                    "recommendations",
                    [],
                )
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )