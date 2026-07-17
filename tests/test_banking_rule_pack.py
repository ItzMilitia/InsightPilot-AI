"""
Unit tests for BankingRulePack.
"""

from backend.rules.base_rule import BaseRule
from backend.rules.duplicate_row_rule import DuplicateRowRule
from backend.rules.minimum_row_rule import MinimumRowRule
from backend.rules.packs.banking_pack import BankingRulePack
from backend.rules.required_column_rule import RequiredColumnRule


def test_banking_pack_default_columns():
    """
    BankingRulePack should include the default
    banking required columns.
    """

    pack = BankingRulePack()

    rules = pack.build()

    required_rules = [
        rule for rule in rules
        if isinstance(rule, RequiredColumnRule)
    ]

    names = {rule.column_name for rule in required_rules}

    expected = {
        "CustomerID",
        "AccountNumber",
        "Balance",
        "TransactionDate",
        "BranchCode",
    }

    assert expected.issubset(names)


def test_banking_pack_additional_columns():
    """
    Additional required columns should be merged
    with the default banking columns.
    """

    pack = BankingRulePack(
        required_columns=["CreditScore"]
    )

    rules = pack.build()

    required_rules = [
        rule for rule in rules
        if isinstance(rule, RequiredColumnRule)
    ]

    names = {rule.column_name for rule in required_rules}

    assert "CreditScore" in names
    assert "CustomerID" in names
    assert "AccountNumber" in names


def test_banking_pack_no_duplicate_required_columns():
    """
    Default banking columns should not be duplicated.
    """

    pack = BankingRulePack(
        required_columns=[
            "CustomerID",
            "Balance",
        ]
    )

    rules = pack.build()

    required_rules = [
        rule.column_name
        for rule in rules
        if isinstance(rule, RequiredColumnRule)
    ]

    assert required_rules.count("CustomerID") == 1
    assert required_rules.count("Balance") == 1


def test_banking_pack_contains_minimum_row_rule():
    """
    BankingRulePack should contain exactly one
    MinimumRowRule.
    """

    pack = BankingRulePack()

    rules = pack.build()

    minimum_rules = [
        rule for rule in rules
        if isinstance(rule, MinimumRowRule)
    ]

    assert len(minimum_rules) == 1


def test_banking_pack_contains_duplicate_row_rule():
    """
    BankingRulePack should contain exactly one
    DuplicateRowRule.
    """

    pack = BankingRulePack()

    rules = pack.build()

    duplicate_rules = [
        rule for rule in rules
        if isinstance(rule, DuplicateRowRule)
    ]

    assert len(duplicate_rules) == 1


def test_banking_pack_all_rules_inherit_base_rule():
    """
    Every generated rule should inherit BaseRule.
    """

    pack = BankingRulePack()

    rules = pack.build()

    assert all(
        isinstance(rule, BaseRule)
        for rule in rules
    )


def test_banking_pack_build_returns_new_instances():
    """
    build() should return fresh rule instances.
    """

    pack = BankingRulePack()

    rules1 = pack.build()
    rules2 = pack.build()

    assert rules1 is not rules2

    for r1, r2 in zip(rules1, rules2):
        assert r1 is not r2


def test_banking_pack_rule_count():
    """
    BankingRulePack should contain:

    RequiredColumnRules
    + MinimumRowRule
    + DuplicateRowRule
    """

    pack = BankingRulePack()

    rules = pack.build()

    required_rules = [
        rule for rule in rules
        if isinstance(rule, RequiredColumnRule)
    ]

    assert len(rules) == len(required_rules) + 2