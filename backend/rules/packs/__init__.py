"""
Rule Packs.

A Rule Pack is a reusable collection of validation rules
targeted at a specific domain or use case.

Available Packs
---------------
- GenericRulePack
- BankingRulePack

Future Packs
------------
- HealthcareRulePack
- RetailRulePack
- InsuranceRulePack
- ManufacturingRulePack
"""

from backend.rules.packs.generic_pack import GenericRulePack
from backend.rules.packs.banking_pack import BankingRulePack

__all__ = [
    "GenericRulePack",
    "BankingRulePack",
]