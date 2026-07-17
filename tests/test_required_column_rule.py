"""
Unit tests for RequiredColumnRule.
"""

import pandas as pd

from backend.rules.required_column_rule import RequiredColumnRule


def test_required_column_exists():
    """
    Rule should pass when the required column exists.
    """

    df = pd.DataFrame(
        {
            "CustomerID": [1, 2, 3],
            "Balance": [100, 200, 300],
        }
    )

    rule = RequiredColumnRule("CustomerID")

    result = rule.evaluate(df)

    assert result.passed is True
    assert result.rule_name == "Required Column: CustomerID"
    assert result.severity == "error"
    assert "exists" in result.message.lower()
    assert result.recommendation is None


def test_required_column_missing():
    """
    Rule should fail when the required column is missing.
    """

    df = pd.DataFrame(
        {
            "Balance": [100, 200],
        }
    )

    rule = RequiredColumnRule("CustomerID")

    result = rule.evaluate(df)

    assert result.passed is False
    assert result.rule_name == "Required Column: CustomerID"
    assert result.severity == "error"
    assert "missing" in result.message.lower()
    assert result.recommendation is not None


def test_required_column_empty_dataframe():
    """
    Empty DataFrame without columns should fail.
    """

    df = pd.DataFrame()

    rule = RequiredColumnRule("CustomerID")

    result = rule.evaluate(df)

    assert result.passed is False
    assert result.rule_name == "Required Column: CustomerID"


def test_required_column_empty_dataset_with_columns():
    """
    Empty dataset with schema should still pass because
    the column exists.
    """

    df = pd.DataFrame(
        columns=[
            "CustomerID",
            "Balance",
        ]
    )

    rule = RequiredColumnRule("CustomerID")

    result = rule.evaluate(df)

    assert result.passed is True


def test_required_column_case_sensitive():
    """
    Column names should be case-sensitive.
    """

    df = pd.DataFrame(
        {
            "customerid": [1],
        }
    )

    rule = RequiredColumnRule("CustomerID")

    result = rule.evaluate(df)

    assert result.passed is False


def test_required_column_custom_severity():
    """
    Custom severity should be preserved.
    """

    df = pd.DataFrame(
        {
            "Balance": [100],
        }
    )

    rule = RequiredColumnRule(
        "CustomerID",
        severity="warning",
    )

    result = rule.evaluate(df)

    assert result.severity == "warning"


def test_required_column_custom_recommendation():
    """
    Custom recommendation should be returned on failure.
    """

    df = pd.DataFrame(
        {
            "Balance": [100],
        }
    )

    recommendation = "Please add CustomerID before importing."

    rule = RequiredColumnRule(
        "CustomerID",
        recommendation=recommendation,
    )

    result = rule.evaluate(df)

    assert result.passed is False
    assert result.recommendation == recommendation