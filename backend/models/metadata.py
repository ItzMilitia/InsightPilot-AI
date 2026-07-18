"""
Enterprise Report Metadata Model.

Defines metadata associated with generated InsightPilot AI reports.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import UTC
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ReportType(str, Enum):
    """
    Supported report output formats.
    """

    HTML = "HTML"
    PDF = "PDF"
    JSON = "JSON"


@dataclass(slots=True)
class ReportMetadata:
    """
    Metadata describing a generated InsightPilot AI report.
    """

    report_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = "InsightPilot AI Report"

    version: str = "0.9.0"

    generated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    generated_by: str = "InsightPilot AI"

    report_type: ReportType = ReportType.HTML

    status: str = "Completed"

    author: str | None = None

    dataset_name: str | None = None

    execution_time: float | None = None

    tags: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert metadata into a serializable dictionary.
        """

        data = asdict(self)

        data["generated_at"] = self.generated_at.isoformat()
        data["report_type"] = self.report_type.value

        return data