"""
Enterprise HTML Report Engine.

Coordinates generation of HTML reports for InsightPilot AI.

This engine orchestrates the reporting pipeline while delegating
individual responsibilities to specialized components.
"""

from __future__ import annotations

from pathlib import Path

from backend.core.base_engine import BaseEngine
from backend.models.report_context import ReportContext
from backend.reports.template_renderer import TemplateRenderer


class HTMLReportEngine(BaseEngine):
    """
    Enterprise HTML Report Engine.

    Responsibilities
    ----------------
    - Validate ReportContext
    - Render HTML via TemplateRenderer
    - Save generated report
    """

    def __init__(
        self,
        renderer: TemplateRenderer,
        template_name: str = "report.html",
    ) -> None:
        super().__init__()

        self.renderer = renderer
        self.template_name = template_name

    # ======================================================
    # Public API
    # ======================================================

    def generate(
        self,
        context: ReportContext,
        output_path: str | Path,
    ) -> Path:
        """
        Generate an HTML report.

        Parameters
        ----------
        context
            Fully populated ReportContext.

        output_path
            Destination HTML file.

        Returns
        -------
        Path
            Generated report path.
        """

        self.logger.info("Starting HTML report generation.")

        self._validate_context(context)

        html = self._render(context)

        output_file = self._save_report(
            html=html,
            output_path=output_path,
        )

        self.logger.info("HTML report generated successfully.")

        return output_file

    # ======================================================
    # Validation
    # ======================================================

    def _validate_context(
        self,
        context: ReportContext,
    ) -> None:
        """
        Validate report context.
        """

        if not isinstance(context, ReportContext):
            raise TypeError(
                "context must be a ReportContext."
            )

    # ======================================================
    # Rendering
    # ======================================================

    def _render(
        self,
        context: ReportContext,
    ) -> str:
        """
        Render HTML.
        """

        return self.renderer.render(
            self.template_name,
            context,
        )

    # ======================================================
    # Saving
    # ======================================================

    def _save_report(
        self,
        html: str,
        output_path: str | Path,
    ) -> Path:
        """
        Save HTML report.
        """

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            html,
            encoding="utf-8",
        )

        return output_path