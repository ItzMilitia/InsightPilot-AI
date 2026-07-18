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