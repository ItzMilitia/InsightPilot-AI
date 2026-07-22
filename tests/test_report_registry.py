import pytest

from backend.models.report_package import ReportPackage
from backend.services.report_registry import ReportRegistry

# Import the actual metadata model used in your project.
# If your metadata model has a different name, update this import.
from backend.models.metadata import ReportMetadata


def create_package(report_id: str) -> ReportPackage:
    metadata = ReportMetadata(
        report_id=report_id,
        title="Test Report",
        version="0.9.0",
    )

    return ReportPackage(
        metadata=metadata,
        html_report=None,
        pdf_report=None,
        json_report_path=None,
    )


def test_register_report():

    registry = ReportRegistry()

    package = create_package("report-001")

    registry.register(package)

    assert registry.count() == 1

    assert registry.exists("report-001")


def test_get_registered_report():

    registry = ReportRegistry()

    package = create_package("report-001")

    registry.register(package)

    result = registry.get("report-001")

    assert result is package


def test_duplicate_registration_raises():

    registry = ReportRegistry()

    package = create_package("report-001")

    registry.register(package)

    with pytest.raises(ValueError):
        registry.register(package)


def test_missing_report_raises():

    registry = ReportRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_delete_report():

    registry = ReportRegistry()

    package = create_package("report-001")

    registry.register(package)

    assert registry.delete("report-001") is True

    assert registry.count() == 0

    assert not registry.exists("report-001")


def test_delete_unknown_report():

    registry = ReportRegistry()

    assert registry.delete("unknown") is False


def test_list_reports():

    registry = ReportRegistry()

    registry.register(create_package("report-001"))

    registry.register(create_package("report-002"))

    reports = registry.list()

    assert len(reports) == 2


def test_clear_registry():

    registry = ReportRegistry()

    registry.register(create_package("report-001"))

    registry.register(create_package("report-002"))

    registry.clear()

    assert registry.count() == 0

    assert registry.list() == []