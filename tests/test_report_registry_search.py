from datetime import UTC, datetime, timedelta

from backend.models.metadata import ReportMetadata
from backend.models.report_package import ReportPackage
from backend.services.report_registry import ReportRegistry


def create_package(
    report_id: str,
    dataset: str,
    version: str = "0.9.0",
    formats: list[str] | None = None,
    generated_at: datetime | None = None,
) -> ReportPackage:

    if generated_at is None:
        generated_at = datetime.now(UTC)

    metadata = ReportMetadata(
        report_id=report_id,
        title=f"Report {report_id}",
        dataset_name=dataset,
        version=version,
        generated_at=generated_at,
    )

    package = ReportPackage(
        metadata=metadata,
        html_report=None,
        pdf_report=None,
        json_report_path=None,
    )

    if formats:
        if "HTML" in formats:
            package.html_report = object()

        if "PDF" in formats:
            package.pdf_report = "report.pdf"

        if "JSON" in formats:
            package.json_report_path = "report.json"

    return package


def test_find_by_dataset():

    registry = ReportRegistry()

    registry.register(
        create_package(
            "1",
            "bank_customers",
        )
    )

    registry.register(
        create_package(
            "2",
            "transactions",
        )
    )

    results = registry.find_by_dataset(
        "bank_customers"
    )

    assert len(results) == 1

    assert (
        results[0].metadata.dataset_name
        == "bank_customers"
    )


def test_find_by_version():

    registry = ReportRegistry()

    registry.register(
        create_package(
            "1",
            "bank",
            version="0.9.0",
        )
    )

    registry.register(
        create_package(
            "2",
            "bank",
            version="1.0.0",
        )
    )

    results = registry.find_by_version(
        "1.0.0"
    )

    assert len(results) == 1

    assert (
        results[0].metadata.version
        == "1.0.0"
    )


def test_find_by_format():

    registry = ReportRegistry()

    registry.register(
        create_package(
            "1",
            "bank",
            formats=["HTML"],
        )
    )

    registry.register(
        create_package(
            "2",
            "bank",
            formats=["PDF"],
        )
    )

    results = registry.find_by_format(
        "PDF"
    )

    assert len(results) == 1

    assert (
        results[0].metadata.report_id
        == "2"
    )


def test_find_by_date_range():

    registry = ReportRegistry()

    now = datetime.now(UTC)

    registry.register(
        create_package(
            "1",
            "bank",
            generated_at=now - timedelta(days=5),
        )
    )

    registry.register(
        create_package(
            "2",
            "bank",
            generated_at=now,
        )
    )

    results = registry.find_by_date_range(
        (now - timedelta(days=1)).isoformat(),
        (now + timedelta(days=1)).isoformat(),
    )

    assert len(results) == 1

    assert (
        results[0].metadata.report_id
        == "2"
    )


def test_list_sorted():

    registry = ReportRegistry()

    now = datetime.now(UTC)

    registry.register(
        create_package(
            "old",
            "bank",
            generated_at=now - timedelta(days=2),
        )
    )

    registry.register(
        create_package(
            "new",
            "bank",
            generated_at=now,
        )
    )

    reports = registry.list_sorted()

    assert reports[0].metadata.report_id == "new"

    assert reports[1].metadata.report_id == "old"


def test_find_returns_empty():

    registry = ReportRegistry()

    assert registry.find_by_dataset(
        "missing"
    ) == []

    assert registry.find_by_version(
        "9.9.9"
    ) == []

    assert registry.find_by_format(
        "PDF"
    ) == []