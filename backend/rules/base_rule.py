"""
Base class for all validation rules.

Every business rule in InsightPilot AI must inherit from BaseRule.

Responsibilities
----------------
- Provide a common interface for all rules.
- Standardize logging.
- Ensure every rule returns a RuleResult.
- Encourage small, reusable rule implementations.

Author
------
InsightPilot AI
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from backend.core.base_engine import BaseEngine
from backend.models.rule_result import RuleResult


class BaseRule(BaseEngine, ABC):
    """
    Abstract base class for all validation rules.

    Every concrete rule must implement the `evaluate`
    method and return a RuleResult.
    """

    def __init__(self, rule_name: str) -> None:
        """
        Initialize the rule.

        Parameters
        ----------
        rule_name:
            Human-readable rule name.
        """
        super().__init__()
        self.rule_name = rule_name

    @abstractmethod
    def evaluate(
        self,
        dataframe: pd.DataFrame,
    ) -> RuleResult:
        """
        Evaluate the rule.

        Parameters
        ----------
        dataframe:
            Dataset to validate.

        Returns
        -------
        RuleResult
            Result of the rule evaluation.
        """
        raise NotImplementedError

    def log_start(self) -> None:
        """
        Log the start of rule execution.
        """
        self.logger.info(
            "Executing rule: %s",
            self.rule_name,
        )

    def log_end(
        self,
        result: RuleResult,
    ) -> None:
        """
        Log the completion of rule execution.

        Parameters
        ----------
        result:
            Rule evaluation result.
        """
        status = "PASSED" if result.passed else "FAILED"

        self.logger.info(
            "Rule '%s' completed [%s]",
            self.rule_name,
            status,
        )