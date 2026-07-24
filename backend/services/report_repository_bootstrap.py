"""
Enterprise Report Repository Bootstrap.

Responsible for reconstructing persisted report packages
during application startup.

Responsibilities
----------------
- Read report index.
- Reconstruct persisted reports.
- Register reports in the in-memory registry.
- Skip invalid or missing reports.
- Produce startup statistics.

This service performs startup initialization only.
It contains no business logic related to report
generation or report exploration.

Author
------
InsightPilot AI

Version
-------
v0.9.4
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import logging

from backend.services.report_index_service import (
    ReportIndexService,
)
from backend.services.report_loader_service import (
    ReportLoaderService,
)
from backend.services.report_registry import (
    ReportRegistry,
)


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class BootstrapSummary:
    """
    Startup loading summary.
    """

    discovered: int = 0
    loaded: int = 0
    skipped: int = 0
    failed: int = 0


class ReportRepositoryBootstrap:
    """
    Restores persisted reports into memory.

    Execution Flow
    --------------
    report_index.json
            │
            ▼
    ReportIndexService
            │
            ▼
    ReportLoaderService
            │
            ▼
    ReportRegistry
    """

    def __init__(
        self,
        registry: ReportRegistry,
        loader_service: ReportLoaderService,
        index_service: ReportIndexService,
    ) -> None:

        self._registry = registry
        self._loader = loader_service
        self._index = index_service

    # ======================================================
    # Public API
    # ======================================================

    def initialize(
        self,
    ) -> BootstrapSummary:
        """
        Restore all persisted reports.

        Returns
        -------
        BootstrapSummary
        """

        summary = BootstrapSummary()

        entries = self._index.all_reports() or []

        summary.discovered = len(entries)

        for entry in entries:

            report_id = entry.report_id

            if self._registry.exists(report_id):

                summary.skipped += 1
                continue

            try:

                loaded = self._loader.load(
                    report_id,
                )

                self._registry.register(
                    loaded.package,
                )

                summary.loaded += 1

            except FileNotFoundError:

                logger.warning(
                    "Persisted report '%s' is missing.",
                    report_id,
                )

                summary.failed += 1

            except Exception:

                logger.exception(
                    "Failed to restore report '%s'.",
                    report_id,
                )

                summary.failed += 1

        return summary