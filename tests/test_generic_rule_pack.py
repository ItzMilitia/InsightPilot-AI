"""
Unit tests for GenericRulePack.
"""

from backend.rules.base_rule import BaseRule
from backend.rules.duplicate_row_rule import DuplicateRowRule
from backend.rules.minimum_row_rule import MinimumRowRule
from backend.rules.packs.generic_pack import GenericRulePack
from backend.rules.required_column_rule import RequiredColumnRule


def test_generic_pack_without_required_columns():
    """
    GenericRulePack should build the default rules.
    """

    pack = GenericRulePack()

    rules = pack.build()

    assert len(rules) == 2
    assert any(isinstance(rule, MinimumRowRule) for rule in rules)
    assert any(isinstance(rule, DuplicateRowRule) for rule in rules)


def test_generic_pack_single_required_column():
    """
    One required column should produce one RequiredColumnRule.
    """

    pack = GenericRulePack(
        required_columns=["CustomerID"]
    )

    rules = pack.build()

    required_rules = [
        rule for rule in rules
        if isinstance(rule, RequiredColumnRule)
    ]

    assert len(required_rules) == 1
    assert required_rules[0].column_name == "CustomerID"


def test_generic_pack_multiple_required_columns():
    """
    Multiple required columns should create one rule
    per column.
    """

    columns = [
        "CustomerID",
        "Balance",
        "Age",
    ]

    pack = GenericRulePack(
        required_columns=columns
    )

    rules = pack.build()

    required_rules = [
        rule for rule in rules
        if isinstance(rule, RequiredColumnRule)
    ]

    assert len(required_rules) == len(columns)

    names = {rule.column_name for rule in required_rules}

    assert names == set(columns)


def test_generic_pack_total_rule_count():
    """
    Total number of rules should equal:

    required columns
    + MinimumRowRule
    + DuplicateRowRule
    """

    columns = [
        "CustomerID",
        "Balance",
    ]

    pack = GenericRulePack(
        required_columns=columns
    )

    rules = pack.build()

    assert len(rules) == len(columns) + 2


def test_generic_pack_all_are_base_rules():
    """
    Every generated object should inherit BaseRule.
    """

    pack = GenericRulePack(
        required_columns=["CustomerID"]
    )

    rules = pack.build()

    assert all(
        isinstance(rule, BaseRule)
        for rule in rules
    )


def test_generic_pack_contains_single_minimum_row_rule():
    """
    Only one MinimumRowRule should exist.
    """

    pack = GenericRulePack(
        required_columns=[
            "CustomerID",
            "Balance",
        ]
    )

    rules = pack.build()

    minimum_rules = [
        rule for rule in rules
        if isinstance(rule, MinimumRowRule)
    ]

    assert len(minimum_rules) == 1


def test_generic_pack_contains_single_duplicate_rule():
    """
    Only one DuplicateRowRule should exist.
    """

    pack = GenericRulePack(
        required_columns=[
            "CustomerID",
            "Balance",
        ]
    )

    rules = pack.build()

    duplicate_rules = [
        rule for rule in rules
        if isinstance(rule, DuplicateRowRule)
    ]

    assert len(duplicate_rules) == 1


def test_generic_pack_build_returns_new_instances():
    """
    Calling build() twice should create fresh rule objects.
    """

    pack = GenericRulePack(
        required_columns=["CustomerID"]
    )

    rules1 = pack.build()
    rules2 = pack.build()

    assert rules1 is not rules2

    for r1, r2 in zip(rules1, rules2):
        assert r1 is not r2