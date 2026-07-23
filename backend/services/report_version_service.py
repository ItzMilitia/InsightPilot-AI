from __future__ import annotations

"""
Enterprise Report Version Service.

Provides version navigation and lineage functionality for
InsightPilot AI reports.

Responsibilities
----------------
- Version history
- Previous/Next version lookup
- Latest version lookup
- Version lineage
- Comparison candidate selection

This service operates on top of ReportHistoryService and
contains version-specific business logic.
"""

from backend.models.report_package import ReportPackage
from backend.services.report_history_service import (
    ReportHistoryService,
)


class ReportVersionService:
    """
    Enterprise Report Version Service.
    """

    def __init__(
        self,
        history_service: ReportHistoryService | None = None,
    ) -> None:

        self._history = (
            history_service
            or ReportHistoryService()
        )

    # ======================================================
    # Version Navigation
    # ======================================================

    def latest(
        self,
        dataset_name: str,
    ) -> ReportPackage | None:
        """
        Return latest report.
        """

        return self._history.latest(
            dataset_name,
        )

    def previous(
        self,
        dataset_name: str,
        version: str,
    ) -> ReportPackage | None:
        """
        Return previous version.
        """

        return self._history.previous_version(
            dataset_name,
            version,
        )

    def next(
        self,
        dataset_name: str,
        version: str,
    ) -> ReportPackage | None:
        """
        Return next version.
        """

        return self._history.next_version(
            dataset_name,
            version,
        )

    # ======================================================
    # Version Information
    # ======================================================

    def latest_version(
        self,
        dataset_name: str,
    ) -> str | None:
        """
        Return latest version string.
        """

        return self._history.latest_version(
            dataset_name,
        )

    def all_versions(
        self,
        dataset_name: str,
    ) -> list[str]:
        """
        Return every version.
        """

        return self._history.versions(
            dataset_name,
        )

    def lineage(
        self,
        dataset_name: str,
    ) -> list[str]:
        """
        Return version lineage.
        """

        return self._history.report_lineage(
            dataset_name,
        )

    # ======================================================
    # Comparison
    # ======================================================

    def comparison_pair(
        self,
        dataset_name: str,
    ) -> tuple[
        ReportPackage,
        ReportPackage,
    ] | None:
        """
        Return the latest comparison pair.
        """

        return self._history.comparison_candidates(
            dataset_name,
        )

    def has_multiple_versions(
        self,
        dataset_name: str,
    ) -> bool:
        """
        Return True if dataset has multiple versions.
        """

        return len(
            self._history.history(
                dataset_name,
            )
        ) > 1