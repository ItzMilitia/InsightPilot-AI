"""
Enterprise Report Loader Service.

Responsible for loading persisted report packages from disk
and reconstructing complete ReportPackage objects.
"""

from __future__ import annotations

from pathlib import Path

from backend.models.loaded_report import LoadedReport
from backend.models.report_package import ReportPackage
import json

from backend.models.report_context import ReportContext
from backend.models.report_package import ReportPackage
from datetime import datetime

from backend.models.html_report import HTMLReport
from backend.models.metadata import ReportMetadata
from backend.models.pdf_report import PDFReport

class ReportLoaderService:
    """
    Loads archived report packages.

    Responsibilities
    ----------------
    * Locate persisted report directories.
    * Read manifest.json.
    * Load report.json.
    * Reconstruct ReportContext.
    * Rebuild ReportPackage.
    """

    def __init__(
        self,
        reports_directory: str | Path,
    ) -> None:
        self._reports_directory = Path(
            reports_directory
        )

    def _report_directory(
        self,
        report_id: str,
    ) -> Path:
        """
        Return report directory.
        """

        return (
            self._reports_directory
            / report_id
        )
    
    def _manifest_path(
        self,
        report_id: str,
    ) -> Path:
        """
        Return manifest path.
        """

        return (
            self._report_directory(
                report_id
            )
            / "manifest.json"
        )
    
    def _report_json_path(
        self,
        report_id: str,
    ) -> Path:
        """
        Return report.json path.
        """

        return (
            self._report_directory(
                report_id
            )
            / "report.json"
        )
    
    def _load_json(
        self,
        path: Path,
    ) -> dict:
        """
        Load a JSON document.
        """

        if not path.exists():
            raise FileNotFoundError(path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as fp:
            return json.load(fp)
        
    def _artifact_path(
        self,
        report_id: str,
        filename: str,
    ) -> Path:
        """
        Return the absolute path to an artifact.
        """

        return (
            self._report_directory(report_id)
            / filename
        )

    def load(
        self,
        report_id: str,
    ) -> LoadedReport:
        """
        Load a persisted report package.
        """

        report_directory = self._report_directory(
            report_id
        )

        if not report_directory.exists():
            raise FileNotFoundError(
                f"Report '{report_id}' not found."
            )

        manifest = self._load_json(
            self._manifest_path(report_id)
        )

        report_data = self._load_json(
            self._report_json_path(report_id)
        )

        # ------------------------------------------------------
        # Reconstruct ReportContext
        # ------------------------------------------------------

        report_context = ReportContext.from_dict(
            report_data
        )

        # ------------------------------------------------------
        # Reconstruct ReportPackage
        # ------------------------------------------------------

        metadata = ReportMetadata.from_dict(
            report_data["metadata"]
        )

        package = ReportPackage(
            metadata=metadata,
        )

        metadata = ReportMetadata.from_dict(
            report_data["metadata"]
        )

        package = ReportPackage(
            metadata=metadata,
        )

        if "created_at" in manifest:
            package.created_at = datetime.fromisoformat(
                manifest["created_at"]
            )

        if "metadata_extra" in manifest:
            package.metadata_extra = dict(
                manifest["metadata_extra"]
            )

        if "artifacts" in manifest:
            package.artifacts = dict(
                manifest["artifacts"]
            )

        html_path = self._artifact_path(
            report_id,
            "report.html",
        )

        if html_path.exists():
            package.html_report = HTMLReport(
            title=metadata.title,
            html=html_path.read_text(
                encoding="utf-8",
            ),
        )
            
        pdf_path = self._artifact_path(
            report_id,
            "report.pdf",
        )

        if pdf_path.exists():
            package.pdf_report = PDFReport(
            title=metadata.title,
            file_path=str(pdf_path),
        )

        json_path = self._artifact_path(
            report_id,
            "report.json",
        )

        if json_path.exists():
            package.json_report_path = str(
                json_path
            )

        return LoadedReport(
            package=package,
            context=report_context,
        )