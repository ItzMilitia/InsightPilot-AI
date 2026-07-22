from datetime import UTC, datetime

from backend.models.metadata import ReportMetadata
from backend.models.report_package import ReportPackage
from backend.services.report_registry import ReportRegistry


def create_package(
    report_id: str,
    dataset: str,
    version: str,
) -> ReportPackage:

    metadata = ReportMetadata(
        report_id=report_id,
        title="History Test",
        dataset_name=dataset,
        version=version,
        generated_at=datetime.now(UTC),
    )

    return ReportPackage(
        metadata=metadata,
        html_report=None,
        pdf_report=None,
        json_report_path=None,
    )


def test_history_registration():

    registry = ReportRegistry()

    registry.register(
        create_package("1", "bank", "1.0")
    )

    registry.register(
        create_package("2", "bank", "1.1")
    )

    assert registry.history_count("bank") == 2


def test_get_latest():

    registry = ReportRegistry()

    registry.register(
        create_package("1", "bank", "1.0")
    )

    registry.register(
        create_package("2", "bank", "2.0")
    )

    latest = registry.get_latest("bank")

    assert latest is not None
    assert latest.metadata.version == "2.0"


def test_get_versions():

    registry = ReportRegistry()

    registry.register(
        create_package("1", "bank", "1.0")
    )

    registry.register(
        create_package("2", "bank", "1.1")
    )

    registry.register(
        create_package("3", "bank", "2.0")
    )

    assert registry.get_versions("bank") == [
        "1.0",
        "1.1",
        "2.0",
    ]


def test_has_history():

    registry = ReportRegistry()

    assert not registry.has_history("bank")

    registry.register(
        create_package("1", "bank", "1.0")
    )

    assert registry.has_history("bank")


def test_delete_updates_history():

    registry = ReportRegistry()

    package = create_package(
        "1",
        "bank",
        "1.0",
    )

    registry.register(package)

    registry.delete(
        package.metadata.report_id,
    )

    assert not registry.has_history("bank")


def test_clear_updates_history():

    registry = ReportRegistry()

    registry.register(
        create_package("1", "bank", "1.0")
    )

    registry.clear()

    assert registry.history_count("bank") == 0