"""
Required Column Rule.

Validates that a required column exists in the dataset.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd

from backend.models.rule_result import RuleResult
from backend.rules.base_rule import BaseRule


class RequiredColumnRule(BaseRule):
    """
    Validates that a required column exists.
    """

    def __init__(
        self,
        column_name: str,
        severity: str = "error",
        recommendation: Optional[str] = None,
    ) -> None:
        """
        Initialize the rule.

        Parameters
        ----------
        column_name:
            Name of the required column.

        severity:
            Rule severity.

        recommendation:
            Optional recommendation shown when validation fails.
        """

        super().__init__(
            rule_name=f"Required Column: {column_name}"
        )

        self.column_name = column_name
        self.severity = severity
        self.recommendation = (
            recommendation
            or f"Add the required column '{column_name}'."
        )

    def evaluate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:
        """
        Evaluate whether the required column exists.

        Parameters
        ----------
        dataframe:
            Dataset to validate.

        Returns
        -------
        RuleResult
        """

        self.log_start()

        exists = self.column_name in dataframe.columns

        result = RuleResult(
            rule_name=self.rule_name,
            passed=exists,
            severity=self.severity,
            message=(
                "Column exists."
                if exists
                else f"Missing required column '{self.column_name}'."
            ),
            affected_columns=(
                []
                if exists
                else [self.column_name]
            ),
            expected="Column present",
            actual=(
                "Present"
                if exists
                else "Missing"
            ),
            recommendation=(
                None
                if exists
                else self.recommendation
            ),
        )

        self.log_end(result)

        return result