"""
Minimum Row Rule.

Validates that the dataset contains at least
a minimum number of rows.
"""

from __future__ import annotations

import pandas as pd

from backend.models.rule_result import RuleResult
from backend.rules.base_rule import BaseRule


class MinimumRowRule(BaseRule):
    """
    Validates the minimum dataset size.
    """

    def __init__(
        self,
        minimum_rows: int,
        severity: str = "error",
    ) -> None:
        """
        Initialize the rule.

        Parameters
        ----------
        minimum_rows:
            Minimum number of rows required.

        severity:
            Rule severity.
        """

        super().__init__("Minimum Row Count")

        self.minimum_rows = minimum_rows
        self.severity = severity

    def evaluate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:
        """
        Evaluate the dataset size.

        Parameters
        ----------
        dataframe:
            Dataset to validate.

        Returns
        -------
        RuleResult
        """

        self.log_start()

        row_count = len(dataframe)

        passed = row_count >= self.minimum_rows

        result = RuleResult(
            rule_name=self.rule_name,
            passed=passed,
            severity=self.severity,
            message=(
                f"Dataset contains {row_count} rows."
            ),
            expected=f">= {self.minimum_rows}",
            actual=str(row_count),
            recommendation=(
                None
                if passed
                else (
                    "Dataset contains fewer rows than "
                    "the required minimum."
                )
            ),
        )

        self.log_end(result)

        return result