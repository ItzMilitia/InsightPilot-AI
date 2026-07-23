"""
Comparison Utility Functions.

Provides reusable helper functions for comparing report metrics.
These functions contain no service orchestration and are intended
to be consumed by ReportComparisonService.

Author:
    InsightPilot AI

Version:
    v0.8.9
"""

from __future__ import annotations

from typing import Any


# ==========================================================
# Numeric Comparison
# ==========================================================


def calculate_delta(
    before: int | float,
    after: int | float,
) -> float:
    """
    Calculate the difference between two numeric values.

    Parameters
    ----------
    before:
        Baseline value.

    after:
        Comparison value.

    Returns
    -------
    float
        Difference (after - before).
    """

    return float(after) - float(before)


# ==========================================================
# Percentage Change
# ==========================================================


def calculate_percentage_change(
    before: int | float,
    after: int | float,
) -> float:
    """
    Calculate percentage change.

    Parameters
    ----------
    before:
        Baseline value.

    after:
        Comparison value.

    Returns
    -------
    float
        Percentage change.

    Notes
    -----
    Returns 0.0 when the baseline value is zero.
    """

    if before == 0:
        return 0.0

    return ((after - before) / before) * 100.0


# ==========================================================
# Grade Comparison
# ==========================================================


def has_grade_changed(
    before: str,
    after: str,
) -> bool:
    """
    Determine whether the quality grade changed.
    """

    return before != after


# ==========================================================
# Dictionary Comparison
# ==========================================================


def compare_dictionary(
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """
    Compare two dictionaries.

    Returns
    -------
    dict
        Mapping of changed keys to their old/new values.
    """

    changes: dict[str, dict[str, Any]] = {}

    keys = set(before) | set(after)

    for key in sorted(keys):

        old_value = before.get(key)

        new_value = after.get(key)

        if old_value != new_value:
            changes[key] = {
                "before": old_value,
                "after": new_value,
            }

    return changes


# ==========================================================
# List Comparison
# ==========================================================


def compare_lists(
    before: list[str],
    after: list[str],
) -> dict[str, list[str]]:
    """
    Compare two unordered lists.

    Returns
    -------
    dict
        Added and removed elements.
    """

    before_set = set(before)
    after_set = set(after)

    return {
        "added": sorted(after_set - before_set),
        "removed": sorted(before_set - after_set),
    }


# ==========================================================
# Recommendation Comparison
# ==========================================================


def compare_recommendations(
    before: list[str],
    after: list[str],
) -> dict[str, list[str]]:
    """
    Compare recommendation lists.
    """

    return compare_lists(before, after)


# ==========================================================
# Improvement Detection
# ==========================================================


def metric_improved(delta: int | float) -> bool:
    """
    Determine whether a metric improved.

    Negative deltas indicate improvements for metrics where
    lower values are better (e.g., missing values, duplicates).

    Returns
    -------
    bool
    """

    return delta < 0


# ==========================================================
# Regression Detection
# ==========================================================


def metric_regressed(delta: int | float) -> bool:
    """
    Determine whether a metric regressed.

    Positive deltas indicate regressions for metrics where
    lower values are preferred.

    Returns
    -------
    bool
    """

    return delta > 0


# ==========================================================
# Equality Check
# ==========================================================


def reports_are_identical(
    metric_changes: dict[str, Any],
    improvements: list[str],
    regressions: list[str],
) -> bool:
    """
    Determine whether two reports are effectively identical.

    Parameters
    ----------
    metric_changes:
        Dictionary of detected metric changes.

    improvements:
        Improvement descriptions.

    regressions:
        Regression descriptions.

    Returns
    -------
    bool
    """

    return (
        not metric_changes
        and not improvements
        and not regressions
    )