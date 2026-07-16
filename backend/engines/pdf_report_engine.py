from __future__ import annotations

from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from backend.models.html_report import HTMLReport
from backend.models.pdf_report import PDFReport


class PDFReportEngine:
    """
    Generates a PDF report from an HTMLReport.

    Currently, the engine extracts the textual content from the HTML
    report and writes it into a structured PDF. This provides a
    platform-independent implementation using ReportLab.
    """

    def generate(
        self,
        html_report: HTMLReport,
        output_path: str = "reports/report.pdf",
    ) -> PDFReport:

        output_file = Path(output_path)

        self._validate_output_directory(output_file)

        self._write_pdf(
            html_report,
            output_file,
        )

        return PDFReport(
            title=html_report.title,
            file_path=str(output_file),
        )

    # ============================================================
    # Directory Validation
    # ============================================================

    def _validate_output_directory(
        self,
        output_file: Path,
    ) -> None:

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ============================================================
    # PDF Writer
    # ============================================================

    def _write_pdf(
        self,
        html_report: HTMLReport,
        output_file: Path,
    ) -> None:

        document = SimpleDocTemplate(
            str(output_file)
        )

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                html_report.title,
                styles["Title"],
            )
        )

        story.append(
            Spacer(
                1,
                20,
            )
        )

        story.append(
            Paragraph(
                html_report.html,
                styles["BodyText"],
            )
        )

        document.build(story)