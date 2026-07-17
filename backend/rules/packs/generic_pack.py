"""
Generic Rule Pack.

Provides a reusable collection of validation rules suitable for
most tabular datasets.

This pack serves as the default validation pack for
InsightPilot AI.
"""

from __future__ import annotations

from typing import Iterable, List

from backend.config.settings import settings
from backend.rules.base_rule import BaseRule
from backend.rules.duplicate_row_rule import DuplicateRowRule
from backend.rules.minimum_row_rule import MinimumRowRule
from backend.rules.required_column_rule import RequiredColumnRule


class GenericRulePack:
    """
    Default validation rule pack.

    The GenericRulePack is intentionally domain-independent
    and can be applied to most structured datasets.
    """

    def __init__(
        self,
        required_columns: Iterable[str] | None = None,
    ) -> None:
        """
        Initialize the Generic Rule Pack.

        Parameters
        ----------
        required_columns:
            Optional iterable of required column names.
        """

        self.required_columns = list(required_columns or [])

    ####################################################################
    # Public API
    ####################################################################

    def build(self) -> List[BaseRule]:
        """
        Build the complete list of validation rules.

        Returns
        -------
        List[BaseRule]
        """

        rules: List[BaseRule] = []

        rules.extend(
            self._required_column_rules()
        )

        rules.append(
            self._minimum_row_rule()
        )

        rules.append(
            self._duplicate_row_rule()
        )

        return rules

    ####################################################################
    # Rule Builders
    ####################################################################

    def _required_column_rules(
        self,
    ) -> List[BaseRule]:
        """
        Build RequiredColumnRule objects.
        """

        return [
            RequiredColumnRule(column)
            for column in self.required_columns
        ]

    def _minimum_row_rule(
        self,
    ) -> BaseRule:
        """
        Build MinimumRowRule.
        """

        return MinimumRowRule(
            minimum_rows=settings.rule_engine.minimum_rows,
            severity=settings.rule_engine.default_severity,
        )

    def _duplicate_row_rule(
        self,
    ) -> BaseRule:
        """
        Build DuplicateRowRule.
        """

        return DuplicateRowRule(
            max_duplicate_rows=(
                settings.rule_engine.max_duplicate_rows
            ),
            severity=settings.rule_engine.default_severity,
        )