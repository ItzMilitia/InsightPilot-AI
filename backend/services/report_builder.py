from __future__ import annotations

from pathlib import Path

from backend.models.analysis_report import AnalysisReport
from backend.models.dataset_report import DatasetReport
from backend.models.insight_report import InsightReport
from backend.models.metadata import ReportMetadata
from backend.models.recommendation_report import RecommendationReport
from backend.models.report_context import ReportContext
from backend.models.rule_report import RuleReport


class ReportBuilder:
    """
    Builds the enterprise ReportContext from the outputs
    of all InsightPilot AI engines.

    This class contains no business logic. It simply
    aggregates validated report models into a single
    object that can be consumed by HTML, PDF, JSON,
    API, and future renderers.
    """

    def build(
        self,
        *,
        dataset: DatasetReport,
        analysis: AnalysisReport,
        rules: RuleReport,
        insights: InsightReport,
        recommendations: RecommendationReport,
        title: str = "InsightPilot AI Report",
        dataset_name: str | None = None,
    ) -> ReportContext:
        """
        Build the enterprise ReportContext.
        """

        metadata = ReportMetadata(
            title=title,
            dataset_name=dataset_name,
        )

        return ReportContext(
            metadata=metadata,
            dataset=dataset,
            quality=analysis.quality,
            profiling=analysis.profiling,
            correlation=analysis.correlation,
            visualization=analysis.visualization,
            rules=rules,
            insights=insights,
            recommendations=recommendations,
        )

    @staticmethod
    def infer_dataset_name(
        file_path: str | None,
    ) -> str | None:
        """
        Infer dataset name from a file path.
        """

        if not file_path:
            return None

        return Path(file_path).stem