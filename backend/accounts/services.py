"""
Account-group / ledger provisioning logic.

Builds on the plain-data definitions in core/constants.py and turns them into
Django ORM rows. Idempotent throughout (get_or_create) so it's safe to call
repeatedly without duplicating groups or ledgers.
"""

from core.constants import (
    DEFAULT_SUB_ACCOUNT_GROUPS,
    PARTY_LEDGER_GROUP,
    PRIMARY_ACCOUNT_GROUPS,
    SYSTEM_LEDGERS,
)


def _build_group_metadata():
    meta = {}
    for group in PRIMARY_ACCOUNT_GROUPS:
        meta[group["name"]] = {
            "nature": group["nature"],
            "is_revenue": group["is_revenue"],
            "parent": None,
        }
    for group in DEFAULT_SUB_ACCOUNT_GROUPS:
        parent_meta = meta[group["parent"]]
        meta[group["name"]] = {
            "nature": group["nature"],
            "is_revenue": parent_meta["is_revenue"],
            "parent": group["parent"],
        }
    return meta


# name -> {nature, is_revenue, parent} for every primary + default sub-group.
GROUP_METADATA = _build_group_metadata()


def get_or_create_account_group(company, name):
    """Fetch (or create, with its parent chain) the named system account group."""
    from accounts.models import AccountGroup

    if name not in GROUP_METADATA:
        raise ValueError(f"Unknown account group: {name!r}")

    meta = GROUP_METADATA[name]
    parent = (
        get_or_create_account_group(company, meta["parent"]) if meta["parent"] else None
    )
    group, _ = AccountGroup.objects.get_or_create(
        company=company,
        name=name,
        parent=parent,
        defaults={
            "nature": meta["nature"],
            "is_revenue": meta["is_revenue"],
            "is_system": True,
        },
    )
    return group


def seed_company_accounts(company):
    """Create the 16 primary groups, 15 sub-groups, and 11 system ledgers for a new company."""
    from accounts.models import Ledger

    for name in GROUP_METADATA:
        get_or_create_account_group(company, name)

    for ledger_data in SYSTEM_LEDGERS:
        group = get_or_create_account_group(company, ledger_data["group"])
        Ledger.objects.get_or_create(
            company=company,
            name=ledger_data["name"],
            defaults={"group": group, "is_system": True, "opening_balance": 0},
        )


def get_or_create_party_ledger(party):
    """Ensure a Party has a matching Ledger under Sundry Debtors/Creditors."""
    from accounts.models import Ledger

    group_name = PARTY_LEDGER_GROUP[party.party_type]
    group = get_or_create_account_group(party.company, group_name)
    ledger, _ = Ledger.objects.get_or_create(
        party=party,
        defaults={
            "company": party.company,
            "group": group,
            "name": party.name,
            "is_system": False,
            "opening_balance": 0,
        },
    )
    return ledger
