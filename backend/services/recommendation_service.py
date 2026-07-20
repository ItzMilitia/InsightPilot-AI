from __future__ import annotations

from backend.models.analysis_report import AnalysisReport
from backend.models.insight_report import InsightReport
from backend.models.recommendation_report import (
    BusinessImpact,
    ImplementationEffort,
    Recommendation,
    RecommendationPriority,
    RecommendationReport,
    RecommendationSummary,
)
from backend.models.rule_report import RuleReport


class RecommendationService:
    """
    Builds an enterprise RecommendationReport by aggregating
    recommendations from every analysis stage.

    Sources
    -------
    - Quality Engine
    - Rule Engine
    - Insight Engine

    The service performs aggregation only.
    It contains no business-analysis logic.
    """

    def build(
        self,
        *,
        analysis: AnalysisReport,
        rules: RuleReport,
        insights: InsightReport,
    ) -> RecommendationReport:
        """
        Build a RecommendationReport from all engine outputs.
        """

        recommendations: list[Recommendation] = []

        recommendations.extend(
            self._collect_quality_recommendations(
                analysis,
            )
        )

        recommendations.extend(
            self._collect_rule_recommendations(
                rules,
            )
        )

        recommendations.extend(
            self._collect_insight_recommendations(
                insights,
            )
        )

        recommendations = self._deduplicate(
            recommendations,
        )

        summary = self._build_summary(
            recommendations,
        )

        return RecommendationReport(
            summary=summary,
            recommendations=recommendations,
            metadata={
                "engine": "RecommendationService",
                "version": "8.3",
                "sources": [
                    "QualityEngine",
                    "RuleEngine",
                    "InsightEngine",
                ],
            },
        )

    # ==========================================================
    # Collection Methods
    # ==========================================================

    def _collect_quality_recommendations(
        self,
        analysis: AnalysisReport,
    ) -> list[Recommendation]:

        recommendations: list[Recommendation] = []

        for index, text in enumerate(
            analysis.quality.recommendations,
            start=1,
        ):

            recommendations.append(
                Recommendation(
                    id=f"QUALITY-{index}",
                    title="Data Quality Improvement",
                    description=text,
                    category="Quality",
                    priority=RecommendationPriority.MEDIUM,
                    impact=BusinessImpact.MEDIUM,
                    effort=ImplementationEffort.LOW,
                    source_engine="QualityEngine",
                )
            )

        return recommendations

    def _collect_rule_recommendations(
        self,
        rules: RuleReport,
    ) -> list[Recommendation]:

        recommendations: list[Recommendation] = []

        counter = 1

        for result in rules.results:

            if result.passed:
                continue

            description = (
                result.recommendation
                or result.message
            )

            severity = result.severity.lower()

            if severity == "critical":
                priority = RecommendationPriority.HIGH

            elif severity == "warning":
                priority = RecommendationPriority.MEDIUM

            else:
                priority = RecommendationPriority.LOW

            recommendations.append(
                Recommendation(
                    id=f"RULE-{counter}",
                    title=result.rule_name,
                    description=description,
                    category="Business Rule",
                    priority=priority,
                    impact=BusinessImpact.HIGH,
                    effort=ImplementationEffort.MEDIUM,
                    source_engine="RuleEngine",
                    affected_columns=result.affected_columns,
                    implementation_steps=[
                        "Review the affected records.",
                        "Correct invalid values.",
                        "Re-run validation.",
                    ],
                )
            )

            counter += 1

        return recommendations

    def _collect_insight_recommendations(
        self,
        insights: InsightReport,
    ) -> list[Recommendation]:

        recommendations: list[Recommendation] = []

        counter = 1

        for insight in insights.insights:

            if not insight.recommendation:
                continue

            severity = insight.severity.lower()

            if severity == "critical":
                priority = RecommendationPriority.HIGH

            elif severity == "warning":
                priority = RecommendationPriority.MEDIUM

            else:
                priority = RecommendationPriority.LOW

            recommendations.append(
                Recommendation(
                    id=f"INSIGHT-{counter}",
                    title=insight.title,
                    description=insight.recommendation,
                    category=insight.category,
                    priority=priority,
                    impact=BusinessImpact.HIGH,
                    effort=ImplementationEffort.MEDIUM,
                    source_engine=insight.source_engine,
                    affected_columns=insight.affected_columns,
                    implementation_steps=[
                        "Review the affected data.",
                        "Apply the recommended corrective action.",
                        "Re-run the analysis.",
                    ],
                )
            )

            counter += 1

        return recommendations

    # ==========================================================
    # Internal Helpers
    # ==========================================================

    def _deduplicate(
        self,
        recommendations: list[Recommendation],
    ) -> list[Recommendation]:

        unique: dict[str, Recommendation] = {}

        for recommendation in recommendations:

            key = (
                recommendation.title.strip().lower(),
                recommendation.description.strip().lower(),
            )

            if key not in unique:
                unique[key] = recommendation

        return list(unique.values())

    def _build_summary(
        self,
        recommendations: list[Recommendation],
    ) -> RecommendationSummary:

        summary = RecommendationSummary()

        summary.total_actions = len(recommendations)

        summary.high_priority = sum(
            recommendation.priority == RecommendationPriority.HIGH
            for recommendation in recommendations
        )

        summary.medium_priority = sum(
            recommendation.priority == RecommendationPriority.MEDIUM
            for recommendation in recommendations
        )

        summary.low_priority = sum(
            recommendation.priority == RecommendationPriority.LOW
            for recommendation in recommendations
        )

        return summary