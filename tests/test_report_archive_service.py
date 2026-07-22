from __future__ import annotations

import zipfile

import pytest

from backend.services.report_archive_service import (
    ReportArchiveService,
)


# ==========================================================
# Fixtures
# ==========================================================


@pytest.fixture
def service() -> ReportArchiveService:
    return ReportArchiveService()


@pytest.fixture
def report_directory(tmp_path):
    """
    Creates a report directory containing all
    standard report artifacts.
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
        '{"status":"ok"}',
        encoding="utf-8",
    )

    (directory / "manifest.json").write_text(
        '{"version":"0.9"}',
        encoding="utf-8",
    )

    return directory


# ==========================================================
# Archive Creation
# ==========================================================


def test_archive_created(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    assert archive.exists()

    assert archive.is_file()

    assert archive.suffix == ".zip"


def test_default_archive_name(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    assert (
        archive.name
        == "report_archive.zip"
    )


def test_custom_archive_path(
    service,
    report_directory,
    tmp_path,
):

    custom = (
        tmp_path
        / "custom.zip"
    )

    archive = service.archive(
        report_directory,
        custom,
    )

    assert archive == custom

    assert custom.exists()


# ==========================================================
# ZIP Contents
# ==========================================================


def test_archive_contains_manifest(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        assert (
            "manifest.json"
            in zip_file.namelist()
        )


def test_archive_contains_html(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        assert (
            "report.html"
            in zip_file.namelist()
        )


def test_archive_contains_pdf(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        assert (
            "report.pdf"
            in zip_file.namelist()
        )


def test_archive_contains_json(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        assert (
            "report.json"
            in zip_file.namelist()
        )


# ==========================================================
# Optional Files
# ==========================================================


def test_archive_without_pdf(
    service,
    tmp_path,
):

    directory = tmp_path / "reports"

    directory.mkdir()

    (directory / "report.html").write_text(
        "html",
        encoding="utf-8",
    )

    (directory / "manifest.json").write_text(
        "{}",
        encoding="utf-8",
    )

    archive = service.archive(
        directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        names = zip_file.namelist()

        assert "report.html" in names

        assert "manifest.json" in names

        assert "report.pdf" not in names


def test_archive_without_json(
    service,
    tmp_path,
):

    directory = tmp_path / "reports"

    directory.mkdir()

    (directory / "report.html").write_text(
        "html",
        encoding="utf-8",
    )

    (directory / "report.pdf").write_text(
        "pdf",
        encoding="utf-8",
    )

    (directory / "manifest.json").write_text(
        "{}",
        encoding="utf-8",
    )

    archive = service.archive(
        directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        names = zip_file.namelist()

        assert "report.pdf" in names

        assert "report.json" not in names


# ==========================================================
# Validation
# ==========================================================


def test_missing_report_directory(
    service,
    tmp_path,
):

    missing = (
        tmp_path
        / "missing"
    )

    with pytest.raises(
        FileNotFoundError
    ):

        service.archive(
            missing,
        )


def test_missing_manifest(
    service,
    tmp_path,
):

    directory = (
        tmp_path
        / "reports"
    )

    directory.mkdir()

    (directory / "report.html").write_text(
        "html",
        encoding="utf-8",
    )

    with pytest.raises(
        FileNotFoundError
    ):

        service.archive(
            directory,
        )


def test_directory_is_not_folder(
    service,
    tmp_path,
):

    file = (
        tmp_path
        / "report.txt"
    )

    file.write_text(
        "test",
        encoding="utf-8",
    )

    with pytest.raises(
        NotADirectoryError
    ):

        service.archive(
            file,
        )


# ==========================================================
# Existing Archive
# ==========================================================


def test_existing_archive_overwritten(
    service,
    report_directory,
):

    archive = (
        report_directory
        / "report_archive.zip"
    )

    archive.write_text(
        "old archive",
        encoding="utf-8",
    )

    service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        assert (
            "manifest.json"
            in zip_file.namelist()
        )


# ==========================================================
# ZIP Integrity
# ==========================================================


def test_archive_is_valid_zip(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        assert (
            zip_file.testzip()
            is None
        )


def test_archive_preserves_relative_names(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        for name in zip_file.namelist():

            assert "/" not in name
            assert "\\" not in name


# ==========================================================
# Internal Collection
# ==========================================================


def test_existing_zip_not_rearchived(
    service,
    report_directory,
):

    existing = (
        report_directory
        / "old.zip"
    )

    existing.write_text(
        "old",
        encoding="utf-8",
    )

    archive = service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        assert (
            "old.zip"
            not in zip_file.namelist()
        )


def test_archive_contains_expected_file_count(
    service,
    report_directory,
):

    archive = service.archive(
        report_directory,
    )

    with zipfile.ZipFile(
        archive,
        "r",
    ) as zip_file:

        assert len(
            zip_file.namelist()
        ) == 4