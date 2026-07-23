"""
Unit tests for RuleLibrary.
"""

import pytest

from backend.rules.base_rule import BaseRule
from backend.rules.rule_library import RuleLibrary
from backend.rules.packs.banking_pack import BankingRulePack
from backend.rules.packs.generic_pack import GenericRulePack


def test_library_initialization():
    """
    RuleLibrary should initialize successfully.
    """

    library = RuleLibrary()

    assert library is not None


def test_register_generic_pack():
    """
    Generic Rule Pack should populate the library.
    """

    library = RuleLibrary.from_generic_pack()

    assert library.rule_count > 0

    assert all(
        isinstance(rule, BaseRule)
        for rule in library.rules
    )


def test_register_banking_pack():
    """
    Banking Rule Pack should populate the library.
    """

    library = RuleLibrary.from_banking_pack()

    assert library.rule_count > 0

    assert all(
        isinstance(rule, BaseRule)
        for rule in library.rules
    )


def test_duplicate_registration_overwrites():
    """
    Multiple rules can be registered.
    """

    library = RuleLibrary()

    rules = RuleLibrary.from_generic_pack().rules

    library.register(rules[0])
    library.register(rules[0])

    assert library.rule_count == 2


def test_multiple_registrations():
    """
    Library should register multiple rules.
    """

    library = RuleLibrary()

    rules = RuleLibrary.from_generic_pack().rules

    library.register_many(rules)

    assert library.rule_count == len(rules)


def test_get_returns_same_registered_class():
    """
    Registered rule instances should be preserved.
    """

    library = RuleLibrary()

    rule = RuleLibrary.from_generic_pack().rules[0]

    library.register(rule)

    assert library.rules[0] is rule