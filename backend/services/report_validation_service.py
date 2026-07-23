from __future__ import annotations

"""
Enterprise Report Validation Service.

Responsible for validating persisted report artifacts.

Responsibilities
----------------
- Validate report directory
- Validate manifest existence
- Validate manifest schema
- Validate metadata
- Validate generated formats
- Validate referenced artifacts

This service never raises exceptions for validation failures.
Instead, it returns a ValidationResult describing all detected
issues.
"""

import json
from pathlib import Path
from typing import Any

from backend.models.validation_result import ValidationResult


class ReportValidationService:
    """
    Service responsible for validating persisted reports.
    """

    MANIFEST_FILENAME = "manifest.json"

    REQUIRED_MANIFEST_KEYS = (
        "metadata",
        "formats",
        "artifacts",
    )

    REQUIRED_METADATA_KEYS = (
        "report_id",
        "title",
        "version",
        "generated_at",
    )

    FORMAT_TO_ARTIFACT = {
        "HTML": "html",
        "PDF": "pdf",
        "JSON": "json",
    }

    # ======================================================
    # Public API
    # ======================================================

    def validate(
        self,
        report_directory: str | Path,
    ) -> ValidationResult:
        """
        Validate a persisted report directory.
        """

        result = ValidationResult()

        directory = Path(report_directory)

        if not self._validate_directory(
            directory,
            result,
        ):
            return result

        manifest = self._load_manifest(
            directory,
            result,
        )

        if manifest is None:
            return result

        self._validate_manifest_schema(
            manifest,
            result,
        )

        if result.has_errors():
            return result

        self._validate_metadata(
            manifest["metadata"],
            result,
        )

        self._validate_formats(
            manifest,
            result,
        )

        self._validate_artifacts(
            directory,
            manifest["artifacts"],
            result,
        )

        return result

    # ======================================================
    # Directory Validation
    # ======================================================

    def _validate_directory(
        self,
        directory: Path,
        result: ValidationResult,
    ) -> bool:

        if not directory.exists():

            result.add_error(
                f"Directory does not exist: {directory}"
            )

            return False

        if not directory.is_dir():

            result.add_error(
                f"Not a directory: {directory}"
            )

            return False

        return True

    # ======================================================
    # Manifest
    # ======================================================

    def _load_manifest(
        self,
        directory: Path,
        result: ValidationResult,
    ) -> dict[str, Any] | None:

        manifest_path = (
            directory / self.MANIFEST_FILENAME
        )

        if not manifest_path.exists():

            result.add_error(
                "manifest.json not found."
            )

            return None

        try:

            with manifest_path.open(
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except json.JSONDecodeError:

            result.add_error(
                "manifest.json contains invalid JSON."
            )

            return None

    # ======================================================
    # Manifest Schema
    # ======================================================

    def _validate_manifest_schema(
        self,
        manifest: dict[str, Any],
        result: ValidationResult,
    ) -> None:

        for key in self.REQUIRED_MANIFEST_KEYS:

            if key not in manifest:

                result.add_error(
                    f"Missing manifest key: {key}"
                )

    # ======================================================
    # Metadata
    # ======================================================

    def _validate_metadata(
        self,
        metadata: dict[str, Any],
        result: ValidationResult,
    ) -> None:

        for key in self.REQUIRED_METADATA_KEYS:

            value = metadata.get(key)

            if value is None or value == "":

                result.add_error(
                    f"Missing metadata field: {key}"
                )

    # ======================================================
    # Formats
    # ======================================================

    def _validate_formats(
        self,
        manifest: dict[str, Any],
        result: ValidationResult,
    ) -> None:

        formats = manifest["formats"]

        artifacts = manifest["artifacts"]

        for report_format in formats:

            artifact = self.FORMAT_TO_ARTIFACT.get(
                report_format
            )

            if artifact is None:

                result.add_error(
                    f"Unsupported format: {report_format}"
                )

                continue

            if artifact not in artifacts:

                result.add_error(
                    f"Missing artifact entry for {report_format}"
                )

    # ======================================================
    # Artifacts
    # ======================================================

    def _validate_artifacts(
        self,
        directory: Path,
        artifacts: dict[str, str],
        result: ValidationResult,
    ) -> None:

        for name, path in artifacts.items():

            artifact = Path(path)

            if not artifact.exists():

                artifact = directory / artifact

            if not artifact.exists():

                result.add_error(
                    f"Missing artifact file: {name}"
                )