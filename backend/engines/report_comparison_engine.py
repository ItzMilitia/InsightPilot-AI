from __future__ import annotations

from backend.core.base_engine import BaseEngine
from backend.models.report_comparison import ReportComparison
from backend.models.report_context import ReportContext
from backend.services.report_comparison_service import (
    ReportComparisonService,
)


class ReportComparisonEngine(BaseEngine):
    """
    Generates a comparison between two reports.
    """

    def __init__(self) -> None:
        super().__init__()
        self.service = ReportComparisonService()

    def analyze(
        self,
        baseline: ReportContext,
        comparison: ReportContext,
    ) -> ReportComparison:
        """
        Compare two ReportContext objects.
        """

        start = self.log_start(
            "Report Comparison"
        )

        try:

            report = self.service.compare(
                baseline,
                comparison,
            )

            self.log_finish(
                "Report Comparison",
                start,
            )

            return report

        except Exception as exc:

            self.log_error(
                "Report Comparison",
                exc,
            )

            raise