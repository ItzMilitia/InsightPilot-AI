"""
Enterprise Validation Result Model.

Represents the outcome of validating a persisted
InsightPilot AI report package.

The model is intentionally lightweight and immutable in
structure while providing convenience helpers for
collecting validation errors.

Future versions may extend this model to support:

- Warning messages
- Validation severity
- Error codes
- Execution timestamps
- Validation metrics
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field


# ==========================================================
# Validation Result
# ==========================================================


@dataclass(slots=True)
class ValidationResult:
    """
    Represents the result of report validation.

    Attributes
    ----------
    is_valid:
        Overall validation status.

    errors:
        Collection of validation errors.
    """

    is_valid: bool = True

    errors: list[str] = field(
        default_factory=list
    )

    # ======================================================
    # Error Management
    # ======================================================

    def add_error(
        self,
        message: str,
    ) -> None:
        """
        Add a validation error.

        Parameters
        ----------
        message:
            Validation error description.
        """

        self.errors.append(message)

        self.is_valid = False

    def add_errors(
        self,
        messages: list[str],
    ) -> None:
        """
        Add multiple validation errors.

        Parameters
        ----------
        messages:
            Collection of validation errors.
        """

        if not messages:
            return

        self.errors.extend(messages)

        self.is_valid = False

    # ======================================================
    # Status Helpers
    # ======================================================

    def has_errors(self) -> bool:
        """
        Returns True if validation errors exist.
        """

        return len(self.errors) > 0

    def error_count(self) -> int:
        """
        Returns the total number of validation errors.
        """

        return len(self.errors)

    def clear(self) -> None:
        """
        Reset validation state.
        """

        self.errors.clear()

        self.is_valid = True

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict[str, object]:
        """
        Convert the validation result into a
        serializable dictionary.
        """

        return {
            "is_valid": self.is_valid,
            "error_count": self.error_count(),
            "errors": list(self.errors),
        }