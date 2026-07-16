from __future__ import annotations

import pandas as pd

from backend.core.base_engine import BaseEngine

from backend.engines.quality_engine import QualityEngine
from backend.engines.profiling_engine import ProfilingEngine
from backend.engines.correlation_engine import CorrelationEngine
from backend.engines.visualization_engine import VisualizationEngine

from backend.models.analysis_report import AnalysisReport


class AnalysisEngine(BaseEngine):
    """
    Orchestrates all analysis engines and returns a unified report.

    This engine contains no business logic. It coordinates the
    execution of specialized engines and aggregates their outputs
    into a single AnalysisReport.
    """

    def __init__(self) -> None:
        super().__init__()

        self._quality_engine = QualityEngine()
        self._profiling_engine = ProfilingEngine()
        self._correlation_engine = CorrelationEngine()
        self._visualization_engine = VisualizationEngine()

    def analyze(
        self,
        df: pd.DataFrame,
    ) -> AnalysisReport:
        """
        Run all analysis engines and return a unified report.
        """

        start = self.log_start("Complete Dataset Analysis")

        quality_report = self._quality_engine.analyze(df)

        profiling_report = self._profiling_engine.analyze(df)

        correlation_report = self._correlation_engine.analyze(df)

        visualization_report = self._visualization_engine.analyze(df)

        report = AnalysisReport(
            quality=quality_report,
            profiling=profiling_report,
            correlation=correlation_report,
            visualization=visualization_report,
        )

        self.log_finish(
            "Complete Dataset Analysis",
            start,
        )

        return report