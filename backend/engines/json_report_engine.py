from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.core.base_engine import BaseEngine
from backend.models.report_context import ReportContext


class JSONReportEngine(BaseEngine):
    """
    Generates a JSON representation of an enterprise ReportContext.

    The generated JSON can be used for:

    - API responses
    - Report persistence
    - Future ReportPackage support
    - External integrations
    """

    def generate(
        self,
        report_context: ReportContext,
        output_path: str = "reports/report.json",
    ) -> str:
        """
        Generate a JSON report from a ReportContext.

        Parameters
        ----------
        report_context:
            Fully populated ReportContext.

        output_path:
            Destination JSON file.

        Returns
        -------
        str
            Path to the generated JSON file.
        """

        operation = "JSON report generation"
        start_time = self.log_start(operation)

        try:
            self._validate_report_context(report_context)

            output_file = Path(output_path)

            self._validate_output_directory(output_file)

            payload = report_context.to_dict()

            self._write_json(
                payload=payload,
                output_file=output_file,
            )

            self.log_finish(
                operation,
                start_time,
            )

            return str(output_file)

        except Exception as exc:
            self.log_error(
                operation,
                exc,
            )
            raise

    # ============================================================
    # Validation
    # ============================================================

    def _validate_report_context(
        self,
        report_context: ReportContext,
    ) -> None:
        """
        Validate report input.
        """

        if report_context is None:
            raise ValueError(
                "ReportContext cannot be None."
            )

    # ============================================================
    # Directory Validation
    # ============================================================

    def _validate_output_directory(
        self,
        output_file: Path,
    ) -> None:
        """
        Ensure the destination directory exists.
        """

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ============================================================
    # JSON Writer
    # ============================================================

    def _write_json(
        self,
        payload: dict[str, Any],
        output_file: Path,
    ) -> None:
        """
        Write JSON payload to disk.
        """

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                payload,
                file,
                indent=4,
                ensure_ascii=False,
                default=self._json_serializer,
            )

    # ============================================================
    # JSON Serializer
    # ============================================================

    @staticmethod
    def _json_serializer(
        value: Any,
    ) -> Any:
        """
        Serialize objects unsupported by the default
        JSON encoder.
        """

        if hasattr(value, "isoformat"):
            return value.isoformat()

        if isinstance(value, Path):
            return str(value)

        return str(value)