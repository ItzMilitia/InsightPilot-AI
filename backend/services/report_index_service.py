from __future__ import annotations

"""
Enterprise Report Index Service.

Maintains a persistent registry of generated InsightPilot AI
reports.

Responsibilities
----------------
- Register reports
- Load index
- Save index
- Search reports
- Prevent duplicate registrations
"""

import json
from pathlib import Path
from typing import Any

from backend.models.report_index import (
    ReportIndex,
    ReportIndexEntry,
)


class ReportIndexService:
    """
    Service responsible for maintaining the report index.
    """

    DEFAULT_INDEX_PATH = Path(
        "reports/report_index.json"
    )

    def __init__(
        self,
        index_path: str | Path | None = None,
    ) -> None:

        self._index_path = (
            Path(index_path)
            if index_path is not None
            else self.DEFAULT_INDEX_PATH
        )

        self._index = ReportIndex()

    # ======================================================
    # Public API
    # ======================================================

    def load(self) -> ReportIndex:
        """
        Load the report index from disk.
        """

        if not self._index_path.exists():

            self._index = ReportIndex()

            return self._index

        with self._index_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        entries = []

        for item in data.get(
            "entries",
            [],
        ):

            entries.append(
                ReportIndexEntry(**item)
            )

        self._index = ReportIndex(
            entries=entries,
        )

        return self._index

    def save(self) -> None:
        """
        Persist the report index.
        """

        self._index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._index_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._index.to_dict(),
                file,
                indent=4,
                ensure_ascii=False,
            )

    def register(
        self,
        entry: ReportIndexEntry,
    ) -> None:
        """
        Register a report.

        Duplicate report IDs are ignored.
        """

        self.load()

        self._index.add(
            entry,
        )

        self.save()

    # ======================================================
    # Search API
    # ======================================================

    def find_by_report_id(
        self,
        report_id: str,
    ) -> ReportIndexEntry | None:

        self.load()

        return self._index.find_by_report_id(
            report_id,
        )

    def find_by_dataset(
        self,
        dataset_name: str,
    ) -> list[ReportIndexEntry]:

        self.load()

        return self._index.find_by_dataset(
            dataset_name,
        )

    def find_by_version(
        self,
        version: str,
    ) -> list[ReportIndexEntry]:

        self.load()

        return self._index.find_by_version(
            version,
        )

    def all_reports(
        self,
    ) -> list[ReportIndexEntry]:
        """
        Return every indexed report.
        """

        self.load()

        return list(
            self._index.entries
        )

    # ======================================================
    # Helpers
    # ======================================================

    def clear(self) -> None:
        """
        Remove all indexed reports.
        """

        self._index = ReportIndex()

        self.save()

    @property
    def index_path(self) -> Path:
        """
        Return the configured index path.
        """

        return self._index_path