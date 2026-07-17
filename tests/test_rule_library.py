"""
Unit tests for RuleLibrary.
"""

import pytest

from backend.rules.base_rule import BaseRule
from backend.rules.library import RuleLibrary
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
    GenericRulePack should be registered correctly.
    """

    library = RuleLibrary()

    library.register(
        "generic",
        GenericRulePack,
    )

    pack = library.get("generic")

    assert pack is GenericRulePack


def test_register_banking_pack():
    """
    BankingRulePack should be registered correctly.
    """

    library = RuleLibrary()

    library.register(
        "banking",
        BankingRulePack,
    )

    pack = library.get("banking")

    assert pack is BankingRulePack


def test_duplicate_registration_overwrites():
    """
    Registering the same key twice should overwrite
    the previous registration.
    """

    library = RuleLibrary()

    library.register(
        "pack",
        GenericRulePack,
    )

    library.register(
        "pack",
        BankingRulePack,
    )

    assert library.get("pack") is BankingRulePack


def test_get_unknown_pack_raises():
    """
    Unknown pack names should raise KeyError.
    """

    library = RuleLibrary()

    with pytest.raises(KeyError):
        library.get("unknown")


def test_multiple_registrations():
    """
    Library should store multiple packs.
    """

    library = RuleLibrary()

    library.register(
        "generic",
        GenericRulePack,
    )

    library.register(
        "banking",
        BankingRulePack,
    )

    assert library.get("generic") is GenericRulePack
    assert library.get("banking") is BankingRulePack


def test_get_returns_same_registered_class():
    """
    get() should return exactly the registered class.
    """

    library = RuleLibrary()

    library.register(
        "generic",
        GenericRulePack,
    )

    assert library.get("generic") == GenericRulePack