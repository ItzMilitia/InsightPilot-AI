from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from backend.models.correlation_report import CorrelationReport
from backend.models.profiling_report import ProfilingReport
from backend.models.quality_report import QualityReport
from backend.models.visualization_report import VisualizationReport


@dataclass(slots=True)
class AnalysisReport:
    """
    Complete analysis produced by InsightPilot AI.
    """

    quality: QualityReport = field(
        default_factory=QualityReport
    )

    profiling: ProfilingReport = field(
        default_factory=ProfilingReport
    )

    correlation: CorrelationReport = field(
        default_factory=CorrelationReport
    )

    visualization: VisualizationReport = field(
        default_factory=VisualizationReport
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)