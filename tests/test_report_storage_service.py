from __future__ import annotations

import json

import pytest

from backend.models.html_report import HTMLReport
from backend.models.metadata import ReportMetadata
from backend.models.pdf_report import PDFReport
from backend.models.report_package import ReportPackage
from backend.services.report_storage_service import (
    ReportStorageService,
)


# ==========================================================
# Fixtures
# ==========================================================


@pytest.fixture
def service() -> ReportStorageService:
    return ReportStorageService()


@pytest.fixture
def metadata() -> ReportMetadata:
    return ReportMetadata(
        title="Test Report",
        dataset_name="bank_customers.csv",
    )


@pytest.fixture
def html_report() -> HTMLReport:
    return HTMLReport(
        title="Test Report",
        html="<html><body><h1>InsightPilot</h1></body></html>",
    )


@pytest.fixture
def package(
    tmp_path,
    metadata,
    html_report,
) -> ReportPackage:

    pdf_file = tmp_path / "source.pdf"
    pdf_file.write_text(
        "dummy pdf",
        encoding="utf-8",
    )

    json_file = tmp_path / "source.json"
    json_file.write_text(
        '{"status":"ok"}',
        encoding="utf-8",
    )

    pdf_report = PDFReport(
        title="PDF Report",
        file_path=str(pdf_file),
    )

    return ReportPackage(
        metadata=metadata,
        html_report=html_report,
        pdf_report=pdf_report,
        json_report_path=str(json_file),
    )


# ==========================================================
# Save
# ==========================================================


def test_save_returns_package(
    service,
    package,
    tmp_path,
):

    result = service.save(
        package,
        tmp_path / "reports",
    )

    assert result is package


def test_output_directory_created(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    assert output.exists()
    assert output.is_dir()


# ==========================================================
# HTML
# ==========================================================


def test_html_report_saved(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    html = output / "report.html"

    assert html.exists()

    assert (
        html.read_text(encoding="utf-8")
        == package.html_report.html
    )


# ==========================================================
# PDF
# ==========================================================


def test_pdf_report_copied(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    pdf = output / "report.pdf"

    assert pdf.exists()

    assert pdf.read_text(
        encoding="utf-8"
    ) == "dummy pdf"


# ==========================================================
# JSON
# ==========================================================


def test_json_report_copied(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    report = output / "report.json"

    assert report.exists()

    data = json.loads(
        report.read_text(
            encoding="utf-8"
        )
    )

    assert data["status"] == "ok"


# ==========================================================
# Manifest
# ==========================================================


def test_manifest_created(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    manifest = output / "manifest.json"

    assert manifest.exists()


def test_manifest_contains_metadata(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    manifest = json.loads(
        (
            output / "manifest.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert manifest["metadata"]["title"] == "Test Report"

    assert (
        manifest["metadata"]["dataset_name"]
        == "bank_customers.csv"
    )


def test_manifest_contains_formats(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    manifest = json.loads(
        (
            output / "manifest.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert "HTML" in manifest["formats"]

    assert "PDF" in manifest["formats"]

    assert "JSON" in manifest["formats"]


def test_manifest_contains_artifacts(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    manifest = json.loads(
        (
            output / "manifest.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    artifacts = manifest["artifacts"]

    assert "html" in artifacts

    assert "pdf" in artifacts

    assert "json" in artifacts


# ==========================================================
# Artifacts
# ==========================================================


def test_package_artifacts_updated(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    result = service.save(
        package,
        output,
    )

    assert result.get_artifact("html")

    assert result.get_artifact("pdf")

    assert result.get_artifact("json")


def test_artifact_paths_exist(
    service,
    package,
    tmp_path,
):

    output = tmp_path / "reports"

    result = service.save(
        package,
        output,
    )

    assert result.get_artifact("html") is not None

    assert result.get_artifact("pdf") is not None

    assert result.get_artifact("json") is not None


# ==========================================================
# Edge Cases
# ==========================================================


def test_save_without_pdf(
    service,
    metadata,
    html_report,
    tmp_path,
):

    package = ReportPackage(
        metadata=metadata,
        html_report=html_report,
    )

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    assert (output / "report.html").exists()

    assert not (output / "report.pdf").exists()


def test_save_without_json(
    service,
    metadata,
    html_report,
    tmp_path,
):

    pdf = tmp_path / "input.pdf"

    pdf.write_text(
        "pdf",
        encoding="utf-8",
    )

    package = ReportPackage(
        metadata=metadata,
        html_report=html_report,
        pdf_report=PDFReport(
            title="PDF",
            file_path=str(pdf),
        ),
    )

    output = tmp_path / "reports"

    service.save(
        package,
        output,
    )

    assert (output / "report.pdf").exists()

    assert not (output / "report.json").exists()


def test_save_none_package(
    service,
    tmp_path,
):

    with pytest.raises(ValueError):

        service.save(
            None,
            tmp_path,
        )