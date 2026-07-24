"""
Anomaly Detection Engine

Provides the foundation for machine learning-based anomaly
detection within InsightPilot AI.

Sprint 11.0 - Phase 1
"""

from __future__ import annotations

import logging
import time

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from backend.core.base_engine import BaseEngine
from backend.models.anomaly_report import (
    AnomalyReport,
    AnomalySummary,
)


logger = logging.getLogger(__name__)


class AnomalyDetectionEngine(BaseEngine):
    """
    Enterprise anomaly detection engine.

    This engine provides the common interface for all
    anomaly detection algorithms implemented in
    InsightPilot AI.
    """

    def __init__(self) -> None:
        """Initialize the anomaly detection engine."""
        super().__init__()

    def analyze(
        self,
        dataframe: pd.DataFrame,
    ) -> AnomalyReport:
        """
        Analyze a dataset for anomalies.

        Parameters
        ----------
        dataframe : pd.DataFrame
            Dataset to analyze.

        Returns
        -------
        AnomalyReport
            Structured anomaly detection report.
        """

        logger.info(
            "Starting anomaly detection..."
        )

        start_time = time.perf_counter()

        self._validate_dataframe(
            dataframe
        )

        numeric_dataframe = (
            self._prepare_features(
                dataframe
            )
        )

        anomaly_rows, anomaly_scores = (
            self._run_isolation_forest(
                numeric_dataframe
            )
        )

        report = self._build_report(
            numeric_dataframe,
            anomaly_rows,
            anomaly_scores,
        )

        report.summary.execution_time = (
            round(
                time.perf_counter() - start_time,
                3,
            )
        )

        logger.info(
            "Anomaly detection completed."
        )

        return report

    # --------------------------------------------------
    # Private Methods
    # --------------------------------------------------

    def _validate_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate the input dataframe.
        """

        if dataframe is None:
            raise ValueError(
                "DataFrame cannot be None."
            )

        if dataframe.empty:
            raise ValueError(
                "DataFrame is empty."
            )

    def _prepare_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Prepare numeric features for anomaly detection.

        Phase 2:
        - Select numeric columns
        - Replace infinite values
        - Impute missing values
        """

        logger.info(
            "Preparing numeric features..."
        )

        numeric_dataframe = dataframe.select_dtypes(
            include="number"
        ).copy()

        if numeric_dataframe.empty:
            raise ValueError(
                "No numeric columns available for anomaly detection."
            )

        numeric_dataframe.replace(
            [np.inf, -np.inf],
            np.nan,
            inplace=True,
        )

        numeric_dataframe.fillna(
            numeric_dataframe.median(
                numeric_only=True
            ),
            inplace=True,
        )

        return numeric_dataframe

    def _run_isolation_forest(
        self,
        dataframe: pd.DataFrame,
    ) -> tuple[list[int], list[float]]:
        """
        Execute Isolation Forest.

        Parameters
        ----------
        dataframe : pd.DataFrame
            Prepared numeric dataframe.

        Returns
        -------
        tuple[list[int], list[float]]
            Row indices detected as anomalies and
            their anomaly scores.
        """

        logger.info(
            "Running Isolation Forest..."
        )

        model = IsolationForest(
            contamination="auto",
            random_state=42,
        )

        predictions = model.fit_predict(
            dataframe
        )

        scores = model.decision_function(
            dataframe
        )

        anomaly_mask = predictions == -1

        anomaly_rows = (
            dataframe.index[
                anomaly_mask
            ].tolist()
        )

        anomaly_scores = (
            scores[
                anomaly_mask
            ].tolist()
        )

        logger.info(
            "Isolation Forest detected %d anomalies.",
            len(anomaly_rows),
        )

        return (
            anomaly_rows,
            anomaly_scores,
        )

    def _run_local_outlier_factor(
        self,
        dataframe: pd.DataFrame,
    ):
        """
        Placeholder for Local Outlier Factor.

        Implemented in Sprint 11.0 Phase 2.
        """

        raise NotImplementedError

    def _build_report(
        self,
        dataframe: pd.DataFrame,
        anomaly_rows: list[int],
        anomaly_scores: list[float],
    ) -> AnomalyReport:
        """
        Build an empty anomaly report.

        Phase 1 implementation.
        """

        logger.info(
            "Building anomaly report..."
        )

        total_rows = len(dataframe)

        anomaly_count = len(anomaly_rows)

        anomaly_percentage = (
            (anomaly_count / total_rows) * 100
            if total_rows
            else 0.0
        )

        if anomaly_percentage < 1:

            severity = "Low"

        elif anomaly_percentage < 5:

            severity = "Medium"

        elif anomaly_percentage < 10:

            severity = "High"

        else:

            severity = "Critical"

        confidence = (
            round(
                float(
                    abs(min(anomaly_scores))
                ),
                3,
            )
            if anomaly_scores
            else 0.0
        )

        report = AnomalyReport()

        report.summary = AnomalySummary(
            algorithm="Isolation Forest",
            algorithm_version="1.0",
            anomaly_count=anomaly_count,
            anomaly_percentage=round(
                anomaly_percentage,
                2,
            ),
            severity=severity,
            confidence_score=confidence,
        )

        report.detected_rows = anomaly_rows

        report.anomaly_scores = anomaly_scores

        report.metadata = {
            "rows": total_rows,
            "numeric_columns": len(
                dataframe.columns
            ),
            "feature_count": len(
                dataframe.columns
            ),
            "sample_count": total_rows,
        }

        return report