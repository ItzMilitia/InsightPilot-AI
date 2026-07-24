"""
Enterprise Report Explorer Service.

Provides a unified entry point for browsing and exploring
generated InsightPilot AI reports.

The ReportExplorerService composes higher-level services such
as ReportHistoryService and ReportVersionService without
containing UI-specific logic.

Responsibilities
----------------
- Dependency composition
- Future report browsing
- Future filtering
- Future searching
- Future pagination

Author:
    InsightPilot AI

Version:
    v0.9.3
"""

from __future__ import annotations

from backend.engines.report_comparison_engine import ReportComparisonEngine
from backend.services.report_history_service import (
    ReportHistoryService,
)
from backend.services.report_registry import ReportRegistry
from backend.services.report_version_service import (
    ReportVersionService,
)
from backend.models.report_package import ReportPackage
from datetime import datetime
from operator import attrgetter
import math
from backend.models.loaded_report import LoadedReport
from backend.services.report_loader_service import ReportLoaderService
from backend.models.report_comparison import ReportComparison

class ReportExplorerService:
    """
    High-level service for report exploration.

    This service acts as the single entry point for future
    report browsing functionality. It composes the history
    and version services while remaining independent of any
    presentation layer.
    """

    def __init__(
        self,
        registry: ReportRegistry,
        history_service: ReportHistoryService,
        version_service: ReportVersionService,
        loader_service: ReportLoaderService,
        comparison_engine: ReportComparisonEngine,
    ):
        """
        Initialize the Report Explorer Service.

        Parameters
        ----------
        history_service:
            Optional ReportHistoryService instance.

        version_service:
            Optional ReportVersionService instance.
        """

        self._history_service = history_service

        self._version_service = version_service

        self._loader = loader_service

        self._comparison_engine = comparison_engine

    # ======================================================
    # Properties
    # ======================================================

    @property
    def history_service(
        self,
    ) -> ReportHistoryService:
        """
        Return the ReportHistoryService.
        """

        return self._history_service

    @property
    def version_service(
        self,
    ) -> ReportVersionService:
        """
        Return the ReportVersionService.
        """

        return self._version_service
    
    # ======================================================
    # Browsing APIs
    # ======================================================

    def list_reports(
        self,
    ) -> list:
        """
        Return all registered reports.

        Returns
        -------
        list
            List of ReportPackage instances.
        """

        return self._history_service.list_reports()

    def datasets(
        self,
    ) -> list[str]:
        """
        Return all unique dataset names.

        Returns
        -------
        list[str]
            Sorted dataset names.
        """

        datasets = {
            report.metadata.dataset_name
            for report in self.list_reports()
        }

        return sorted(datasets)

    def versions(
        self,
        dataset_name: str,
    ) -> list[str]:
        """
        Return all versions for a dataset.

        Parameters
        ----------
        dataset_name:
            Dataset identifier.

        Returns
        -------
        list[str]
            Available versions.
        """

        return self._history_service.versions(
            dataset_name,
        )

    def latest(
        self,
        dataset_name: str,
    ):
        """
        Return the latest report for a dataset.

        Parameters
        ----------
        dataset_name:
            Dataset identifier.

        Returns
        -------
        ReportPackage | None
        """

        return self._version_service.latest(
            dataset_name,
        )
    
    # ======================================================
    # Filtering APIs
    # ======================================================

    def filter_by_dataset(
        self,
        dataset_name: str,
    ) -> list[ReportPackage]:
        """
        Return all reports for a dataset.

        Parameters
        ----------
        dataset_name:
            Dataset identifier.

        Returns
        -------
        list[ReportPackage]
            Matching ReportPackage instances.
        """

        return self._history_service.find_by_dataset(
            dataset_name,
        )

    def filter_by_version(
        self,
        version: str,
    ) -> list[ReportPackage]:
        """
        Return all reports matching a version.

        Parameters
        ----------
        version:
            Report version.

        Returns
        -------
        list[ReportPackage]
            Matching ReportPackage instances.
        """

        return self._history_service.find_by_version(
            version,
        )

    def filter_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> list[ReportPackage]:
        """
        Return reports generated within a date range.

        Parameters
        ----------
        start_date:
            Inclusive start datetime.

        end_date:
            Inclusive end datetime.

        Returns
        -------
        list[ReportPackage]
            Matching ReportPackage instances.
        """

        return self._history_service.find_by_date_range(
            start_date.isoformat(),
            end_date.isoformat(),
        )
    
    # ======================================================
    # Search APIs
    # ======================================================

    def search(
        self,
        query: str,
    ) -> list[ReportPackage]:
        """
        Search reports using report metadata.

        Search is performed against:

        - Report ID
        - Report title
        - Dataset name
        - Version

        Parameters
        ----------
        query:
            Search text.

        Returns
        -------
        list[ReportPackage]
            Matching reports.
        """

        query = query.strip().lower()

        if not query:
            return self.list_reports()

        matches: list[ReportPackage] = []

        for report in self.list_reports():

            metadata = report.metadata

            searchable_fields = (
                metadata.report_id,
                metadata.title,
                metadata.dataset_name,
                metadata.version,
            )

            if any(
                query in str(field).lower()
                for field in searchable_fields
                if field is not None
            ):
                matches.append(report)

        return matches
    
    # ======================================================
    # Sorting APIs
    # ======================================================

    def sort_reports(
        self,
        reports: list[ReportPackage],
        *,
        sort_by: str = "generated_at",
        descending: bool = True,
    ) -> list[ReportPackage]:
        """
        Sort reports by a metadata field.

        Supported fields
        ----------------
        - generated_at
        - version
        - title
        - dataset_name
        - report_id

        Parameters
        ----------
        reports:
            Reports to sort.

        sort_by:
            Metadata field name.

        descending:
            Sort order.

        Returns
        -------
        list[ReportPackage]
            Sorted reports.

        Raises
        ------
        ValueError
            If the requested field is unsupported.
        """

        valid_fields = {
            "generated_at",
            "version",
            "title",
            "dataset_name",
            "report_id",
        }

        if sort_by not in valid_fields:
            raise ValueError(
                f"Unsupported sort field: {sort_by}"
            )

        return sorted(
            reports,
            key=lambda report: getattr(
                report.metadata,
                sort_by,
            ),
            reverse=descending,
        )
    
        # ======================================================
    # Pagination APIs
    # ======================================================

    def paginate(
        self,
        reports: list[ReportPackage],
        *,
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        """
        Paginate a collection of reports.

        Parameters
        ----------
        reports:
            Reports to paginate.

        page:
            One-based page number.

        page_size:
            Number of reports per page.

        Returns
        -------
        dict
            Pagination information containing:

            - items
            - page
            - page_size
            - total_items
            - total_pages
            - has_previous
            - has_next

        Raises
        ------
        ValueError
            If page or page_size is less than 1.
        """

        if page < 1:
            raise ValueError(
                "page must be greater than or equal to 1."
            )

        if page_size < 1:
            raise ValueError(
                "page_size must be greater than or equal to 1."
            )

        total_items = len(reports)

        total_pages = max(
            1,
            math.ceil(total_items / page_size),
        )

        page = min(page, total_pages)

        start = (page - 1) * page_size
        end = start + page_size

        return {
            "items": reports[start:end],
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_previous": page > 1,
            "has_next": page < total_pages,
        }
    
        # ======================================================
    # Summary APIs
    # ======================================================

    def summary(self) -> dict:
        """
        Return a high-level summary of the report repository.

        Returns
        -------
        dict
            Repository summary.
        """

        reports = self.list_reports()
        datasets = self.datasets()

        return {
            "total_reports": len(reports),
            "total_datasets": len(datasets),
            "datasets": datasets,
        }

    def dataset_summary(
        self,
        dataset_name: str,
    ) -> dict:
        """
        Return summary information for a dataset.

        Parameters
        ----------
        dataset_name:
            Dataset identifier.

        Returns
        -------
        dict
            Dataset summary.
        """

        reports = self.filter_by_dataset(
            dataset_name,
        )

        latest = self.latest(
            dataset_name,
        )

        versions = self.versions(
            dataset_name,
        )

        return {
            "dataset_name": dataset_name,
            "report_count": len(reports),
            "versions": versions,
            "latest_version": (
                latest.metadata.version
                if latest is not None
                else None
            ),
            "latest_report": latest,
        }

    def version_summary(
        self,
        dataset_name: str,
    ) -> dict:
        """
        Return version statistics for a dataset.

        Parameters
        ----------
        dataset_name:
            Dataset identifier.

        Returns
        -------
        dict
            Version summary.
        """

        versions = self.versions(
            dataset_name,
        )

        return {
            "dataset_name": dataset_name,
            "version_count": len(versions),
            "versions": versions,
        }
    
    def compare_reports(
        self,
        baseline,
        comparison,
    ):
        """
        Compare two report contexts.

        Parameters
        ----------
        baseline:
            Baseline ReportContext.

        comparison:
            Comparison ReportContext.

        Returns
        -------
        ReportComparison
            Comparison produced by the ReportComparisonEngine.
        """

        from backend.engines.report_comparison_engine import (
            ReportComparisonEngine,
        )

        engine = ReportComparisonEngine()

        return engine.analyze(
            baseline=baseline,
            comparison=comparison,
        )
    
    def load_report(
        self,
        report_id: str,
    ) -> LoadedReport:
        """
        Load a persisted report.

        Parameters
        ----------
        report_id:
            Identifier of the report.

        Returns
        -------
        LoadedReport
            Fully reconstructed report.
        """

        return self._loader.load(
            report_id
        )
    
    def compare_reports(
        self,
        baseline_report_id: str,
        comparison_report_id: str,
    ) -> ReportComparison:
        """
        Compare two persisted reports.

        Parameters
        ----------
        baseline_report_id:
            Baseline report identifier.

        comparison_report_id:
            Comparison report identifier.

        Returns
        -------
        ReportComparison
        """

        baseline = self.load_report(
            baseline_report_id
        )

        comparison = self.load_report(
            comparison_report_id
        )

        return self._comparison_engine.analyze(
            baseline=baseline.context,
            comparison=comparison.context,
        )