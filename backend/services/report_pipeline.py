from __future__ import annotations

from pathlib import Path

import pandas as pd

from backend.engines.analysis_engine import AnalysisEngine
from backend.engines.html_report_engine import HTMLReportEngine
from backend.engines.insight_engine import InsightEngine
from backend.engines.json_report_engine import JSONReportEngine
from backend.engines.pdf_report_engine import PDFReportEngine
from backend.engines.rule_engine import RuleEngine
from backend.engines.report_comparison_engine import (
    ReportComparisonEngine,
)
from backend.services.report_registry import ReportRegistry
from backend.models.html_report import HTMLReport
from backend.models.pdf_report import PDFReport
from backend.models.report_context import ReportContext
from backend.models.report_index import ReportIndexEntry
from backend.models.report_package import ReportPackage

from backend.services.dataset_service import DatasetService
from backend.services.recommendation_service import RecommendationService
from backend.services.report_archive_service import ReportArchiveService
from backend.services.report_builder import ReportBuilder
from backend.services.report_index_service import ReportIndexService
from backend.services.report_storage_service import ReportStorageService
from backend.services.report_validation_service import ReportValidationService


class ReportPipeline:
    """
    Enterprise reporting pipeline.

    Responsible only for orchestrating the complete report
    generation lifecycle.

    Execution Flow
    --------------
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
        │
        ▼
    JSONReportEngine (optional)
        │
        ▼
    ReportStorageService (optional)
        │
        ▼
    ReportValidationService
        │
        ▼
    ReportArchiveService
        │
        ▼
    ReportIndexService
    """

    def __init__(
        self,
        registry: ReportRegistry | None = None,
    ):

        self._registry = registry or ReportRegistry()

        self._dataset_service = DatasetService()

        self._analysis_engine = AnalysisEngine()

        self._rule_engine = RuleEngine()

        self._insight_engine = InsightEngine()

        self._recommendation_service = RecommendationService()

        self._report_builder = ReportBuilder()

        self._html_engine = HTMLReportEngine()

        self._pdf_engine = PDFReportEngine()

        self._json_engine = JSONReportEngine()

        self._comparison_engine = (
            ReportComparisonEngine()
        )

        self._storage_service = ReportStorageService()

        self._validation_service = ReportValidationService()

        self._archive_service = ReportArchiveService()

        self._index_service = ReportIndexService()

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
        persist_reports: bool = False,
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
        if dataframe.empty:
            raise ValueError(
                "Cannot generate reports from an empty DataFrame."
            )
        
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
            or "dataset"
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

        if not return_package:

            return (
                context,
                html_report,
                pdf_path,
            )

        package = ReportPackage(
            metadata=context.metadata,
            html_report=html_report,
            pdf_report=pdf_report,
            json_report_path=json_path,
        )
        
        self._registry.register(package)

        if persist_reports:

            report_directory = (
                Path("reports")
                / context.metadata.report_id
            )

            package = self._storage_service.save(
                package=package,
                output_directory=report_directory,
            )

            package.add_artifact(
                "report_directory",
                str(report_directory),
            )

            validation = (
                self._validation_service.validate(
                    report_directory
                )
            )

            # ValidationResult returns collected errors instead of
            # raising exceptions.
            if validation.has_errors():

                raise RuntimeError(
                    "Generated report package failed validation:\n"
                    + "\n".join(validation.errors)
                )

            archive_path = (
                self._archive_service.archive(
                    report_directory
                )
            )

            package.add_artifact(
                "archive",
                str(archive_path),
            )

            entry = ReportIndexEntry(
                report_id=context.metadata.report_id,
                title=context.metadata.title,
                dataset_name=dataset_name,
                version=context.metadata.version,
                generated_at=context.metadata.generated_at,
                directory=str(report_directory),
                archive_path=str(archive_path),
                formats=package.available_formats(),
            )

            self._index_service.register(
                entry,
            )

        #
        # Ensure generated artifacts are registered even when
        # persist_reports=False.
        #

        if pdf_path is not None and "pdf" not in package.artifacts:

            package.add_artifact(
                "pdf",
                pdf_path,
            )

        if json_path is not None and "json" not in package.artifacts:

            package.add_artifact(
                "json",
                json_path,
            )

        return package
    
    def compare_reports(
            self,
            baseline: ReportContext,
            comparison: ReportContext,
        ):
            """
            Compare two generated reports.

            Parameters
            ----------
            baseline:
                Original report.

            comparison:
                Newly generated report.

            Returns
            -------
            ReportComparison
                Comparison between the supplied reports.
            """

            return self._comparison_engine.analyze(
                baseline,
                comparison,
            )

    @property
    def registry(self) -> ReportRegistry:
        """
        Return the report registry associated with this pipeline.
        """
        return self._registry