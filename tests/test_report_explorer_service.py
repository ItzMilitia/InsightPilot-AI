"""
Unit tests for ReportExplorerService.

Sprint 9.3
Phase 1:
- Fixtures
- Helper builders
- Constructor tests
- Property tests
"""

from __future__ import annotations

from datetime import datetime

import pytest

from backend.models.html_report import HTMLReport
from backend.models.metadata import ReportMetadata
from backend.models.report_package import ReportPackage
from backend.services.report_explorer_service import ReportExplorerService
from backend.services.report_history_service import ReportHistoryService
from backend.services.report_version_service import ReportVersionService


# ======================================================
# Helpers
# ======================================================

def create_report(
    report_id: str,
    dataset_name: str,
    version: str,
    title: str,
) -> ReportPackage:
    """
    Build a minimal ReportPackage for testing.
    """

    metadata = ReportMetadata(
        report_id=report_id,
        dataset_name=dataset_name,
        version=version,
        title=title,
        generated_at=datetime.now(),
    )

    html_report = HTMLReport(
        title=title,
        html="<html></html>",
    )

    return ReportPackage(
        metadata=metadata,
        html_report=html_report,
    )


# ======================================================
# Fixtures
# ======================================================

@pytest.fixture
def history_service() -> ReportHistoryService:
    """
    Create an empty history service.
    """

    return ReportHistoryService()


@pytest.fixture
def version_service(
    history_service: ReportHistoryService,
) -> ReportVersionService:
    """
    Create a version service.
    """

    return ReportVersionService(
        history_service=history_service,
    )


@pytest.fixture
def explorer(
    history_service: ReportHistoryService,
    version_service: ReportVersionService,
) -> ReportExplorerService:
    """
    Create explorer using injected services.
    """

    return ReportExplorerService(
        history_service=history_service,
        version_service=version_service,
    )


# ======================================================
# Constructor
# ======================================================

def test_default_constructor():
    """
    Explorer should create default services.
    """

    explorer = ReportExplorerService()

    assert isinstance(
        explorer.history_service,
        ReportHistoryService,
    )

    assert isinstance(
        explorer.version_service,
        ReportVersionService,
    )


def test_constructor_with_dependencies(
    history_service: ReportHistoryService,
    version_service: ReportVersionService,
):
    """
    Explorer should use injected dependencies.
    """

    explorer = ReportExplorerService(
        history_service=history_service,
        version_service=version_service,
    )

    assert explorer.history_service is history_service
    assert explorer.version_service is version_service


# ======================================================
# Properties
# ======================================================

