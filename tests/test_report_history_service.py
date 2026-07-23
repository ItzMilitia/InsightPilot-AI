from __future__ import annotations

from datetime import datetime

import pytest

from backend.models.html_report import HTMLReport
from backend.models.metadata import ReportMetadata
from backend.models.report_package import ReportPackage
from backend.services.report_history_service import (
    ReportHistoryService,
)
from backend.services.report_registry import ReportRegistry


# ==========================================================
# Helpers
# ==========================================================


def build_package(
    report_id: str,
    dataset: str,
    version: str,
) -> ReportPackage:

    metadata = ReportMetadata(
        report_id=report_id,
        title=f"Report {report_id}",
        dataset_name=dataset,
        version=version,
        generated_at=datetime.now(),
    )

    return ReportPackage(
        metadata=metadata,
        html_report=HTMLReport(
            title=f"Report {report_id}",
            html="<html></html>",
        ),
        pdf_report=None,
        json_report_path=None,
    )


@pytest.fixture
def registry() -> ReportRegistry:

    registry = ReportRegistry()

    registry.register(
        build_package(
            "r1",
            "bank_customers",
            "1.0.0",
        )
    )

    registry.register(
        build_package(
            "r2",
            "bank_customers",
            "1.1.0",
        )
    )

    registry.register(
        build_package(
            "r3",
            "credit_risk",
            "1.0.0",
        )
    )

    return registry


@pytest.fixture
def history(
    registry: ReportRegistry,
) -> ReportHistoryService:

    return ReportHistoryService(
        registry=registry,
    )


# ==========================================================
# Initialization
# ==========================================================


def test_service_initialization():

    service = ReportHistoryService()

    assert service is not None


# ==========================================================
# Basic Operations
# ==========================================================


def test_list_reports(
    history: ReportHistoryService,
):

    reports = history.list_reports()

    assert len(reports) == 3


def test_count(
    history: ReportHistoryService,
):

    assert history.count() == 3


def test_exists_true(
    history: ReportHistoryService,
):

    assert history.exists("r1")


def test_exists_false(
    history: ReportHistoryService,
):

    assert not history.exists("unknown")


def test_get(
    history: ReportHistoryService,
):

    report = history.get("r1")

    assert report.metadata.report_id == "r1"


def test_get_invalid(
    history: ReportHistoryService,
):

    with pytest.raises(KeyError):

        history.get("invalid")


# ==========================================================
# Dataset History
# ==========================================================


def test_history(
    history: ReportHistoryService,
):

    reports = history.history(
        "bank_customers",
    )

    assert len(reports) == 2


def test_latest(
    history: ReportHistoryService,
):

    latest = history.latest(
        "bank_customers",
    )

    assert latest is not None
    assert latest.metadata.version == "1.1.0"


def test_versions(
    history: ReportHistoryService,
):

    versions = history.versions(
        "bank_customers",
    )

    assert versions == [
        "1.0.0",
        "1.1.0",
    ]


def test_has_history_true(
    history: ReportHistoryService,
):

    assert history.has_history(
        "bank_customers",
    )


def test_has_history_false(
    history: ReportHistoryService,
):

    assert not history.has_history(
        "telecom",
    )


# ==========================================================
# Search
# ==========================================================


def test_find_by_dataset(
    history: ReportHistoryService,
):

    reports = history.find_by_dataset(
        "bank_customers",
    )

    assert len(reports) == 2


def test_find_by_version(
    history: ReportHistoryService,
):

    reports = history.find_by_version(
        "1.0.0",
    )

    assert len(reports) == 2


# ==========================================================
# Advanced History
# ==========================================================


def test_previous_version(
    history: ReportHistoryService,
):

    report = history.previous_version(
        "bank_customers",
        "1.1.0",
    )

    assert report is not None
    assert report.metadata.version == "1.0.0"


def test_previous_version_none(
    history: ReportHistoryService,
):

    report = history.previous_version(
        "bank_customers",
        "1.0.0",
    )

    assert report is None


def test_next_version(
    history: ReportHistoryService,
):

    report = history.next_version(
        "bank_customers",
        "1.0.0",
    )

    assert report is not None
    assert report.metadata.version == "1.1.0"


def test_next_version_none(
    history: ReportHistoryService,
):

    report = history.next_version(
        "bank_customers",
        "1.1.0",
    )

    assert report is None


def test_latest_version(
    history: ReportHistoryService,
):

    version = history.latest_version(
        "bank_customers",
    )

    assert version == "1.1.0"


def test_comparison_candidates(
    history: ReportHistoryService,
):

    previous, latest = history.comparison_candidates(
        "bank_customers",
    )

    assert previous.metadata.version == "1.0.0"
    assert latest.metadata.version == "1.1.0"


def test_report_lineage(
    history: ReportHistoryService,
):

    lineage = history.report_lineage(
        "bank_customers",
    )

    assert lineage == [
        "1.0.0",
        "1.1.0",
    ]


def test_report_ids(
    history: ReportHistoryService,
):

    ids = history.report_ids(
        "bank_customers",
    )

    assert ids == [
        "r1",
        "r2",
    ]


# ==========================================================
# Lifecycle
# ==========================================================


def test_delete(
    history: ReportHistoryService,
):

    assert history.delete("r1")

    assert history.count() == 2


def test_delete_invalid(
    history: ReportHistoryService,
):

    assert not history.delete(
        "unknown",
    )


def test_clear(
    history: ReportHistoryService,
):

    history.clear()

    assert history.count() == 0