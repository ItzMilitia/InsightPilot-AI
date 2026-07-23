from __future__ import annotations

from copy import deepcopy

import pytest

from backend.engines.report_comparison_engine import (
    ReportComparisonEngine,
)
from backend.models.comparison_summary import (
    ComparisonSummary,
)
from backend.models.correlation_report import (
    CorrelationReport,
)
from backend.models.dataset_report import (
    DatasetReport,
)
from backend.models.insight_report import (
    InsightReport,
)
from backend.models.metadata import (
    ReportMetadata,
)
from backend.models.profiling_report import (
    ProfilingReport,
    ProfilingSummary,
    MemoryProfile,
)
from backend.models.quality_report import (
    QualityReport,
    QualitySummary,
    MissingValueReport,
    DuplicateReport,
    DataTypeReport,
    OutlierReport,
)
from backend.models.recommendation_report import (
    RecommendationReport,
)
from backend.models.report_comparison import (
    ReportComparison,
)
from backend.models.report_context import (
    ReportContext,
)
from backend.models.rule_report import (
    RuleReport,
)
from backend.models.visualization_report import (
    VisualizationReport,
)

def build_quality(
    score: float = 90.0,
    grade: str = "Excellent",
) -> QualityReport:

    report = QualityReport()

    report.summary = QualitySummary(
        total_rows=100,
        total_columns=10,
        score=score,
        grade=grade,
    )

    report.missing = MissingValueReport(
        total_missing=0,
        columns={},
    )

    report.duplicates = DuplicateReport(
        duplicate_rows=0,
        duplicate_columns=0,
        row_summary={},
        column_summary={},
    )

    report.data_types = DataTypeReport(
        summary={},
    )

    report.outliers = OutlierReport(
        columns={},
    )

    report.recommendations = []

    return report

def build_profiling() -> ProfilingReport:

    report = ProfilingReport()

    report.summary = ProfilingSummary(
        total_columns=10,
        numeric_columns=5,
        categorical_columns=5,
        datetime_columns=0,
    )

    report.numeric_profiles = []
    report.categorical_profiles = []
    report.datetime_profiles = []

    report.high_cardinality_columns = []

    report.memory = MemoryProfile(
        total_memory="10 KB",
        average_column_memory="1 KB",
    )

    return report

def build_metadata(
    report_id: str = "report_001",
    version: str = "1.0.0",
) -> ReportMetadata:

    metadata = ReportMetadata()

    metadata.report_id = report_id
    metadata.version = version
    metadata.title = "Comparison Test"
    metadata.report_type = "quality"
    metadata.dataset_name = "bank_customers.csv"
    metadata.execution_time = 5.0
    metadata.tags = []
    metadata.metadata = {}

    return metadata

def build_context(
    score: float = 90.0,
    report_id: str = "report_001",
) -> ReportContext:

    return ReportContext(
        metadata=build_metadata(
            report_id=report_id,
        ),
        dataset=DatasetReport(),
        quality=build_quality(score),
        profiling=build_profiling(),
        correlation=CorrelationReport(),
        visualization=VisualizationReport(),
        rules=RuleReport(),
        insights=InsightReport(),
        recommendations=RecommendationReport(),
    )

@pytest.fixture
def engine():

    return ReportComparisonEngine()


@pytest.fixture
def baseline():

    return build_context(
        score=80,
        report_id="baseline",
    )


@pytest.fixture
def comparison():

    return build_context(
        score=90,
        report_id="comparison",
    )

# ============================================================
# Test 1
# ============================================================

def test_engine_initialization():

    engine = ReportComparisonEngine()

    assert isinstance(
        engine,
        ReportComparisonEngine,
    )

    assert engine.service is not None

# ============================================================
# Test 2
# ============================================================

def test_compare_returns_reportcomparison(
    engine,
    baseline,
    comparison,
):

    result = engine.analyze(
        baseline,
        comparison,
    )

    assert isinstance(
        result,
        ReportComparison,
    )

    assert result.baseline_report_id == "baseline"

    assert (
        result.comparison_report_id
        == "comparison"
    )

    assert result.summary is not None

    assert isinstance(
        result.summary,
        ComparisonSummary,
    )

# ============================================================
# Test 3
# ============================================================

def test_quality_delta_calculated(
    engine,
    baseline,
    comparison,
):

    baseline.quality.summary.score = 80.0

    comparison.quality.summary.score = 90.0

    result = engine.analyze(
        baseline,
        comparison,
    )

    assert result.quality_score_before == 80.0

    assert result.quality_score_after == 90.0

    assert result.quality_score_delta == 10.0

    assert (
        result.summary.executive_summary
        != ""
    )

    assert (
        len(result.summary.improvements)
        >= 1
    )

# ============================================================
# Test 4
# ============================================================

def test_identical_reports(
    engine,
    baseline,
    comparison,
):

    comparison = deepcopy(baseline)

    result = engine.analyze(
        baseline,
        comparison,
    )

    assert result.quality_score_delta == 0.0

    assert result.missing_value_delta == 0

    assert result.duplicate_row_delta == 0

    assert result.duplicate_column_delta == 0

    assert result.outlier_delta == 0

    assert len(
        result.summary.regressions
    ) == 0

# ============================================================
# Test 5
# ============================================================

def test_invalid_report(
    engine,
    comparison,
):

    with pytest.raises(ValueError):

        engine.analyze(
            None,
            comparison,
        )

    with pytest.raises(ValueError):

        engine.analyze(
            comparison,
            None,
        )

# ============================================================
# Test 6
# ============================================================

def test_metadata_preserved(
    engine,
    baseline,
    comparison,
):

    baseline.metadata.report_id = (
        "baseline_report"
    )

    comparison.metadata.report_id = (
        "comparison_report"
    )

    baseline.metadata.version = "1.0.0"

    comparison.metadata.version = "2.0.0"

    result = engine.analyze(
        baseline,
        comparison,
    )

    assert (
        result.baseline_report_id
        == "baseline_report"
    )

    assert (
        result.comparison_report_id
        == "comparison_report"
    )

    assert (
        result.baseline_version
        == "1.0.0"
    )

    assert (
        result.comparison_version
        == "2.0.0"
    )