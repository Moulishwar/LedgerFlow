from core import constants


def test_no_django_import():
    import sys

    assert "django" not in sys.modules


def test_state_codes_count_and_shape():
    assert len(constants.INDIAN_STATES) == 38
    for code, name in constants.INDIAN_STATES:
        assert len(code) == 2 and code.isdigit()
        assert isinstance(name, str) and name


def test_tamil_nadu_is_33():
    assert dict(constants.INDIAN_STATES)["33"] == "Tamil Nadu"


def test_gst_slabs():
    assert [str(r) for r in constants.GST_SLABS] == [
        "0",
        "0.1",
        "0.25",
        "3",
        "5",
        "12",
        "18",
        "28",
    ]


def test_primary_account_groups_count():
    assert len(constants.PRIMARY_ACCOUNT_GROUPS) == 16
    names = {g["name"] for g in constants.PRIMARY_ACCOUNT_GROUPS}
    assert len(names) == 16  # no duplicates


def test_sub_account_groups_count_and_parents_resolve():
    assert len(constants.DEFAULT_SUB_ACCOUNT_GROUPS) == 15
    primary_names = {g["name"] for g in constants.PRIMARY_ACCOUNT_GROUPS}
    for sub in constants.DEFAULT_SUB_ACCOUNT_GROUPS:
        assert sub["parent"] in primary_names


def test_system_ledgers_count_and_groups_resolve():
    assert len(constants.SYSTEM_LEDGERS) == 11
    primary_names = {g["name"] for g in constants.PRIMARY_ACCOUNT_GROUPS}
    sub_names = {g["name"] for g in constants.DEFAULT_SUB_ACCOUNT_GROUPS}
    valid_group_names = primary_names | sub_names
    for ledger in constants.SYSTEM_LEDGERS:
        assert ledger["group"] in valid_group_names


def test_party_ledger_group_mapping_covers_all_party_types():
    party_types = {value for value, _ in constants.PARTY_TYPE_CHOICES}
    assert party_types <= set(constants.PARTY_LEDGER_GROUP.keys())