def test_history_service_property(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    history_service property should expose
    injected service.
    """

    assert explorer.history_service is history_service


def test_version_service_property(
    explorer: ReportExplorerService,
    version_service: ReportVersionService,
):
    """
    version_service property should expose
    injected service.
    """

    assert explorer.version_service is version_service

# ======================================================
# Browsing APIs
# ======================================================

def test_list_reports(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    list_reports() should return all registered reports.
    """

    report1 = create_report(
        "RPT-001",
        "bank_customers",
        "1.0",
        "Quality Report",
    )

    report2 = create_report(
        "RPT-002",
        "loan_portfolio",
        "1.0",
        "Loan Report",
    )

    history_service.registry.register(report1)
    history_service.registry.register(report2)

    reports = explorer.list_reports()

    assert len(reports) == 2
    assert report1 in reports
    assert report2 in reports


def test_datasets(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    datasets() should return unique dataset names.
    """

    history_service.registry.register(
        create_report(
            "RPT-001",
            "bank_customers",
            "1.0",
            "Report A",
        )
    )

    history_service.registry.register(
        create_report(
            "RPT-002",
            "bank_customers",
            "1.1",
            "Report B",
        )
    )

    history_service.registry.register(
        create_report(
            "RPT-003",
            "loan_portfolio",
            "1.0",
            "Report C",
        )
    )

    datasets = explorer.datasets()

    assert datasets == [
        "bank_customers",
        "loan_portfolio",
    ]


def test_versions(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    versions() should return dataset versions.
    """

    history_service.registry.register(
        create_report(
            "RPT-001",
            "bank_customers",
            "1.0",
            "Report A",
        )
    )

    history_service.registry.register(
        create_report(
            "RPT-002",
            "bank_customers",
            "2.0",
            "Report B",
        )
    )

    versions = explorer.versions(
        "bank_customers",
    )

    assert versions == [
        "1.0",
        "2.0",
    ]


def test_latest(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    latest() should return newest report.
    """

    report1 = create_report(
        "RPT-001",
        "bank_customers",
        "1.0",
        "Report A",
    )

    report2 = create_report(
        "RPT-002",
        "bank_customers",
        "2.0",
        "Report B",
    )

    history_service.registry.register(report1)
    history_service.registry.register(report2)

    latest = explorer.latest(
        "bank_customers",
    )

    assert latest is report2


# ======================================================
# Filtering APIs
# ======================================================

def test_filter_by_dataset(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    filter_by_dataset() should return matching reports.
    """

    report = create_report(
        "RPT-001",
        "bank_customers",
        "1.0",
        "Report",
    )

    history_service.registry.register(report)

    results = explorer.filter_by_dataset(
        "bank_customers",
    )

    assert len(results) == 1
    assert results[0] is report


def test_filter_by_version(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    filter_by_version() should return matching reports.
    """

    report = create_report(
        "RPT-001",
        "bank_customers",
        "2.0",
        "Report",
    )

    history_service.registry.register(report)

    results = explorer.filter_by_version(
        "2.0",
    )

    assert len(results) == 1
    assert results[0] is report


def test_filter_by_date_range(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    filter_by_date_range() should return reports
    within the requested range.
    """

    report = create_report(
        "RPT-001",
        "bank_customers",
        "1.0",
        "Report",
    )

    history_service.registry.register(report)

    results = explorer.filter_by_date_range(
        datetime(2000, 1, 1),
        datetime(2100, 1, 1),
    )

    assert report in results

# ======================================================
# Search APIs
# ======================================================

def test_search_by_dataset(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    search() should find reports by dataset name.
    """

    report = create_report(
        "RPT-001",
        "bank_customers",
        "1.0",
        "Quality Report",
    )

    history_service.registry.register(report)

    results = explorer.search("bank")

    assert len(results) == 1
    assert results[0] is report


def test_search_case_insensitive(
    explorer: ReportExplorerService,
    history_service: ReportHistoryService,
):
    """
    search() should ignore case.
    """

    report = create_report(
        "RPT-001",
        "Bank_Customers",
        "1.0",
        "Quality Report",
    )

    history_service.registry.register(report)

    results = explorer.search("bank_customers")

    assert len(results) == 1
    assert results[0] is report


def test_search_no_matches(
    explorer: ReportExplorerService,
):
    """
    search() should return an empty list when
    nothing matches.
    """

    assert explorer.search("unknown_dataset") == []


# ======================================================
# Sorting APIs
# ======================================================

def test_sort_reports_by_title(
    explorer: ReportExplorerService,
):
    """
    Reports should be sorted alphabetically by title.
    """

    report_a = create_report(
        "RPT-001",
        "bank",
        "1.0",
        "B Report",
    )

    report_b = create_report(
        "RPT-002",
        "bank",
        "1.0",
        "A Report",
    )

    reports = explorer.sort_reports(
        [report_a, report_b],
        sort_by="title",
        descending=False,
    )

    assert reports[0] is report_b
    assert reports[1] is report_a


def test_sort_reports_invalid_field(
    explorer: ReportExplorerService,
):
    """
    Unsupported sort fields should raise ValueError.
    """

    with pytest.raises(ValueError):
        explorer.sort_reports(
            [],
            sort_by="invalid_field",
        )