from __future__ import annotations

import json

import pytest

from backend.models.validation_result import ValidationResult
from backend.services.report_validation_service import (
    ReportValidationService,
)


# ==========================================================
# Fixtures
# ==========================================================


@pytest.fixture
def service() -> ReportValidationService:
    return ReportValidationService()


@pytest.fixture
def valid_report_directory(tmp_path):
    """
    Creates a fully valid persisted report directory.
    """

    directory = tmp_path / "reports"

    directory.mkdir()

    (directory / "report.html").write_text(
        "<html>Report</html>",
        encoding="utf-8",
    )

    (directory / "report.pdf").write_text(
        "dummy pdf",
        encoding="utf-8",
    )

    (directory / "report.json").write_text(
        "{}",
        encoding="utf-8",
    )

    manifest = {
        "metadata": {
            "report_id": "123",
            "title": "Test Report",
            "version": "0.9.0",
            "generated_at": "2026-01-01T00:00:00Z",
        },
        "formats": [
            "HTML",
            "PDF",
            "JSON",
        ],
        "artifacts": {
            "html": "report.html",
            "pdf": "report.pdf",
            "json": "report.json",
        },
    }

    (directory / "manifest.json").write_text(
        json.dumps(
            manifest,
            indent=4,
        ),
        encoding="utf-8",
    )

    return directory


# ==========================================================
# Successful Validation
# ==========================================================


def test_validate_valid_report(
    service,
    valid_report_directory,
):

    result = service.validate(
        valid_report_directory,
    )

    assert isinstance(
        result,
        ValidationResult,
    )

    assert result.is_valid

    assert result.error_count() == 0

    assert result.errors == []


# ==========================================================
# Directory Validation
# ==========================================================


def test_missing_directory(
    service,
    tmp_path,
):

    result = service.validate(
        tmp_path / "missing",
    )

    assert not result.is_valid

    assert result.has_errors()


def test_not_a_directory(
    service,
    tmp_path,
):

    file = tmp_path / "report.txt"

    file.write_text(
        "test",
        encoding="utf-8",
    )

    result = service.validate(
        file,
    )

    assert not result.is_valid

    assert result.has_errors()


def test_empty_directory(
    service,
    tmp_path,
):

    directory = tmp_path / "reports"

    directory.mkdir()

    result = service.validate(
        directory,
    )

    assert not result.is_valid

    assert result.has_errors()


# ==========================================================
# Manifest Validation
# ==========================================================


def test_missing_manifest(
    service,
    tmp_path,
):

    directory = tmp_path / "reports"

    directory.mkdir()

    result = service.validate(
        directory,
    )

    assert not result.is_valid

    assert result.has_errors()


def test_invalid_manifest_json(
    service,
    tmp_path,
):

    directory = tmp_path / "reports"

    directory.mkdir()

    (directory / "manifest.json").write_text(
        "{invalid json",
        encoding="utf-8",
    )

    result = service.validate(
        directory,
    )

    assert not result.is_valid

    assert result.has_errors()


def test_missing_manifest_metadata(
    service,
    valid_report_directory,
):

    manifest = {
        "formats": [],
        "artifacts": {},
    }

    (
        valid_report_directory / "manifest.json"
    ).write_text(
        json.dumps(
            manifest,
        ),
        encoding="utf-8",
    )

    result = service.validate(
        valid_report_directory,
    )

    assert not result.is_valid


def test_missing_manifest_formats(
    service,
    valid_report_directory,
):

    manifest = {
        "metadata": {},
        "artifacts": {},
    }

    (
        valid_report_directory / "manifest.json"
    ).write_text(
        json.dumps(
            manifest,
        ),
        encoding="utf-8",
    )

    result = service.validate(
        valid_report_directory,
    )

    assert not result.is_valid


def test_missing_manifest_artifacts(
    service,
    valid_report_directory,
):

    manifest = {
        "metadata": {},
        "formats": [],
    }

    (
        valid_report_directory / "manifest.json"
    ).write_text(
        json.dumps(
            manifest,
        ),
        encoding="utf-8",
    )

    result = service.validate(
        valid_report_directory,
    )

    assert not result.is_valid


# ==========================================================
# Metadata Validation
# ==========================================================


@pytest.mark.parametrize(
    "field",
    [
        "report_id",
        "title",
        "version",
        "generated_at",
    ],
)
def test_missing_required_metadata(
    service,
    valid_report_directory,
    field,
):

    manifest_path = (
        valid_report_directory
        / "manifest.json"
    )

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )

    del manifest["metadata"][field]

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=4,
        ),
        encoding="utf-8",
    )

    result = service.validate(
        valid_report_directory,
    )

    assert not result.is_valid


# ==========================================================
# Format Validation
# ==========================================================


def test_unknown_format(
    service,
    valid_report_directory,
):

    manifest_path = (
        valid_report_directory
        / "manifest.json"
    )

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )

    manifest["formats"].append(
        "CSV"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=4,
        ),
        encoding="utf-8",
    )

    result = service.validate(
        valid_report_directory,
    )

    assert not result.is_valid


def test_missing_artifact_mapping(
    service,
    valid_report_directory,
):

    manifest_path = (
        valid_report_directory
        / "manifest.json"
    )

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )

    del manifest["artifacts"]["pdf"]

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=4,
        ),
        encoding="utf-8",
    )

    result = service.validate(
        valid_report_directory,
    )

    assert not result.is_valid


# ==========================================================
# Artifact Validation
# ==========================================================


@pytest.mark.parametrize(
    "filename",
    [
        "report.html",
        "report.pdf",
        "report.json",
    ],
)
def test_missing_artifact_file(
    service,
    valid_report_directory,
    filename,
):

    (
        valid_report_directory
        / filename
    ).unlink()

    result = service.validate(
        valid_report_directory,
    )

    assert not result.is_valid


# ==========================================================
# Multiple Errors
# ==========================================================


def test_multiple_validation_errors(
    service,
    valid_report_directory,
):

    (
        valid_report_directory
        / "report.pdf"
    ).unlink()

    (
        valid_report_directory
        / "report.json"
    ).unlink()

    manifest_path = (
        valid_report_directory
        / "manifest.json"
    )

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8",
        )
    )

    del manifest["metadata"]["title"]

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=4,
        ),
        encoding="utf-8",
    )

    result = service.validate(
        valid_report_directory,
    )

    assert not result.is_valid

    assert result.error_count() >= 3


# ==========================================================
# ValidationResult Helpers
# ==========================================================


def test_validation_result_has_errors(
    service,
    tmp_path,
):

    result = service.validate(
        tmp_path / "missing",
    )

    assert result.has_errors()


def test_validation_result_error_count(
    service,
    tmp_path,
):

    result = service.validate(
        tmp_path / "missing",
    )

    assert result.error_count() > 0