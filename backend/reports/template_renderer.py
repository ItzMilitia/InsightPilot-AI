"""
Enterprise Template Renderer.

Responsible for rendering Jinja2 templates.

This renderer is intentionally independent of the report engines.
It accepts a ReportContext (or compatible mapping) and produces
rendered HTML.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from collections.abc import Mapping

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined
from jinja2 import Template
from jinja2 import TemplateNotFound
from jinja2 import select_autoescape

from backend.models.report_context import ReportContext


class TemplateRenderer:
    """
    Enterprise Jinja2 template renderer.
    """

    def __init__(
        self,
        template_directory: str | Path,
    ) -> None:
        """
        Parameters
        ----------
        template_directory
            Directory containing Jinja templates.
        """

        self.template_directory = Path(template_directory)

        if not self.template_directory.exists():
            raise FileNotFoundError(
                f"Template directory does not exist: "
                f"{self.template_directory}"
            )

        self.environment = Environment(
            loader=FileSystemLoader(self.template_directory),
            autoescape=select_autoescape(
                enabled_extensions=("html", "xml"),
                default=True,
            ),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined,
        )

        self._register_filters()
        self._register_globals()

    # ======================================================
    # Public API
    # ======================================================

    def render(
        self,
        template_name: str,
        context: ReportContext | Mapping[str, Any],
    ) -> str:
        """
        Render a template.

        Parameters
        ----------
        template_name
            Template filename.

        context
            ReportContext or dictionary.

        Returns
        -------
        str
            Rendered HTML.
        """

        template = self._load_template(template_name)

        if isinstance(context, ReportContext):
            context = context.to_dict()

        return template.render(**context)

    # ======================================================
    # Internal Helpers
    # ======================================================

    def _load_template(
        self,
        template_name: str,
    ) -> Template:
        """
        Load a template.

        Raises
        ------
        FileNotFoundError
            If the template does not exist.
        """

        try:
            return self.environment.get_template(template_name)

        except TemplateNotFound as exc:
            raise FileNotFoundError(
                f"Template '{template_name}' not found."
            ) from exc

    def _register_filters(self) -> None:
        """
        Register custom Jinja filters.

        Reserved for future use.
        """

        pass

    def _register_globals(self) -> None:
        """
        Register global template helpers.

        Reserved for future use.
        """

        pass