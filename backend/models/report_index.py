"""
Enterprise Report Index Models.

Defines the persistent registry of generated InsightPilot AI
reports.

The index is composed of individual report entries and a
collection model that provides convenience helpers for
managing the registry.

Future versions may extend these models to support:

- Tags
- Authors
- Status
- Categories
- Cloud storage locations
- Custom metadata
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any


# ==========================================================
# Report Index Entry
# ==========================================================


@dataclass(slots=True)
class ReportIndexEntry:
    """
    Represents a single indexed report.
    """

    report_id: str

    title: str

    dataset_name: str | None

    version: str

    generated_at: str

    directory: str

    archive_path: str | None = None

    formats: list[str] = field(
        default_factory=list
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert entry into a serializable dictionary.
        """

        return asdict(self)


# ==========================================================
# Report Index
# ==========================================================


@dataclass(slots=True)
class ReportIndex:
    """
    Represents the complete report registry.
    """

    entries: list[ReportIndexEntry] = field(
        default_factory=list
    )

    # ======================================================
    # Entry Management
    # ======================================================

    def add(
        self,
        entry: ReportIndexEntry,
    ) -> None:
        """
        Add a report entry.

        Duplicate report IDs are ignored.
        """

        if self.find_by_report_id(
            entry.report_id,
        ) is not None:
            return

        self.entries.append(entry)

    def remove(
        self,
        report_id: str,
    ) -> bool:
        """
        Remove a report entry.

        Returns
        -------
        bool
            True if removed.
        """

        entry = self.find_by_report_id(
            report_id,
        )

        if entry is None:
            return False

        self.entries.remove(entry)

        return True

    def clear(self) -> None:
        """
        Remove all entries.
        """

        self.entries.clear()

    # ======================================================
    # Search Helpers
    # ======================================================

    def find_by_report_id(
        self,
        report_id: str,
    ) -> ReportIndexEntry | None:
        """
        Find report by ID.
        """

        for entry in self.entries:

            if entry.report_id == report_id:
                return entry

        return None

    def find_by_dataset(
        self,
        dataset_name: str,
    ) -> list[ReportIndexEntry]:
        """
        Find reports by dataset.
        """

        return [
            entry
            for entry in self.entries
            if entry.dataset_name == dataset_name
        ]

    def find_by_version(
        self,
        version: str,
    ) -> list[ReportIndexEntry]:
        """
        Find reports by version.
        """

        return [
            entry
            for entry in self.entries
            if entry.version == version
        ]

    # ======================================================
    # Convenience Helpers
    # ======================================================

    def count(self) -> int:
        """
        Return total indexed reports.
        """

        return len(self.entries)

    def is_empty(self) -> bool:
        """
        Return True if the index is empty.
        """

        return self.count() == 0

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Convert index into a serializable dictionary.
        """

        return {
            "entries": [
                entry.to_dict()
                for entry in self.entries
            ]
        }