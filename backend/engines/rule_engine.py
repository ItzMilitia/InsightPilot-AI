"""
Enterprise Rule Engine.

Responsible for orchestrating business rule validation against
tabular datasets.

The RuleEngine delegates rule creation to RuleLibrary and
focuses solely on coordinating execution and building the final
RuleReport.
"""

from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd

from backend.core.base_engine import BaseEngine 
from backend.models.rule_report import RuleReport
from backend.models.rule_result import RuleResult
from backend.rules.rule_library import RuleLibrary


class RuleEngine(BaseEngine):
    """
    Enterprise Rule Engine.

    The RuleEngine acts as an orchestration layer and does not
    contain individual business validation logic.
    """

    def __init__(self) -> None:
        super().__init__()

    ####################################################################
    # Public API
    ####################################################################

    def evaluate(
        self,
        dataframe: pd.DataFrame,
        required_columns: Optional[Iterable[str]] = None,
        pack: str = "generic",
    ) -> RuleReport:
        """
        Evaluate business validation rules.

        Parameters
        ----------
        dataframe
            Dataset to validate.

        required_columns
            Additional required columns.

        pack
            Rule pack to execute.

            Supported values:

            - generic
            - banking

        Returns
        -------
        RuleReport
        """

        self.logger.info("Starting Rule Engine")

        library = self._create_library(
            pack=pack,
            required_columns=required_columns,
        )

        results = library.execute(dataframe)

        report = self._build_report(results)

        self.logger.info("Rule Engine completed")

        return report

    ####################################################################
    # Internal Helpers
    ####################################################################

    def _create_library(
        self,
        pack: str,
        required_columns: Optional[Iterable[str]],
    ) -> RuleLibrary:
        """
        Create a RuleLibrary using the selected Rule Pack.
        """

        pack = pack.lower()

        if pack == "generic":
            return RuleLibrary.from_generic_pack(
                required_columns=required_columns,
            )

        if pack == "banking":
            return RuleLibrary.from_banking_pack(
                required_columns=required_columns,
            )

        raise ValueError(
            f"Unknown rule pack: '{pack}'."
        )

    ####################################################################
    # Report Builder
    ####################################################################

    def _build_report(
        self,
        results: list[RuleResult],
    ) -> RuleReport:
        """
        Build a RuleReport from validation results.
        """

        passed = sum(result.passed for result in results)

        failed = sum(not result.passed for result in results)

        warnings = sum(
            (not result.passed)
            and result.severity.lower() == "warning"
            for result in results
        )

        status = "PASS" if failed == 0 else "FAIL"

        return RuleReport(
            total_rules=len(results),
            passed_rules=passed,
            failed_rules=failed,
            warning_rules=warnings,
            overall_status=status,
            results=results,
        )