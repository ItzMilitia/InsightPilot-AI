from __future__ import annotations

from dataclasses import dataclass

from backend.models.report_context import ReportContext
from backend.models.report_package import ReportPackage


@dataclass(slots=True)
class LoadedReport:
    """
    Represents a fully reconstructed persisted report.
    """

    package: ReportPackage

    context: ReportContext