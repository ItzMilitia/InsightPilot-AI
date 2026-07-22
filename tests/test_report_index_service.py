from __future__ import annotations

import json

import pytest

from backend.models.report_index import (
    ReportIndexEntry,
)
from backend.services.report_index_service import (
    ReportIndexService,
)


# ==========================================================
# Fixtures
# ==========================================================


@pytest.fixture
def index_file(tmp_path):
    return tmp_path / "report_index.json"


@pytest.fixture
def service(index_file):
    return ReportIndexService(
        index_path=index_file,
    )


@pytest.fixture
def sample_entry():
    return ReportIndexEntry(
        report_id="report-001",
        title="Customer Quality Report",
        dataset_name="bank_customers.csv",
        version="0.9.0",
        generated_at="2026-07-23T12:00:00Z",
        directory="reports/report-001",
        archive_path="reports/report-001.zip",
        formats=[
            "HTML",
            "PDF",
            "JSON",
        ],
    )


# ==========================================================
# Initial State
# ==========================================================


def test_empty_index(
    service,
):
    index = service.load()

    assert index.is_empty()
    assert index.count() == 0


# ==========================================================
# Registration
# ==========================================================


def test_register_report(
    service,
    sample_entry,
):
    service.register(sample_entry)

    reports = service.all_reports()

    assert len(reports) == 1
    assert reports[0].report_id == "report-001"


def test_duplicate_registration_is_ignored(
    service,
    sample_entry,
):
    service.register(sample_entry)
    service.register(sample_entry)

    reports = service.all_reports()

    assert len(reports) == 1


# ==========================================================
# Persistence
# ==========================================================


def test_save_and_reload(
    service,
    sample_entry,
):
    service.register(sample_entry)

    new_service = ReportIndexService(
        index_path=service.index_path,
    )

    reports = new_service.all_reports()

    assert len(reports) == 1
    assert reports[0].title == sample_entry.title


def test_index_file_created(
    service,
    sample_entry,
):
    service.register(sample_entry)

    assert service.index_path.exists()


def test_index_file_contains_json(
    service,
    sample_entry,
):
    service.register(sample_entry)

    with service.index_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    assert "entries" in data


# ==========================================================
# Search
# ==========================================================


def test_find_by_report_id(
    service,
    sample_entry,
):
    service.register(sample_entry)

    report = service.find_by_report_id(
        "report-001"
    )

    assert report is not None
    assert report.title == sample_entry.title


def test_find_missing_report(
    service,
):
    report = service.find_by_report_id(
        "missing"
    )

    assert report is None


def test_find_by_dataset(
    service,
    sample_entry,
):
    service.register(sample_entry)

    reports = service.find_by_dataset(
        "bank_customers.csv"
    )

    assert len(reports) == 1


def test_find_by_unknown_dataset(
    service,
):
    reports = service.find_by_dataset(
        "unknown.csv"
    )

    assert reports == []


def test_find_by_version(
    service,
    sample_entry,
):
    service.register(sample_entry)

    reports = service.find_by_version(
        "0.9.0"
    )

    assert len(reports) == 1


def test_find_unknown_version(
    service,
):
    reports = service.find_by_version(
        "2.0.0"
    )

    assert reports == []


# ==========================================================
# Multiple Reports
# ==========================================================


def test_multiple_reports(
    service,
):
    for i in range(5):

        service.register(
            ReportIndexEntry(
                report_id=f"id-{i}",
                title=f"Report {i}",
                dataset_name=f"dataset-{i}.csv",
                version="0.9.0",
                generated_at="2026-07-23",
                directory=f"reports/{i}",
                archive_path=None,
                formats=["HTML"],
            )
        )

    reports = service.all_reports()

    assert len(reports) == 5


# ==========================================================
# Clear
# ==========================================================


def test_clear_index(
    service,
    sample_entry,
):
    service.register(sample_entry)

    service.clear()

    reports = service.all_reports()

    assert reports == []


# ==========================================================
# Reload After Clear
# ==========================================================


def test_reload_after_clear(
    service,
    sample_entry,
):
    service.register(sample_entry)

    service.clear()

    new_service = ReportIndexService(
        index_path=service.index_path,
    )

    assert new_service.all_reports() == []