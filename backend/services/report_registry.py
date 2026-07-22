"""
Enterprise Report Registry

Maintains an in-memory registry of generated ReportPackage instances
alongside a lightweight searchable report index.

Author: InsightPilot AI
"""

from __future__ import annotations

from importlib import metadata
from typing import Dict

from backend.models.report_index import (
    ReportIndex,
    ReportIndexEntry,
)
from backend.models.report_package import ReportPackage


class ReportRegistry:
    """
    Enterprise in-memory registry for generated reports.

    Responsibilities
    ----------------
    - Register ReportPackage objects
    - Fast lookup by report ID
    - Maintain lightweight ReportIndex
    - Delete/Clear reports
    - Expose searchable index

    Notes
    -----
    This registry is intentionally in-memory. Future versions may
    persist the index to disk or a database without changing the API.
    """

    def __init__(self) -> None:
        self._reports: Dict[str, ReportPackage] = {}
        self._index = ReportIndex()
        self._history: dict[str, list[str]] = {}

    @property
    def index(self) -> ReportIndex:
        """
        Return the report index.
        """
        return self._index

    def register(self, package: ReportPackage) -> None:
        """
        Register a report package.

        Raises
        ------
        ValueError
            If the report already exists.
        """

        report_id = package.metadata.report_id

        if report_id in self._reports:
            raise ValueError(
                f"Report '{report_id}' is already registered."
            )

        self._reports[report_id] = package

        metadata = package.metadata

        formats: list[str] = []

        if package.html_report is not None:
            formats.append("HTML")

        if package.pdf_report is not None:
            formats.append("PDF")

        if package.json_report_path is not None:
            formats.append("JSON")

        entry = ReportIndexEntry(
            report_id=metadata.report_id,
            title=metadata.title,
            dataset_name=metadata.dataset_name,
            version=metadata.version,
            generated_at=metadata.generated_at.isoformat(),
            directory="",
            archive_path=None,
            formats=formats,
        )

        self._index.add(entry)
        dataset = metadata.dataset_name

        if dataset:

            self._history.setdefault(
                dataset,
                [],
            ).append(
                metadata.report_id
            )

    def get(self, report_id: str) -> ReportPackage:
        """
        Retrieve a report package.

        Raises
        ------
        KeyError
            If report does not exist.
        """

        if report_id not in self._reports:
            raise KeyError(
                f"Report '{report_id}' was not found."
            )

        return self._reports[report_id]

    def exists(self, report_id: str) -> bool:
        """
        Return True if report exists.
        """

        return report_id in self._reports

    def list(self) -> list[ReportPackage]:
        """
        Return all registered reports.
        """

        return list(self._reports.values())
    
    def find_by_dataset(
        self,
        dataset_name: str,
    ) -> list[ReportPackage]:
        """
        Return all reports for a dataset.
        """

        entries = self._index.find_by_dataset(dataset_name)

        return [
            self._reports[entry.report_id]
            for entry in entries
        ]


    def find_by_version(
        self,
        version: str,
    ) -> list[ReportPackage]:
        """
        Return all reports matching a version.
        """

        entries = self._index.find_by_version(version)

        return [
            self._reports[entry.report_id]
            for entry in entries
        ]


    def find_by_format(
        self,
        report_format: str,
    ) -> list[ReportPackage]:
        """
        Return all reports supporting the given format.
        """

        entries = self._index.find_by_format(report_format)

        return [
            self._reports[entry.report_id]
            for entry in entries
        ]


    def find_by_date_range(
        self,
        start: str,
        end: str,
    ) -> list[ReportPackage]:
        """
        Return reports generated between two ISO timestamps.
        """

        entries = self._index.find_by_date_range(
            start,
            end,
        )

        return [
            self._reports[entry.report_id]
            for entry in entries
        ]


    def list_sorted(
        self,
        reverse: bool = True,
    ) -> list[ReportPackage]:
        """
        Return reports sorted by generation time.
        """

        entries = self._index.list_sorted(
            reverse=reverse,
        )

        return [
            self._reports[entry.report_id]
            for entry in entries
        ]
    
    def get_history(
        self,
        dataset_name: str,
    ) -> list[ReportPackage]:
        """
        Return the complete report history for a dataset.

        Reports are returned in registration order
        (oldest → newest).
        """

        report_ids = self._history.get(
            dataset_name,
            [],
        )

        return [
            self._reports[report_id]
            for report_id in report_ids
            if report_id in self._reports
        ]


    def get_latest(
        self,
        dataset_name: str,
    ) -> ReportPackage | None:
        """
        Return the latest report generated for a dataset.

        Returns
        -------
        ReportPackage | None
        """

        history = self.get_history(
            dataset_name,
        )

        if not history:
            return None

        return history[-1]


    def get_versions(
        self,
        dataset_name: str,
    ) -> list[str]:
        """
        Return all report versions for a dataset.
        """

        return [
            report.metadata.version
            for report in self.get_history(
                dataset_name,
            )
        ]


    def has_history(
        self,
        dataset_name: str,
    ) -> bool:
        """
        Return True if history exists.
        """

        return dataset_name in self._history


    def history_count(
        self,
        dataset_name: str,
    ) -> int:
        """
        Return number of reports for a dataset.
        """

        return len(
            self._history.get(
                dataset_name,
                [],
            )
        )

    def delete(self, report_id: str) -> bool:
        """
        Delete a report from the registry.

        Returns
        -------
        bool
            True if the report was deleted, False if it was not found.
        """

        package = self._reports.get(report_id)

        if package is None:
            return False

        dataset = package.metadata.dataset_name

        del self._reports[report_id]

        self._index.remove(report_id)

        if dataset is not None and dataset in self._history:

            history = self._history[dataset]

            if report_id in history:
                history.remove(report_id)

            if not history:
                del self._history[dataset]

        return True

    def clear(self) -> None:
        """
        Remove all registered reports.
        """

        self._reports.clear()
        self._index.clear()
        self._history.clear()

    def count(self) -> int:
        """
        Return number of registered reports.
        """

        return len(self._reports)