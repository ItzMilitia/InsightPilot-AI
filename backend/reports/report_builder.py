"""
Enterprise Report Builder.

Responsible for assembling a strongly typed ReportContext from
the outputs of all InsightPilot AI engines.

The ReportBuilder is intentionally independent of any rendering
technology (HTML, PDF, JSON, etc.).
"""

from __future__ import annotations

from backend.models.correlation_report import CorrelationReport
from backend.models.dataset_report import DatasetReport
from backend.models.insight_report import InsightReport
from backend.models.metadata import ReportMetadata
from backend.models.profiling_report import ProfilingReport
from backend.models.quality_report import QualityReport
from backend.models.recommendation_report import RecommendationReport
from backend.models.report_context import ReportContext
from backend.models.rule_report import RuleReport
from backend.models.visualization_report import VisualizationReport


class ReportBuilder:
    """
    Enterprise Report Builder.

    Responsibilities
    ----------------
    - Aggregate engine outputs
    - Assemble ReportContext
    - Provide a single report object for renderers
    """

    def build(
        self,
        *,
        metadata: ReportMetadata | None = None,
        dataset: DatasetReport | None = None,
        quality: QualityReport | None = None,
        profiling: ProfilingReport | None = None,
        correlation: CorrelationReport | None = None,
        visualization: VisualizationReport | None = None,
        rules: RuleReport | None = None,
        insights: InsightReport | None = None,
        recommendations: RecommendationReport | None = None,
    ) -> ReportContext:
        """
        Build a complete ReportContext.

        Parameters
        ----------
        metadata
            Report metadata.

        dataset
            Dataset report.

        quality
            Quality report.

        profiling
            Profiling report.

        correlation
            Correlation report.

        visualization
            Visualization report.

        rules
            Rule evaluation report.

        insights
            AI-generated insights.

        recommendations
            Actionable recommendations.

        Returns
        -------
        ReportContext
            Fully populated report context.
        """

        return ReportContext(
            metadata=metadata or ReportMetadata(),
            dataset=dataset or DatasetReport(),
            quality=quality or QualityReport(),
            profiling=profiling or ProfilingReport(),
            correlation=correlation or CorrelationReport(),
            visualization=visualization or VisualizationReport(),
            rules=rules or RuleReport(),
            insights=insights or InsightReport(),
            recommendations=recommendations or RecommendationReport(),
        )