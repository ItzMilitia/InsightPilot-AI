"""
Enterprise Dataset Report Model.

Represents dataset metadata and structural information
used throughout the InsightPilot AI reporting pipeline.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any


# ==========================================================
# File Information
# ==========================================================

@dataclass(slots=True)
class DatasetFileInfo:
    """
    Physical dataset information.
    """

    name: str = ""

    path: str | None = None

    file_format: str = ""

    file_size: str | None = None

    memory_usage: str | None = None

    encoding: str | None = None

    checksum: str | None = None

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "DatasetFileInfo":

        return cls(**data)


# ==========================================================
# Dataset Structure
# ==========================================================

@dataclass(slots=True)
class DatasetStructure:
    """
    Dataset dimensions.
    """

    total_rows: int = 0

    total_columns: int = 0

    total_cells: int = 0

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "DatasetStructure":

        return cls(**data)


# ==========================================================
# Column Type Summary
# ==========================================================

@dataclass(slots=True)
class ColumnTypeSummary:
    """
    Counts of detected column types.
    """

    numeric: int = 0

    categorical: int = 0

    datetime: int = 0

    boolean: int = 0

    text: int = 0

    other: int = 0

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "ColumnTypeSummary":

        return cls(**data)


# ==========================================================
# Dataset Preview
# ==========================================================

@dataclass(slots=True)
class DatasetPreview:
    """
    Preview rows displayed in reports.
    """

    rows: list[dict[str, Any]] = field(
        default_factory=list
    )

    max_rows: int = 5

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "DatasetPreview":

        return cls(
            rows=list(
                data.get(
                    "rows",
                    [],
                )
            ),
            max_rows=data.get(
                "max_rows",
                5,
            ),
        )


# ==========================================================
# Dataset Report
# ==========================================================

@dataclass(slots=True)
class DatasetReport:
    """
    Complete dataset report.

    Contains all dataset-level information required
    by report renderers.
    """

    file: DatasetFileInfo = field(
        default_factory=DatasetFileInfo
    )

    structure: DatasetStructure = field(
        default_factory=DatasetStructure
    )

    column_types: ColumnTypeSummary = field(
        default_factory=ColumnTypeSummary
    )

    preview: DatasetPreview = field(
        default_factory=DatasetPreview
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the report into a serializable dictionary.
        """

        return asdict(self)
    
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "DatasetReport":
        """
        Deserialize DatasetReport.
        """

        return cls(
            file=DatasetFileInfo.from_dict(
                data.get(
                    "file",
                    {},
                )
            ),
            structure=DatasetStructure.from_dict(
                data.get(
                    "structure",
                    {},
                )
            ),
            column_types=ColumnTypeSummary.from_dict(
                data.get(
                    "column_types",
                    {},
                )
            ),
            preview=DatasetPreview.from_dict(
                data.get(
                    "preview",
                    {},
                )
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )