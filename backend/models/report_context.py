"""
Enterprise Report Context.

Root model representing a complete InsightPilot AI report.
Acts as the single source of truth for all report renderers
(HTML, PDF, JSON, API, etc.).
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any

from backend.models.correlation_report import CorrelationReport
from backend.models.dataset_report import DatasetReport
from backend.models.insight_report import InsightReport
from backend.models.metadata import ReportMetadata
from backend.models.profiling_report import ProfilingReport
from backend.models.quality_report import QualityReport
from backend.models.recommendation_report import RecommendationReport
from backend.models.rule_report import RuleReport
from backend.models.visualization_report import VisualizationReport


@dataclass(slots=True)
class ReportContext:
    """
    Root object containing the complete report generated
    by InsightPilot AI.

    Every report renderer should consume this object rather
    than individual engine outputs.
    """

    metadata: ReportMetadata

    dataset: DatasetReport

    quality: QualityReport

    profiling: ProfilingReport

    correlation: CorrelationReport

    visualization: VisualizationReport

    rules: RuleReport

    insights: InsightReport

    recommendations: RecommendationReport

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the complete report into a serializable dictionary.

        Returns
        -------
        dict[str, Any]
            Dictionary representation of the report context.
        """

        return asdict(self)