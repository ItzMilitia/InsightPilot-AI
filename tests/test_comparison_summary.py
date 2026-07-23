"""
Unit tests for the ComparisonSummary model.
"""

from __future__ import annotations

from backend.models.comparison_summary import ComparisonSummary


# ==========================================================
# Default Construction
# ==========================================================


def test_default_construction() -> None:
    """
    ComparisonSummary should initialize with default values.
    """

    summary = ComparisonSummary()

    assert summary.executive_summary == ""
    assert summary.improvements == []
    assert summary.regressions == []
    assert summary.recommendations == []

    assert summary.is_empty
    assert not summary.has_improvements
    assert not summary.has_regressions
    assert len(summary) == 0


# ==========================================================
# Improvements
# ==========================================================


def test_has_improvements() -> None:
    """
    has_improvements should reflect improvement entries.
    """

    summary = ComparisonSummary(
        improvements=[
            "Missing values reduced."
        ]
    )

    assert summary.has_improvements
    assert not summary.has_regressions
    assert not summary.is_empty
    assert len(summary) == 1


# ==========================================================
# Regressions
# ==========================================================


def test_has_regressions() -> None:
    """
    has_regressions should reflect regression entries.
    """

    summary = ComparisonSummary(
        regressions=[
            "Duplicate rows increased."
        ]
    )

    assert summary.has_regressions
    assert not summary.has_improvements
    assert not summary.is_empty
    assert len(summary) == 1


# ==========================================================
# Mixed Findings
# ==========================================================


def test_length_counts_findings() -> None:
    """
    __len__ should count improvements and regressions.
    """

    summary = ComparisonSummary(
        improvements=[
            "Quality score improved.",
            "Missing values reduced.",
        ],
        regressions=[
            "Outliers increased."
        ],
    )

    assert len(summary) == 3


# ==========================================================
# Serialization
# ==========================================================


def test_to_dict() -> None:
    """
    Model should serialize correctly.
    """

    summary = ComparisonSummary(
        executive_summary="Quality improved.",
        improvements=[
            "Quality score increased."
        ],
        regressions=[
            "Outlier count increased."
        ],
        recommendations=[
            "Review detected outliers."
        ],
    )

    data = summary.to_dict()

    assert data["executive_summary"] == "Quality improved."
    assert data["improvements"] == [
        "Quality score increased."
    ]
    assert data["regressions"] == [
        "Outlier count increased."
    ]
    assert data["recommendations"] == [
        "Review detected outliers."
    ]


# ==========================================================
# Deserialization
# ==========================================================


def test_from_dict() -> None:
    """
    Model should deserialize correctly.
    """

    data = {
        "executive_summary": "Dataset improved.",
        "improvements": [
            "Duplicates removed."
        ],
        "regressions": [],
        "recommendations": [
            "Continue monitoring."
        ],
    }

    summary = ComparisonSummary.from_dict(data)

    assert summary.executive_summary == "Dataset improved."
    assert summary.improvements == [
        "Duplicates removed."
    ]
    assert summary.regressions == []
    assert summary.recommendations == [
        "Continue monitoring."
    ]


# ==========================================================
# Copy
# ==========================================================


def test_copy_creates_independent_instance() -> None:
    """
    copy() should return an independent object.
    """

    original = ComparisonSummary(
        executive_summary="Original",
        improvements=[
            "Improvement"
        ],
        recommendations=[
            "Recommendation"
        ],
    )

    copied = original.copy()

    assert copied == original
    assert copied is not original

    copied.improvements.append("New")

    assert len(original.improvements) == 1
    assert len(copied.improvements) == 2


# ==========================================================
# Empty Detection
# ==========================================================


def test_is_empty_with_recommendations() -> None:
    """
    Recommendations alone should make the summary non-empty.
    """

    summary = ComparisonSummary(
        recommendations=[
            "Review quality metrics."
        ]
    )

    assert not summary.is_empty


# ==========================================================
# Empty Dictionary
# ==========================================================


def test_from_empty_dict() -> None:
    """
    Deserializing an empty dictionary should produce defaults.
    """

    summary = ComparisonSummary.from_dict({})

    assert summary.executive_summary == ""
    assert summary.improvements == []
    assert summary.regressions == []
    assert summary.recommendations == []

    assert summary.is_empty