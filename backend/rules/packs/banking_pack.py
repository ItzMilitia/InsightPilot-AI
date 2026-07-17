"""
Banking Rule Pack.

Extends the Generic Rule Pack with banking-specific validation
rules.

This pack demonstrates how InsightPilot AI can support
industry-specific validation without modifying the core
validation framework.
"""

from __future__ import annotations

from typing import Iterable, List

from backend.rules.base_rule import BaseRule
from backend.rules.packs.generic_pack import GenericRulePack
from backend.rules.required_column_rule import RequiredColumnRule


class BankingRulePack(GenericRulePack):
    """
    Banking-specific validation rule pack.

    This pack includes all Generic validation rules and
    automatically validates common banking columns.
    """

    DEFAULT_BANKING_COLUMNS = [
        "CustomerID",
        "AccountNumber",
        "Balance",
    ]

    def __init__(
        self,
        required_columns: Iterable[str] | None = None,
    ) -> None:
        """
        Initialize the Banking Rule Pack.

        Parameters
        ----------
        required_columns:
            Additional required columns.
        """

        columns = list(self.DEFAULT_BANKING_COLUMNS)

        if required_columns:
            for column in required_columns:
                if column not in columns:
                    columns.append(column)

        super().__init__(required_columns=columns)

    ####################################################################
    # Public API
    ####################################################################

    def build(self) -> List[BaseRule]:
        """
        Build the banking validation rule set.

        Returns
        -------
        List[BaseRule]
        """

        rules = super().build()

        rules.extend(
            self._banking_rules()
        )

        return rules

    ####################################################################
    # Banking Rules
    ####################################################################

    def _banking_rules(
        self,
    ) -> List[BaseRule]:
        """
        Build banking-specific rules.

        Currently this validates additional banking columns.

        Future releases can introduce:

        - Account balance rules
        - Transaction rules
        - IBAN validation
        - Currency validation
        - Credit score validation
        - AML validation
        - Fraud detection rules
        """

        return [
            RequiredColumnRule("TransactionDate"),
            RequiredColumnRule("BranchCode"),
        ]