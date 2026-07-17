"""
Unit tests for RuleEngine.
"""

import pandas as pd
import pytest

from backend.engines.rule_engine import RuleEngine
from backend.models.rule_report import RuleReport


def test_rule_engine_initialization():
    """
    RuleEngine should initialize successfully.
    """
    engine = RuleEngine()

    assert engine is not None


def test_evaluate_returns_rule_report():
    """
    evaluate() should return a RuleReport.
    """
    df = pd.DataFrame(
        {
            "CustomerID": [1, 2],
            "Balance": [100, 200],
        }
    )

    engine = RuleEngine()

    report = engine.evaluate(df)

    assert isinstance(report, RuleReport)


def test_empty_dataframe_returns_report():
    """
    Empty DataFrame should still return a RuleReport.
    """
    df = pd.DataFrame()

    engine = RuleEngine()

    report = engine.evaluate(df)

    assert isinstance(report, RuleReport)


def test_total_rules_matches_results():
    """
    total_rules should equal the number of RuleResults.
    """
    df = pd.DataFrame(
        {
            "CustomerID": [1],
            "Balance": [100],
        }
    )

    engine = RuleEngine()

    report = engine.evaluate(df)

    assert report.total_rules == len(report.results)


def test_passed_failed_equals_total():
    """
    passed_rules + failed_rules should equal total_rules.
    """
    df = pd.DataFrame(
        {
            "CustomerID": [1],
            "Balance": [100],
        }
    )

    engine = RuleEngine()

    report = engine.evaluate(df)

    assert (
        report.passed_rules
        + report.failed_rules
        == report.total_rules
    )


def test_pass_status_when_all_rules_pass():
    """
    Valid data should produce PASS status.
    """
    df = pd.DataFrame(
        {
            "CustomerID": list(range(10)),
            "Balance": [100] * 10,
        }
    )

    engine = RuleEngine()

    report = engine.evaluate(
        df,
        required_columns=["CustomerID", "Balance"],
    )

    print("Overall:", report.overall_status)
    print("Passed:", report.passed_rules)
    print("Failed:", report.failed_rules)
    print("Warnings:", report.warning_rules)

    for result in report.results:
        print(result)

    assert report.overall_status == "PASS"


def test_fail_status_when_required_column_missing():
    """
    Missing required column should produce FAIL status.
    """
    df = pd.DataFrame(
        {
            "CustomerID": [1, 2],
        }
    )

    engine = RuleEngine()

    report = engine.evaluate(
        df,
        required_columns=[
            "CustomerID",
            "Balance",
        ],
    )

    assert report.overall_status == "FAIL"
    assert report.failed_rules > 0


def test_generic_pack_execution():
    """
    Generic rule pack should execute successfully.
    """
    df = pd.DataFrame(
        {
            "CustomerID": [1],
            "Balance": [100],
        }
    )

    engine = RuleEngine()

    report = engine.evaluate(
        df,
        pack="generic",
    )

    assert isinstance(report, RuleReport)


def test_banking_pack_execution():
    """
    Banking rule pack should execute successfully.
    """
    df = pd.DataFrame(
        {
            "CustomerID": [1],
            "AccountNumber": ["A001"],
            "Balance": [100],
            "TransactionDate": ["2025-01-01"],
            "BranchCode": ["B01"],
        }
    )

    engine = RuleEngine()

    report = engine.evaluate(
        df,
        pack="banking",
    )

    assert isinstance(report, RuleReport)


def test_invalid_pack_raises_value_error():
    """
    Unknown rule pack should raise ValueError.
    """
    df = pd.DataFrame()

    engine = RuleEngine()

    with pytest.raises(ValueError):
        engine.evaluate(
            df,
            pack="unknown",
        )