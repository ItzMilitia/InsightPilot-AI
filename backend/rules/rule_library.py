"""
Enterprise Rule Library.

The RuleLibrary is responsible for:

- Selecting a Rule Pack
- Building validation rules
- Executing rules
- Returning RuleResult objects

The RuleEngine should never instantiate individual rules
or Rule Packs directly.
"""

from __future__ import annotations

from typing import Iterable, List

import pandas as pd

from backend.models.rule_result import RuleResult
from backend.rules.base_rule import BaseRule
from backend.rules.packs.banking_pack import BankingRulePack
from backend.rules.packs.generic_pack import GenericRulePack


class RuleLibrary:
    """
    Central registry for Rule Packs.
    """

    def __init__(
        self,
        rules: Iterable[BaseRule] | None = None,
    ) -> None:
        self._rules: List[BaseRule] = list(rules or [])

    ####################################################################
    # Registration
    ####################################################################

    def register(
        self,
        rule: BaseRule,
    ) -> None:
        """
        Register a single rule.
        """

        self._rules.append(rule)

    def register_many(
        self,
        rules: Iterable[BaseRule],
    ) -> None:
        """
        Register multiple rules.
        """

        self._rules.extend(rules)

    def clear(self) -> None:
        """
        Remove every registered rule.
        """

        self._rules.clear()

    ####################################################################
    # Execution
    ####################################################################

    def execute(
        self,
        dataframe: pd.DataFrame,
    ) -> List[RuleResult]:
        """
        Execute all registered rules.
        """

        results: List[RuleResult] = []

        for rule in self._rules:
            results.append(
                rule.evaluate(dataframe)
            )

        return results

    ####################################################################
    # Factory Methods
    ####################################################################

    @classmethod
    def from_generic_pack(
        cls,
        *,
        required_columns: Iterable[str] | None = None,
    ) -> "RuleLibrary":
        """
        Create a RuleLibrary using the Generic Rule Pack.
        """

        pack = GenericRulePack(
            required_columns=required_columns,
        )

        return cls(
            rules=pack.build(),
        )

    @classmethod
    def from_banking_pack(
        cls,
        *,
        required_columns: Iterable[str] | None = None,
    ) -> "RuleLibrary":
        """
        Create a RuleLibrary using the Banking Rule Pack.
        """

        pack = BankingRulePack(
            required_columns=required_columns,
        )

        return cls(
            rules=pack.build(),
        )

    ####################################################################
    # Properties
    ####################################################################

    @property
    def rules(
        self,
    ) -> List[BaseRule]:
        """
        Return all registered rules.
        """

        return list(self._rules)

    @property
    def rule_count(
        self,
    ) -> int:
        """
        Number of registered rules.
        """

        return len(self._rules)