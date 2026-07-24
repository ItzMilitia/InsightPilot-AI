"""
Domain model representing the outcome of a single validation rule.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class RuleResult:
    """
    Represents the result of evaluating a single business rule.
    """

    rule_name: str
    passed: bool
    severity: str
    message: str

    affected_rows: List[int] = field(default_factory=list)
    affected_columns: List[str] = field(default_factory=list)

    expected: Optional[str] = None
    actual: Optional[str] = None

    recommendation: Optional[str] = None

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "RuleResult":
        """
        Deserialize RuleResult.
        """

        return cls(
            rule_name=data.get(
                "rule_name",
                "",
            ),
            passed=data.get(
                "passed",
                False,
            ),
            severity=data.get(
                "severity",
                "",
            ),
            message=data.get(
                "message",
                "",
            ),
            affected_rows=list(
                data.get(
                    "affected_rows",
                    [],
                )
            ),
            affected_columns=list(
                data.get(
                    "affected_columns",
                    [],
                )
            ),
            expected=data.get(
                "expected",
            ),
            actual=data.get(
                "actual",
            ),
            recommendation=data.get(
                "recommendation",
            ),
        )