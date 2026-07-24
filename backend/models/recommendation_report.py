"""
Enterprise Recommendation Report Model.

Represents actionable recommendations generated from the
InsightPilot AI analysis pipeline.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Any


# ==========================================================
# Recommendation Enums
# ==========================================================

class RecommendationPriority(str, Enum):
    """
    Priority level of a recommendation.
    """

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class BusinessImpact(str, Enum):
    """
    Expected business impact.
    """

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ImplementationEffort(str, Enum):
    """
    Estimated implementation effort.
    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# ==========================================================
# Recommendation
# ==========================================================

@dataclass(slots=True)
class Recommendation:
    """
    Represents a single actionable recommendation.
    """

    id: str

    title: str

    description: str

    category: str

    priority: RecommendationPriority

    impact: BusinessImpact

    effort: ImplementationEffort

    source_engine: str

    affected_columns: list[str] = field(
        default_factory=list
    )

    implementation_steps: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Recommendation":
        """
        Deserialize Recommendation.
        """

        return cls(
            id=data.get(
                "id",
                "",
            ),
            title=data.get(
                "title",
                "",
            ),
            description=data.get(
                "description",
                "",
            ),
            category=data.get(
                "category",
                "",
            ),
            priority=RecommendationPriority(
                data.get(
                    "priority",
                    RecommendationPriority.MEDIUM.value,
                )
            ),
            impact=BusinessImpact(
                data.get(
                    "impact",
                    BusinessImpact.MEDIUM.value,
                )
            ),
            effort=ImplementationEffort(
                data.get(
                    "effort",
                    ImplementationEffort.MEDIUM.value,
                )
            ),
            source_engine=data.get(
                "source_engine",
                "",
            ),
            affected_columns=list(
                data.get(
                    "affected_columns",
                    [],
                )
            ),
            implementation_steps=list(
                data.get(
                    "implementation_steps",
                    [],
                )
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )


# ==========================================================
# Recommendation Summary
# ==========================================================

@dataclass(slots=True)
class RecommendationSummary:
    """
    Summary statistics for recommendations.
    """

    total_actions: int = 0

    high_priority: int = 0

    medium_priority: int = 0

    low_priority: int = 0

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "RecommendationSummary":
        """
        Deserialize RecommendationSummary.
        """

        return cls(**data)


# ==========================================================
# Recommendation Report
# ==========================================================

@dataclass(slots=True)
class RecommendationReport:
    """
    Collection of actionable recommendations.
    """

    summary: RecommendationSummary = field(
        default_factory=RecommendationSummary
    )

    recommendations: list[Recommendation] = field(
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
    ) -> "RecommendationReport":
        """
        Deserialize RecommendationReport.
        """

        return cls(
            summary=RecommendationSummary.from_dict(
                data.get(
                    "summary",
                    {},
                )
            ),
            recommendations=[
                Recommendation.from_dict(item)
                for item in data.get(
                    "recommendations",
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