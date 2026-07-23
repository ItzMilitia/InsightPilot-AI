"""
Unit tests for the ReportComparison model.
"""

from __future__ import annotations

from datetime import UTC
from datetime import datetime

from backend.models.comparison_summary import ComparisonSummary
from backend.models.report_comparison import ReportComparison


# ==========================================================
# Default Construction
# ==========================================================


def test_default_construction() -> None:
    """
    ReportComparison should initialize correctly.
    """

    comparison = ReportComparison(
        baseline_report_id="report_001",
        comparison_report_id="report_002",
        baseline_version="v1.0",
        comparison_version="v1.1",
    )

    assert comparison.baseline_report_id == "report_001"
    assert comparison.comparison_report_id == "report_002"

    assert comparison.quality_score_before == 0.0
    assert comparison.quality_score_after == 0.0
    assert comparison.quality_score_delta == 0.0

    assert comparison.grade_before == ""
    assert comparison.grade_after == ""

    assert comparison.improvements == []
    assert comparison.regressions == []

    assert isinstance(
        comparison.summary,
        ComparisonSummary,
    )

    assert comparison.is_identical


# ==========================================================
# Improvement Detection
# ==========================================================


def test_has_improvements() -> None:
    """
    Improvements should be detected.
    """

    comparison = ReportComparison(
        baseline_report_id="a",
        comparison_report_id="b",
        baseline_version="1",
        comparison_version="2",
        improvements=[
            "Missing values reduced."
        ],
    )

    assert comparison.has_improvements
    assert not comparison.has_regressions
    assert not comparison.is_identical


# ==========================================================
# Regression Detection
# ==========================================================


def test_has_regressions() -> None:
    """
    Regressions should be detected.
    """

    comparison = ReportComparison(
        baseline_report_id="a",
        comparison_report_id="b",
        baseline_version="1",
        comparison_version="2",
        regressions=[
            "Duplicates increased."
        ],
    )

    assert comparison.has_regressions
    assert not comparison.has_improvements
    assert not comparison.is_identical


# ==========================================================
# Grade Change
# ==========================================================


def test_grade_change() -> None:
    """
    Grade changes should be detected.
    """

    comparison = ReportComparison(
        baseline_report_id="a",
        comparison_report_id="b",
        baseline_version="1",
        comparison_version="2",
        grade_before="B",
        grade_after="A",
    )

    assert comparison.has_grade_change
    assert not comparison.is_identical


# ==========================================================
# Quality Change
# ==========================================================


def test_quality_change() -> None:
    """
    Quality score changes should be detected.
    """

    comparison = ReportComparison(
        baseline_report_id="a",
        comparison_report_id="b",
        baseline_version="1",
        comparison_version="2",
        quality_score_before=82.5,
        quality_score_after=91.0,
        quality_score_delta=8.5,
    )

    assert comparison.has_quality_change
    assert not comparison.is_identical


# ==========================================================
# Serialization
# ==========================================================


def test_to_dict() -> None:
    """
    ReportComparison should serialize correctly.
    """

    comparison = ReportComparison(
        baseline_report_id="old",
        comparison_report_id="new",
        baseline_version="v1",
        comparison_version="v2",
        quality_score_before=80,
        quality_score_after=90,
        quality_score_delta=10,
        improvements=[
            "Quality improved."
        ],
        summary=ComparisonSummary(
            executive_summary="Improved overall."
        ),
    )

    data = comparison.to_dict()

    assert data["baseline_report_id"] == "old"
    assert data["comparison_report_id"] == "new"

    assert data["quality_score_before"] == 80
    assert data["quality_score_after"] == 90
    assert data["quality_score_delta"] == 10

    assert data["summary"]["executive_summary"] == (
        "Improved overall."
    )

    assert "generated_at" in data


# ==========================================================
# Deserialization
# ==========================================================


def test_from_dict() -> None:
    """
    ReportComparison should deserialize correctly.
    """

    now = datetime.now(UTC)

    data = {
        "baseline_report_id": "base",
        "comparison_report_id": "new",
        "baseline_version": "1",
        "comparison_version": "2",
        "quality_score_before": 75,
        "quality_score_after": 85,
        "quality_score_delta": 10,
        "grade_before": "B",
        "grade_after": "A",
        "missing_value_delta": -15,
        "duplicate_row_delta": -3,
        "duplicate_column_delta": 0,
        "outlier_delta": 2,
        "section_changes": {},
        "improvements": [
            "Duplicates removed."
        ],
        "regressions": [],
        "summary": {
            "executive_summary": "Improved."
        },
        "generated_at": now.isoformat(),
        "metadata": {},
    }

    comparison = ReportComparison.from_dict(data)

    assert comparison.baseline_report_id == "base"
    assert comparison.comparison_report_id == "new"

    assert comparison.grade_before == "B"
    assert comparison.grade_after == "A"

    assert comparison.summary.executive_summary == "Improved."

    assert comparison.generated_at == now


# ==========================================================
# Copy
# ==========================================================


def test_copy_creates_independent_instance() -> None:
    """
    copy() should create an independent object.
    """

    comparison = ReportComparison(
        baseline_report_id="old",
        comparison_report_id="new",
        baseline_version="1",
        comparison_version="2",
        improvements=[
            "Improvement"
        ],
    )

    copied = comparison.copy()

    assert copied == comparison
    assert copied is not comparison

    copied.improvements.append("Another")

    assert len(comparison.improvements) == 1
    assert len(copied.improvements) == 2


# ==========================================================
# Identical Reports
# ==========================================================


def test_identical_reports() -> None:
    """
    Identical reports should be detected.
    """

    comparison = ReportComparison(
        baseline_report_id="a",
        comparison_report_id="b",
        baseline_version="1",
        comparison_version="2",
    )

    assert comparison.is_identical


# ==========================================================
# Different Reports
# ==========================================================


def test_reports_not_identical() -> None:
    """
    Any metric change should make reports different.
    """

    comparison = ReportComparison(
        baseline_report_id="a",
        comparison_report_id="b",
        baseline_version="1",
        comparison_version="2",
        quality_score_delta=5,
    )

    assert not comparison.is_identical


# ==========================================================
# Summary Object
# ==========================================================


def test_summary_is_preserved() -> None:
    """
    Nested ComparisonSummary should be preserved.
    """

    summary = ComparisonSummary(
        executive_summary="Overall improved.",
        improvements=[
            "Lower missing values."
        ],
    )

    comparison = ReportComparison(
        baseline_report_id="old",
        comparison_report_id="new",
        baseline_version="1",
        comparison_version="2",
        summary=summary,
    )

    assert comparison.summary.executive_summary == (
        "Overall improved."
    )

    assert comparison.summary.has_improvements