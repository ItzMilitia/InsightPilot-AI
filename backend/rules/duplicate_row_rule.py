"""
Duplicate Row Rule.

Validates that the number of duplicate rows does not exceed
the configured threshold.
"""

from __future__ import annotations

import pandas as pd

from backend.models.rule_result import RuleResult
from backend.rules.base_rule import BaseRule


class DuplicateRowRule(BaseRule):
    """
    Validates duplicate rows within a dataset.
    """

    def __init__(
        self,
        max_duplicate_rows: int,
        severity: str = "warning",
    ) -> None:
        """
        Initialize the rule.

        Parameters
        ----------
        max_duplicate_rows:
            Maximum number of duplicate rows allowed.

        severity:
            Rule severity.
        """

        super().__init__("Duplicate Rows")

        self.max_duplicate_rows = max_duplicate_rows
        self.severity = severity

    def evaluate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:
        """
        Evaluate duplicate rows.

        Parameters
        ----------
        dataframe:
            Dataset to validate.

        Returns
        -------
        RuleResult
        """

        self.log_start()

        duplicate_mask = dataframe.duplicated()

        duplicate_count = int(duplicate_mask.sum())

        duplicate_indices = (
            dataframe.index[duplicate_mask]
            .tolist()
        )

        passed = (
            duplicate_count
            <= self.max_duplicate_rows
        )

        result = RuleResult(
            rule_name=self.rule_name,
            passed=passed,
            severity=self.severity,
            message=(
                f"{duplicate_count} duplicate row(s) detected."
            ),
            affected_rows=duplicate_indices,
            expected=f"<= {self.max_duplicate_rows}",
            actual=str(duplicate_count),
            recommendation=(
                None
                if passed
                else (
                    "Review and remove duplicate "
                    "records before analysis."
                )
            ),
        )

        self.log_end(result)

        return result