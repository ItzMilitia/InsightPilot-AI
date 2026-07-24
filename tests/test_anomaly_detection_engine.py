"""
Unit tests for AnomalyDetectionEngine.

Sprint 11.0 - Phase 1
"""

from __future__ import annotations

import pandas as pd
import pytest

from backend.engines.anomaly_detection_engine import (
    AnomalyDetectionEngine,
)
from backend.models.anomaly_report import (
    AnomalyReport,
)


@pytest.fixture
def engine() -> AnomalyDetectionEngine:
    """
    Create an AnomalyDetectionEngine instance.
    """

    return AnomalyDetectionEngine()


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """
    Create a simple numeric dataframe.
    """

    return pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [10, 20, 30, 40, 50],
        }
    )

@pytest.fixture
def anomaly_dataframe() -> pd.DataFrame:
    """
    Dataset containing obvious anomalies.
    """

    normal = pd.DataFrame(
        {
            "A": list(range(100)),
            "B": list(range(100)),
        }
    )

    anomalies = pd.DataFrame(
        {
            "A": [1000, 1200, 1500],
            "B": [1000, 1200, 1500],
        }
    )

    return pd.concat(
        [normal, anomalies],
        ignore_index=True,
    )

def test_engine_initialization(
    engine: AnomalyDetectionEngine,
) -> None:
    """
    Engine should initialize successfully.
    """

    assert engine is not None


def test_analyze_returns_report(
    engine: AnomalyDetectionEngine,
    sample_dataframe: pd.DataFrame,
) -> None:
    """
    Analyze should return an AnomalyReport.
    """

    report = engine.analyze(
        sample_dataframe
    )

    assert isinstance(
        report,
        AnomalyReport,
    )


def test_empty_dataframe_raises_error(
    engine: AnomalyDetectionEngine,
) -> None:
    """
    Empty dataframe should raise ValueError.
    """

    with pytest.raises(ValueError):
        engine.analyze(
            pd.DataFrame()
        )


def test_none_dataframe_raises_error(
    engine: AnomalyDetectionEngine,
) -> None:
    """
    None dataframe should raise ValueError.
    """

    with pytest.raises(ValueError):
        engine.analyze(None)


def test_execution_time_recorded(
    engine: AnomalyDetectionEngine,
    sample_dataframe: pd.DataFrame,
) -> None:
    """
    Execution time should always be recorded.
    """

    report = engine.analyze(
        sample_dataframe
    )

    assert (
        report.summary.execution_time >= 0
    )


def test_numeric_metadata(
    engine: AnomalyDetectionEngine,
    sample_dataframe: pd.DataFrame,
) -> None:
    """
    Numeric metadata should be populated.
    """

    report = engine.analyze(
        sample_dataframe
    )

    assert (
        report.metadata["rows"] == 5
    )

    assert (
        report.metadata["numeric_columns"] == 2
    )


def test_default_summary_values(
    engine: AnomalyDetectionEngine,
    sample_dataframe: pd.DataFrame,
) -> None:
    """
    Phase 1 should return placeholder values.
    """

    report = engine.analyze(
        sample_dataframe
    )

    assert (
        report.summary.algorithm
        == "Isolation Forest"
    )

    assert (
        report.summary.algorithm_version
        == "1.0"
    )

    assert (
        report.summary.anomaly_count
        >= 0
    )

    assert report.summary.severity in {
        "Low",
        "Medium",
        "High",
        "Critical",
    }

def test_isolation_forest_detects_anomalies(
    engine: AnomalyDetectionEngine,
    anomaly_dataframe: pd.DataFrame,
) -> None:
    """
    Isolation Forest should detect
    obvious anomalies.
    """

    report = engine.analyze(
        anomaly_dataframe
    )

    assert (
        report.summary.algorithm
        == "Isolation Forest"
    )

    assert (
        report.summary.anomaly_count > 0
    )

    assert (
        len(report.detected_rows)
        ==
        report.summary.anomaly_count
    )

def test_anomaly_percentage(
    engine: AnomalyDetectionEngine,
    anomaly_dataframe: pd.DataFrame,
) -> None:
    """
    Percentage should be valid.
    """

    report = engine.analyze(
        anomaly_dataframe
    )

    assert (
        0
        <=
        report.summary.anomaly_percentage
        <=
        100
    )

def test_confidence_score(
    engine: AnomalyDetectionEngine,
    anomaly_dataframe: pd.DataFrame,
) -> None:
    """
    Confidence score should be non-negative.
    """

    report = engine.analyze(
        anomaly_dataframe
    )

    assert (
        report.summary.confidence_score
        >=
        0
    )

def test_metadata_population(
    engine: AnomalyDetectionEngine,
    anomaly_dataframe: pd.DataFrame,
) -> None:
    """
    Metadata should be populated.
    """

    report = engine.analyze(
        anomaly_dataframe
    )

    assert (
        report.metadata["sample_count"]
        ==
        len(anomaly_dataframe)
    )

    assert (
        report.metadata["feature_count"]
        ==
        2
    )
def test_anomaly_scores(
    engine: AnomalyDetectionEngine,
    anomaly_dataframe: pd.DataFrame,
) -> None:
    """
    Every detected anomaly should
    have a score.
    """

    report = engine.analyze(
        anomaly_dataframe
    )

    assert (
        len(report.detected_rows)
        ==
        len(report.anomaly_scores)
    )

def test_severity(
    engine: AnomalyDetectionEngine,
    anomaly_dataframe: pd.DataFrame,
) -> None:
    """
    Severity should be valid.
    """

    report = engine.analyze(
        anomaly_dataframe
    )

    assert report.summary.severity in {
        "Low",
        "Medium",
        "High",
        "Critical",
    }
