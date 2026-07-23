from __future__ import annotations

"""
Enterprise Report History Service.

Provides a unified API for interacting with generated reports
throughout their lifecycle.

Responsibilities
----------------
- List generated reports
- Retrieve reports
- Check report existence
- Access report history
- Search reports
- Delete reports

This service acts as a façade over the existing report
infrastructure and intentionally contains minimal business logic.
"""

from backend.models.report_package import ReportPackage
from backend.services.report_index_service import ReportIndexService
from backend.services.report_registry import ReportRegistry
from backend.services.report_storage_service import ReportStorageService


class ReportHistoryService:
    """
    Enterprise Report History Service.

    Coordinates access to report history without duplicating
    responsibilities already implemented by lower-level services.
    """

    def __init__(
        self,
        registry: ReportRegistry | None = None,
        index_service: ReportIndexService | None = None,
        storage_service: ReportStorageService | None = None,
    ) -> None:

        self._registry = registry or ReportRegistry()

        self._index_service = (
            index_service
            or ReportIndexService()
        )

        self._storage_service = (
            storage_service
            or ReportStorageService()
        )

    # ======================================================
    # Basic Operations
    # ======================================================

    def list_reports(
        self,
    ) -> list[ReportPackage]:
        """
        Return all registered reports.
        """

        return self._registry.list()

    def get(
        self,
        report_id: str,
    ) -> ReportPackage:
        """
        Retrieve a report package.

        Raises
        ------
        KeyError
            If the report does not exist.
        """

        return self._registry.get(
            report_id,
        )

    def exists(
        self,
        report_id: str,
    ) -> bool:
        """
        Return True if a report exists.
        """

        return self._registry.exists(
            report_id,
        )

    def count(
        self,
    ) -> int:
        """
        Return the total number of reports.
        """

        return self._registry.count()

    # ======================================================
    # Dataset History
    # ======================================================

    def history(
        self,
        dataset_name: str,
    ) -> list[ReportPackage]:
        """
        Return the complete history for a dataset.
        """

        return self._registry.get_history(
            dataset_name,
        )

    def latest(
        self,
        dataset_name: str,
    ) -> ReportPackage | None:
        """
        Return the latest report for a dataset.
        """

        return self._registry.get_latest(
            dataset_name,
        )

    def versions(
        self,
        dataset_name: str,
    ) -> list[str]:
        """
        Return all versions generated for a dataset.
        """

        return self._registry.get_versions(
            dataset_name,
        )

    def has_history(
        self,
        dataset_name: str,
    ) -> bool:
        """
        Return True if history exists for a dataset.
        """

        return self._registry.has_history(
            dataset_name,
        )

    # ======================================================
    # Search Operations
    # ======================================================

    def find_by_dataset(
        self,
        dataset_name: str,
    ) -> list[ReportPackage]:
        """
        Return reports generated for a dataset.
        """

        return self._registry.find_by_dataset(
            dataset_name,
        )

    def find_by_version(
        self,
        version: str,
    ) -> list[ReportPackage]:
        """
        Return reports matching a version.
        """

        return self._registry.find_by_version(
            version,
        )

    def find_by_format(
        self,
        report_format: str,
    ) -> list[ReportPackage]:
        """
        Return reports supporting the requested format.
        """

        return self._registry.find_by_format(
            report_format,
        )

    def find_by_date_range(
        self,
        start: str,
        end: str,
    ) -> list[ReportPackage]:
        """
        Return reports generated within a date range.
        """

        return self._registry.find_by_date_range(
            start,
            end,
        )
    
    # ======================================================
    # Advanced History
    # ======================================================

    def previous_version(
        self,
        dataset_name: str,
        version: str,
    ) -> ReportPackage | None:
        """
        Return the report immediately preceding the supplied version.
        """

        history = self.history(
            dataset_name,
        )

        if not history:
            return None

        for index, report in enumerate(history):

            if report.metadata.version == version:

                if index == 0:
                    return None

                return history[index - 1]

        return None

    def next_version(
        self,
        dataset_name: str,
        version: str,
    ) -> ReportPackage | None:
        """
        Return the report immediately following the supplied version.
        """

        history = self.history(
            dataset_name,
        )

        if not history:
            return None

        for index, report in enumerate(history):

            if report.metadata.version == version:

                if index == len(history) - 1:
                    return None

                return history[index + 1]

        return None

    def latest_version(
        self,
        dataset_name: str,
    ) -> str | None:
        """
        Return the latest version string for a dataset.
        """

        latest = self.latest(
            dataset_name,
        )

        if latest is None:
            return None

        return latest.metadata.version

    def comparison_candidates(
        self,
        dataset_name: str,
    ) -> tuple[ReportPackage, ReportPackage] | None:
        """
        Return the two most recent reports for comparison.

        Returns
        -------
        tuple[ReportPackage, ReportPackage] | None
            (previous, latest) if at least two reports exist.
        """

        history = self.history(
            dataset_name,
        )

        if len(history) < 2:
            return None

        return (
            history[-2],
            history[-1],
        )

    def report_lineage(
        self,
        dataset_name: str,
    ) -> list[str]:
        """
        Return the version lineage for a dataset.

        Example
        -------
        ['v1.0.0', 'v1.1.0', 'v2.0.0']
        """

        return [
            report.metadata.version
            for report in self.history(
                dataset_name,
            )
        ]

    def report_ids(
        self,
        dataset_name: str,
    ) -> list[str]:
        """
        Return report IDs for the supplied dataset.
        """

        return [
            report.metadata.report_id
            for report in self.history(
                dataset_name,
            )
        ]

    # ======================================================
    # Lifecycle
    # ======================================================

    def delete(
        self,
        report_id: str,
    ) -> bool:
        """
        Delete a report.

        Returns
        -------
        bool
            True if deleted.
        """

        return self._registry.delete(
            report_id,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all reports.
        """

        self._registry.clear()

    # ======================================================
    # Helpers
    # ======================================================

    @property
    def registry(
        self,
    ) -> ReportRegistry:
        """
        Return the underlying registry.
        """

        return self._registry

    @property
    def index_service(
        self,
    ) -> ReportIndexService:
        """
        Return the report index service.
        """

        return self._index_service

    @property
    def storage_service(
        self,
    ) -> ReportStorageService:
        """
        Return the report storage service.
        """

        return self._storage_service