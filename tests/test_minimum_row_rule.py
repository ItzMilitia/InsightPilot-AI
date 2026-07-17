"""
Unit tests for MinimumRowRule.
"""

import pandas as pd

from backend.rules.minimum_row_rule import MinimumRowRule


def test_minimum_rows_pass():
    """
    Rule should pass when the dataset has at least the
    required number of rows.
    """

    df = pd.DataFrame(
        {
            "A": range(10),
        }
    )

    rule = MinimumRowRule(minimum_rows=10)

    result = rule.evaluate(df)

    assert result.passed is True
    assert result.rule_name == "Minimum Row Count"
    assert result.expected == ">= 10"
    assert result.actual == "10"
    assert result.recommendation is None


def test_minimum_rows_fail():
    """
    Rule should fail when the dataset contains fewer rows
    than required.
    """

    df = pd.DataFrame(
        {
            "A": range(5),
        }
    )

    rule = MinimumRowRule(minimum_rows=10)

    result = rule.evaluate(df)

    assert result.passed is False
    assert result.expected == ">= 10"
    assert result.actual == "5"
    assert result.recommendation is not None


def test_minimum_rows_exact_boundary():
    """
    Dataset exactly at the minimum threshold should pass.
    """

    df = pd.DataFrame(
        {
            "A": range(25),
        }
    )

    rule = MinimumRowRule(minimum_rows=25)

    result = rule.evaluate(df)

    assert result.passed is True


def test_minimum_rows_empty_dataframe():
    """
    Empty DataFrame should fail when minimum_rows > 0.
    """

    df = pd.DataFrame()

    rule = MinimumRowRule(minimum_rows=1)

    result = rule.evaluate(df)

    assert result.passed is False
    assert result.actual == "0"


def test_minimum_rows_zero_threshold():
    """
    Zero required rows should always pass.
    """

    df = pd.DataFrame()

    rule = MinimumRowRule(minimum_rows=0)

    result = rule.evaluate(df)

    assert result.passed is True


def test_minimum_rows_large_dataset():
    """
    Large datasets should be evaluated correctly.
    """

    df = pd.DataFrame(
        {
            "A": range(100_000),
        }
    )

    rule = MinimumRowRule(minimum_rows=50_000)

    result = rule.evaluate(df)

    assert result.passed is True
    assert result.actual == "100000"


def test_minimum_rows_custom_severity():
    """
    Custom severity should be preserved.
    """

    df = pd.DataFrame(
        {
            "A": range(5),
        }
    )

    rule = MinimumRowRule(
        minimum_rows=10,
        severity="warning",
    )

    result = rule.evaluate(df)

    assert result.severity == "warning"


def test_minimum_rows_default_recommendation():
    df = pd.DataFrame({"A": range(3)})

    rule = MinimumRowRule(minimum_rows=10)

    result = rule.evaluate(df)

    assert result.passed is False
    assert result.recommendation is not None