from __future__ import annotations

import json
import shutil
from pathlib import Path

from backend.models.report_package import ReportPackage


class ReportStorageService:
    """
    Enterprise service responsible for persisting report artifacts.

    Responsibilities
    ----------------
    - Create output directory
    - Persist HTML report
    - Copy/Register PDF report
    - Copy/Register JSON report
    - Generate manifest.json
    - Update ReportPackage artifacts

    This service DOES NOT generate reports.
    It only stores artifacts produced by report engines.
    """

    HTML_FILENAME = "report.html"
    PDF_FILENAME = "report.pdf"
    JSON_FILENAME = "report.json"
    MANIFEST_FILENAME = "manifest.json"

    def save(
        self,
        package: ReportPackage,
        output_directory: str | Path,
    ) -> ReportPackage:
        """
        Persist all available report artifacts.

        Parameters
        ----------
        package:
            Generated report package.

        output_directory:
            Directory where reports should be stored.

        Returns
        -------
        ReportPackage
            Updated package with persisted artifact paths.
        """

        self._validate_package(package)

        output_dir = Path(output_directory)

        self._prepare_directory(output_dir)

        if package.html_report is not None:
            html_path = self._save_html(
                package,
                output_dir,
            )

            package.add_artifact(
                "html",
                str(html_path),
            )

        if package.pdf_report is not None:
            pdf_path = self._copy_pdf(
                package,
                output_dir,
            )

            package.add_artifact(
                "pdf",
                str(pdf_path),
            )

        if package.json_report_path:
            json_path = self._copy_json(
                package,
                output_dir,
            )

            package.add_artifact(
                "json",
                str(json_path),
            )

        manifest = self._build_manifest(package)

        self._write_manifest(
            manifest,
            output_dir,
        )

        return package

    def _save_html(
        self,
        package: ReportPackage,
        output_dir: Path,
    ) -> Path:

        path = output_dir / self.HTML_FILENAME

        path.write_text(
            package.html_report.html,
            encoding="utf-8",
        )

        return path

    def _copy_pdf(
        self,
        package: ReportPackage,
        output_dir: Path,
    ) -> Path:

        source = Path(package.pdf_report.file_path)

        destination = output_dir / self.PDF_FILENAME

        if source.resolve() != destination.resolve():
            shutil.copy2(
                source,
                destination,
            )

        return destination

    def _copy_json(
        self,
        package: ReportPackage,
        output_dir: Path,
    ) -> Path:

        source = Path(package.json_report_path)

        destination = output_dir / self.JSON_FILENAME

        if source.resolve() != destination.resolve():
            shutil.copy2(
                source,
                destination,
            )

        return destination

    def _build_manifest(
        self,
        package: ReportPackage,
    ) -> dict:

        return {
            "metadata": package.metadata.to_dict(),
            "formats": package.available_formats(),
            "artifacts": package.artifacts,
        }

    def _write_manifest(
        self,
        manifest: dict,
        output_dir: Path,
    ) -> None:

        path = output_dir / self.MANIFEST_FILENAME

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                manifest,
                file,
                indent=4,
                ensure_ascii=False,
            )

    @staticmethod
    def _prepare_directory(
        directory: Path,
    ) -> None:

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def _validate_package(
        package: ReportPackage,
    ) -> None:

        if package is None:
            raise ValueError(
                "ReportPackage cannot be None."
            )