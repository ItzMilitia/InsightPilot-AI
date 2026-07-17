"""
Unit tests for DuplicateRowRule.
"""

import pandas as pd

from backend.rules.duplicate_row_rule import DuplicateRowRule


def test_duplicate_rows_pass():
    """
    Rule should pass when duplicate rows are within
    the allowed threshold.
    """

    df = pd.DataFrame(
        {
            "A": [1, 2, 3],
            "B": [10, 20, 30],
        }
    )

    rule = DuplicateRowRule(max_duplicate_rows=0)

    result = rule.evaluate(df)

    assert result.passed is True
    assert result.rule_name == "Duplicate Rows"
    assert result.expected == "<= 0"
    assert result.actual == "0"
    assert result.recommendation is None


def test_duplicate_rows_fail():
    """
    Rule should fail when duplicate rows exceed
    the configured threshold.
    """

    df = pd.DataFrame(
        {
            "A": [1, 1],
            "B": [10, 10],
        }
    )

    rule = DuplicateRowRule(max_duplicate_rows=0)

    result = rule.evaluate(df)

    assert result.passed is False
    assert result.expected == "<= 0"
    assert result.actual == "1"
    assert result.recommendation is not None


def test_duplicate_rows_exact_threshold():
    """
    Rule should pass when duplicates equal
    the configured threshold.
    """

    df = pd.DataFrame(
        {
            "A": [1, 1],
            "B": [10, 10],
        }
    )

    rule = DuplicateRowRule(max_duplicate_rows=1)

    result = rule.evaluate(df)

    assert result.passed is True


def test_duplicate_rows_empty_dataframe():
    """
    Empty DataFrame should pass.
    """

    df = pd.DataFrame()

    rule = DuplicateRowRule(max_duplicate_rows=0)

    result = rule.evaluate(df)

    assert result.passed is True
    assert result.actual == "0"


def test_duplicate_rows_multiple_duplicates():
    """
    Rule should correctly count multiple duplicate rows.
    """

    df = pd.DataFrame(
        {
            "A": [1, 1, 1, 2, 2],
            "B": [5, 5, 5, 6, 6],
        }
    )

    rule = DuplicateRowRule(max_duplicate_rows=1)

    result = rule.evaluate(df)

    # pandas duplicated() marks all but the first
    # occurrence of each duplicated row.
    assert result.actual == "3"
    assert result.passed is False


def test_duplicate_rows_large_dataset():
    """
    Rule should evaluate large datasets correctly.
    """

    df = pd.DataFrame(
        {
            "A": list(range(100000)) + [1],
            "B": list(range(100000)) + [1],
        }
    )

    rule = DuplicateRowRule(max_duplicate_rows=1)

    result = rule.evaluate(df)

    assert result.actual == "1"
    assert result.passed is True


def test_duplicate_rows_custom_severity():
    """
    Custom severity should be preserved.
    """

    df = pd.DataFrame(
        {
            "A": [1, 1],
            "B": [10, 10],
        }
    )

    rule = DuplicateRowRule(
        max_duplicate_rows=0,
        severity="error",
    )

    result = rule.evaluate(df)

    assert result.severity == "error"


def test_duplicate_rows_default_recommendation():
    """
    Failed validation should include a recommendation.
    """

    df = pd.DataFrame(
        {
            "A": [1, 1],
            "B": [10, 10],
        }
    )

    rule = DuplicateRowRule(max_duplicate_rows=0)

    result = rule.evaluate(df)

    assert result.passed is False
    assert result.recommendation is not None