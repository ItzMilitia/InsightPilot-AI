from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HTMLReport:
    """
    Represents a generated HTML report.
    """

    title: str

    html: str