from __future__ import annotations

from backend.models.html_report import HTMLReport
from backend.models.metadata import ReportMetadata
from backend.models.pdf_report import PDFReport
from backend.models.report_package import ReportPackage


# ============================================================
# Fixtures
# ============================================================


def create_package() -> ReportPackage:
    """
    Create a ReportPackage for testing.
    """

    metadata = ReportMetadata(
        title="Enterprise Report",
    )

    html_report = HTMLReport(
        title="Enterprise Report",
        html="<h1>InsightPilot AI</h1>",
    )

    pdf_report = PDFReport(
        title="Enterprise Report",
        file_path="reports/report.pdf",
    )

    package = ReportPackage(
        metadata=metadata,
        html_report=html_report,
        pdf_report=pdf_report,
        json_report_path="reports/report.json",
    )

    return package


# ============================================================
# Initialization
# ============================================================


def test_package_initialization() -> None:

    package = create_package()

    assert package.metadata.title == "Enterprise Report"

    assert package.html_report is not None

    assert package.pdf_report is not None

    assert package.json_report_path == "reports/report.json"


# ============================================================
# Helper Methods
# ============================================================


def test_has_html() -> None:

    package = create_package()

    assert package.has_html() is True


def test_has_pdf() -> None:

    package = create_package()

    assert package.has_pdf() is True


def test_has_json() -> None:

    package = create_package()

    assert package.has_json() is True


def test_empty_package_helpers() -> None:

    package = ReportPackage(
        metadata=ReportMetadata(),
    )

    assert package.has_html() is False

    assert package.has_pdf() is False

    assert package.has_json() is False


# ============================================================
# Available Formats
# ============================================================


def test_available_formats() -> None:

    package = create_package()

    formats = package.available_formats()

    assert formats == [
        "HTML",
        "PDF",
        "JSON",
    ]


def test_available_formats_empty() -> None:

    package = ReportPackage(
        metadata=ReportMetadata(),
    )

    assert package.available_formats() == []


# ============================================================
# Artifact Management
# ============================================================


def test_add_artifact() -> None:

    package = create_package()

    package.add_artifact(
        "manifest",
        "reports/manifest.json",
    )

    assert package.artifacts["manifest"] == "reports/manifest.json"


def test_get_artifact() -> None:

    package = create_package()

    package.add_artifact(
        "summary",
        "reports/summary.txt",
    )

    assert (
        package.get_artifact("summary")
        == "reports/summary.txt"
    )


def test_get_unknown_artifact() -> None:

    package = create_package()

    assert package.get_artifact("unknown") is None


# ============================================================
# Serialization
# ============================================================


def test_to_dict() -> None:

    package = create_package()

    data = package.to_dict()

    assert isinstance(data, dict)

    assert data["metadata"]["title"] == "Enterprise Report"

    assert data["json_report_path"] == "reports/report.json"

    assert "available_formats" in data


def test_to_dict_available_formats() -> None:

    package = create_package()

    data = package.to_dict()

    assert data["available_formats"] == [
        "HTML",
        "PDF",
        "JSON",
    ]


def test_created_at_serialized() -> None:

    package = create_package()

    data = package.to_dict()

    assert isinstance(
        data["created_at"],
        str,
    )


# ============================================================
# Metadata
# ============================================================


def test_metadata_extra() -> None:

    package = create_package()

    package.metadata_extra["project"] = "InsightPilot"

    assert (
        package.metadata_extra["project"]
        == "InsightPilot"
    )


# ============================================================
# Artifacts
# ============================================================


def test_multiple_artifacts() -> None:

    package = create_package()

    package.add_artifact(
        "manifest",
        "reports/manifest.json",
    )

    package.add_artifact(
        "archive",
        "reports/report.zip",
    )

    assert len(package.artifacts) == 2

    assert (
        package.get_artifact("archive")
        == "reports/report.zip"
    )