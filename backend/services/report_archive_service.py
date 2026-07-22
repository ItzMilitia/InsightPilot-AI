from __future__ import annotations

"""
Enterprise Report Archive Service.

Responsible for packaging persisted report artifacts into a
single distributable ZIP archive.

Responsibilities
----------------
- Validate report directory
- Validate manifest existence
- Collect report artifacts
- Create ZIP archive
- Preserve relative file names
- Return generated archive path

This service DOES NOT generate reports.
It archives artifacts already produced by ReportStorageService.
"""

from pathlib import Path
import zipfile


class ReportArchiveService:
    """
    Service responsible for archiving report artifacts.
    """

    MANIFEST_FILENAME = "manifest.json"

    DEFAULT_ARCHIVE_NAME = "report_archive.zip"

    def archive(
        self,
        report_directory: str | Path,
        archive_path: str | Path | None = None,
    ) -> Path:
        """
        Create a ZIP archive containing all report artifacts.

        Parameters
        ----------
        report_directory:
            Directory containing report artifacts.

        archive_path:
            Optional custom archive output path.

        Returns
        -------
        Path
            Generated archive path.
        """

        report_directory = Path(report_directory)

        self._validate_directory(report_directory)

        self._validate_manifest(report_directory)

        archive_path = self._default_archive_path(
            report_directory,
            archive_path,
        )

        artifacts = self._collect_artifacts(
            report_directory,
        )

        self._create_archive(
            artifacts,
            archive_path,
        )

        return archive_path

    # ======================================================
    # Validation
    # ======================================================

    def _validate_directory(
        self,
        directory: Path,
    ) -> None:
        """
        Validate report directory.
        """

        if not directory.exists():
            raise FileNotFoundError(
                f"Report directory does not exist: {directory}"
            )

        if not directory.is_dir():
            raise NotADirectoryError(
                f"Expected directory: {directory}"
            )

    def _validate_manifest(
        self,
        directory: Path,
    ) -> None:
        """
        Ensure manifest.json exists.
        """

        manifest = directory / self.MANIFEST_FILENAME

        if not manifest.exists():
            raise FileNotFoundError(
                "manifest.json not found."
            )

    # ======================================================
    # Artifact Collection
    # ======================================================

    def _collect_artifacts(
        self,
        directory: Path,
    ) -> list[Path]:
        """
        Collect all report artifacts.

        Excludes existing ZIP archives.
        """

        artifacts: list[Path] = []

        for path in sorted(directory.iterdir()):

            if not path.is_file():
                continue

            if path.suffix.lower() == ".zip":
                continue

            artifacts.append(path)

        return artifacts

    # ======================================================
    # Archive Creation
    # ======================================================

    def _create_archive(
        self,
        artifacts: list[Path],
        archive_path: Path,
    ) -> None:
        """
        Build ZIP archive.

        Existing archives are overwritten.
        """

        archive_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with zipfile.ZipFile(
            archive_path,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:

            for artifact in artifacts:

                archive.write(
                    artifact,
                    arcname=artifact.name,
                )

    # ======================================================
    # Helpers
    # ======================================================

    def _default_archive_path(
        self,
        report_directory: Path,
        archive_path: str | Path | None,
    ) -> Path:
        """
        Resolve archive output path.
        """

        if archive_path is None:

            return (
                report_directory
                / self.DEFAULT_ARCHIVE_NAME
            )

        return Path(archive_path)