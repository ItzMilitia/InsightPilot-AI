from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PDFReport:
    """
    Represents a generated PDF report.
    """

    title: str

    file_path: str