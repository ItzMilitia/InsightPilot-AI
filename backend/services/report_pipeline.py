from __future__ import annotations

from pathlib import Path

import pandas as pd

from backend.engines.analysis_engine import AnalysisEngine
from backend.engines.html_report_engine import HTMLReportEngine
from backend.engines.insight_engine import InsightEngine
from backend.engines.pdf_report_engine import PDFReportEngine
from backend.engines.rule_engine import RuleEngine
from backend.engines.json_report_engine import JSONReportEngine

from backend.models.pdf_report import PDFReport
from backend.models.report_package import ReportPackage
from backend.models.html_report import HTMLReport
from backend.models.report_context import ReportContext

from backend.services.dataset_service import DatasetService
from backend.services.recommendation_service import RecommendationService
from backend.services.report_builder import ReportBuilder


class ReportPipeline:
    """
    Enterprise reporting pipeline.

    Responsible only for orchestration.

    Execution Flow

        DataFrame
            │
            ▼
        DatasetService
            │
            ▼
        AnalysisEngine
            │
            ▼
        RuleEngine
            │
            ▼
        InsightEngine
            │
            ▼
        RecommendationService
            │
            ▼
        ReportBuilder
            │
            ▼
        HTMLReportEngine
            │
            ▼
        PDFReportEngine (optional)
    """

    def __init__(self) -> None:

        self._dataset_service = DatasetService()

        self._analysis_engine = AnalysisEngine()

        self._rule_engine = RuleEngine()

        self._insight_engine = InsightEngine()

        self._recommendation_service = RecommendationService()

        self._report_builder = ReportBuilder()

        self._html_engine = HTMLReportEngine()

        self._pdf_engine = PDFReportEngine()

        self._json_engine = JSONReportEngine()

    def run(
        self,
        *,
        dataframe: pd.DataFrame,
        file_name: str | None = None,
        file_path: str | None = None,
        encoding: str | None = None,
        rule_pack: str = "generic",
        required_columns: list[str] | None = None,
        generate_pdf: bool = False,
        pdf_output_path: str = "reports/report.pdf",
        generate_json: bool = True,
        json_output_path: str = "reports/report.json",
        return_package: bool = False,
    ) -> (
        tuple[
            ReportContext,
            HTMLReport,
            str | None,
        ]
        | ReportPackage
    ):
        """
        Execute the complete reporting pipeline.

        By default, the legacy API is preserved.

        Set return_package=True to return a ReportPackage
        containing all generated report artifacts.
        """

        dataset = self._dataset_service.build(
            dataframe,
            file_name=file_name,
            file_path=file_path,
            encoding=encoding,
        )

        analysis = self._analysis_engine.analyze(
            dataframe,
        )

        rules = self._rule_engine.evaluate(
            dataframe=dataframe,
            required_columns=required_columns,
            pack=rule_pack,
        )

        insights = self._insight_engine.analyze(
            analysis,
        )

        recommendations = (
            self._recommendation_service.build(
                analysis=analysis,
                rules=rules,
                insights=insights,
            )
        )

        dataset_name = (
            self._report_builder.infer_dataset_name(
                file_path
            )
            or file_name
        )

        context = self._report_builder.build(
            dataset=dataset,
            analysis=analysis,
            rules=rules,
            insights=insights,
            recommendations=recommendations,
            dataset_name=dataset_name,
        )

        html_report = self._html_engine.generate(
            context,
        )

        pdf_report: PDFReport | None = None
        pdf_path: str | None = None

        if generate_pdf:

            output = Path(pdf_output_path)

            output.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            pdf_report = self._pdf_engine.generate(
                html_report=html_report,
                output_path=str(output),
            )

            pdf_path = pdf_report.file_path

        json_path: str | None = None

        if generate_json:

            json_path = self._json_engine.generate(
                report_context=context,
                output_path=json_output_path,
            )

        if return_package:

            package = ReportPackage(
                metadata=context.metadata,
                html_report=html_report,
                pdf_report=pdf_report,
                json_report_path=json_path,
            )

            package.add_artifact(
                "html",
                "IN_MEMORY",
            )

            if pdf_path:

                package.add_artifact(
                    "pdf",
                    pdf_path,
                )

            if json_path:

                package.add_artifact(
                    "json",
                    json_path,
                )

            return package

        return (
            context,
            html_report,
            pdf_path,
        )