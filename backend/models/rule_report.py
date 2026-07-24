"""
Enterprise Rule Report Model.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from backend.models.rule_result import RuleResult


@dataclass(slots=True)
class RuleReport:
    """
    Complete Rule Engine report.
    """

    total_rules: int = 0

    passed_rules: int = 0

    failed_rules: int = 0

    warning_rules: int = 0

    overall_status: str = "PASS"

    results: list[RuleResult] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert report into a serializable dictionary.
        """

        return asdict(self)
    
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "RuleReport":
        """
        Deserialize RuleReport.
        """

        return cls(
            total_rules=data.get(
                "total_rules",
                0,
            ),
            passed_rules=data.get(
                "passed_rules",
                0,
            ),
            failed_rules=data.get(
                "failed_rules",
                0,
            ),
            warning_rules=data.get(
                "warning_rules",
                0,
            ),
            overall_status=data.get(
                "overall_status",
                "PASS",
            ),
            results=[
                RuleResult.from_dict(result)
                for result in data.get(
                    "results",
                    [],
                )
            ],
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )