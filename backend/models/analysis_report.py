from __future__ import annotations

from dataclasses import dataclass

from backend.models.quality_report import QualityReport
from backend.models.profiling_report import ProfilingReport
from backend.models.correlation_report import CorrelationReport
from backend.models.visualization_report import VisualizationReport


@dataclass(slots=True)
class AnalysisReport:
    """
    Complete analysis produced by InsightPilot AI.
    """

    quality: QualityReport

    profiling: ProfilingReport

    correlation: CorrelationReport

    visualization: VisualizationReport