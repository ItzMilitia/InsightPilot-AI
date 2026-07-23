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
from backend.services.report_version_service import (
    ReportVersionService,
)


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
            "bank_customers",
            "2.0.0",
        )
    )

    registry.register(
        build_package(
            "r4",
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


@pytest.fixture
def version_service(
    history: ReportHistoryService,
) -> ReportVersionService:

    return ReportVersionService(
        history_service=history,
    )


# ==========================================================
# Initialization
# ==========================================================


def test_service_initialization():

    service = ReportVersionService()

    assert service is not None


# ==========================================================
# Latest
# ==========================================================


def test_latest(
    version_service: ReportVersionService,
):

    latest = version_service.latest(
        "bank_customers",
    )

    assert latest is not None
    assert latest.metadata.version == "2.0.0"


# ==========================================================
# Navigation
# ==========================================================


def test_previous(
    version_service: ReportVersionService,
):

    previous = version_service.previous(
        "bank_customers",
        "2.0.0",
    )

    assert previous is not None
    assert previous.metadata.version == "1.1.0"


def test_previous_none(
    version_service: ReportVersionService,
):

    previous = version_service.previous(
        "bank_customers",
        "1.0.0",
    )

    assert previous is None


def test_next(
    version_service: ReportVersionService,
):

    nxt = version_service.next(
        "bank_customers",
        "1.1.0",
    )

    assert nxt is not None
    assert nxt.metadata.version == "2.0.0"


def test_next_none(
    version_service: ReportVersionService,
):

    nxt = version_service.next(
        "bank_customers",
        "2.0.0",
    )

    assert nxt is None


# ==========================================================
# Version Information
# ==========================================================


def test_latest_version(
    version_service: ReportVersionService,
):

    version = version_service.latest_version(
        "bank_customers",
    )

    assert version == "2.0.0"


def test_all_versions(
    version_service: ReportVersionService,
):

    versions = version_service.all_versions(
        "bank_customers",
    )

    assert versions == [
        "1.0.0",
        "1.1.0",
        "2.0.0",
    ]


def test_lineage(
    version_service: ReportVersionService,
):

    lineage = version_service.lineage(
        "bank_customers",
    )

    assert lineage == [
        "1.0.0",
        "1.1.0",
        "2.0.0",
    ]


# ==========================================================
# Comparison
# ==========================================================


def test_comparison_pair(
    version_service: ReportVersionService,
):

    previous, latest = (
        version_service.comparison_pair(
            "bank_customers",
        )
    )

    assert previous.metadata.version == "1.1.0"
    assert latest.metadata.version == "2.0.0"


def test_comparison_pair_none(
    version_service: ReportVersionService,
):

    pair = version_service.comparison_pair(
        "credit_risk",
    )

    assert pair is None


def test_has_multiple_versions_true(
    version_service: ReportVersionService,
):

    assert version_service.has_multiple_versions(
        "bank_customers",
    )


def test_has_multiple_versions_false(
    version_service: ReportVersionService,
):

    assert (
        not version_service.has_multiple_versions(
            "credit_risk",
        )
    )