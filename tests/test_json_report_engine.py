from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.engines.json_report_engine import JSONReportEngine

from backend.models.metadata import ReportMetadata
from backend.models.dataset_report import DatasetReport
from backend.models.quality_report import QualityReport
from backend.models.profiling_report import ProfilingReport
from backend.models.correlation_report import CorrelationReport
from backend.models.visualization_report import VisualizationReport
from backend.models.rule_report import RuleReport
from backend.models.insight_report import InsightReport
from backend.models.recommendation_report import RecommendationReport
from backend.models.report_context import ReportContext


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def engine() -> JSONReportEngine:
    """
    JSON report engine fixture.
    """
    return JSONReportEngine()


@pytest.fixture
def report_context() -> ReportContext:
    """
    Minimal valid ReportContext.
    """

    metadata = ReportMetadata(
        title="InsightPilot JSON Test Report",
    )

    dataset = DatasetReport()
    dataset.file.name = "bank_customers.csv"
    dataset.structure.total_rows = 1000
    dataset.structure.total_columns = 25

    return ReportContext(
        metadata=metadata,
        dataset=dataset,
        quality=QualityReport(),
        profiling=ProfilingReport(),
        correlation=CorrelationReport(),
        visualization=VisualizationReport(),
        rules=RuleReport(),
        insights=InsightReport(),
        recommendations=RecommendationReport(),
    )


# ============================================================
# Tests
# ============================================================

def test_generate_json_report(
    engine: JSONReportEngine,
    report_context: ReportContext,
    tmp_path: Path,
) -> None:
    """
    JSON report should be generated successfully.
    """

    output_file = tmp_path / "report.json"

    result = engine.generate(
        report_context,
        str(output_file),
    )

    assert result == str(output_file)
    assert output_file.exists()
    assert output_file.is_file()


def test_output_directory_created(
    engine: JSONReportEngine,
    report_context: ReportContext,
    tmp_path: Path,
) -> None:
    """
    Missing output directories should be created automatically.
    """

    output_file = (
        tmp_path
        / "enterprise"
        / "reports"
        / "report.json"
    )

    engine.generate(
        report_context,
        str(output_file),
    )

    assert output_file.exists()


def test_generated_json_is_valid(
    engine: JSONReportEngine,
    report_context: ReportContext,
    tmp_path: Path,
) -> None:
    """
    Generated report must contain valid JSON.
    """

    output_file = tmp_path / "report.json"

    engine.generate(
        report_context,
        str(output_file),
    )

    with output_file.open(
        encoding="utf-8",
    ) as fp:

        data = json.load(fp)

    assert isinstance(data, dict)


def test_metadata_serialized(
    engine: JSONReportEngine,
    report_context: ReportContext,
    tmp_path: Path,
) -> None:
    """
    Metadata should be serialized correctly.
    """

    output_file = tmp_path / "report.json"

    engine.generate(
        report_context,
        str(output_file),
    )

    with output_file.open(
        encoding="utf-8",
    ) as fp:

        data = json.load(fp)

    assert data["metadata"]["title"] == "InsightPilot JSON Test Report"
    assert "generated_at" in data["metadata"]
    assert "report_id" in data["metadata"]


def test_dataset_serialized(
    engine: JSONReportEngine,
    report_context: ReportContext,
    tmp_path: Path,
) -> None:
    """
    Dataset information should be present.
    """

    output_file = tmp_path / "report.json"

    engine.generate(
        report_context,
        str(output_file),
    )

    with output_file.open(
        encoding="utf-8",
    ) as fp:

        data = json.load(fp)

    dataset = data["dataset"]

    assert dataset["file"]["name"] == "bank_customers.csv"
    assert dataset["structure"]["total_rows"] == 1000
    assert dataset["structure"]["total_columns"] == 25


def test_all_sections_exist(
    engine: JSONReportEngine,
    report_context: ReportContext,
    tmp_path: Path,
) -> None:
    """
    Every ReportContext section should be exported.
    """

    output_file = tmp_path / "report.json"

    engine.generate(
        report_context,
        str(output_file),
    )

    with output_file.open(
        encoding="utf-8",
    ) as fp:

        data = json.load(fp)

    expected = {
        "metadata",
        "dataset",
        "quality",
        "profiling",
        "correlation",
        "visualization",
        "rules",
        "insights",
        "recommendations",
    }

    assert expected == set(data.keys())


def test_invalid_report_context(
    engine: JSONReportEngine,
) -> None:
    """
    Passing None should raise ValueError.
    """

    with pytest.raises(ValueError):
        engine.generate(None)  # type: ignore[arg-type]


def test_json_file_not_empty(
    engine: JSONReportEngine,
    report_context: ReportContext,
    tmp_path: Path,
) -> None:
    """
    Generated file should not be empty.
    """

    output_file = tmp_path / "report.json"

    engine.generate(
        report_context,
        str(output_file),
    )

    assert output_file.stat().st_size > 0