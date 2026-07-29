from core.validators import is_valid_gstin, is_valid_phone, is_valid_pincode


def test_no_django_import():
    import sys

    assert "django" not in sys.modules


# --- GSTIN ---


def test_valid_gstins():
    assert is_valid_gstin("33AABCT1234A1Z5")  # Tamil Nadu
    assert is_valid_gstin("27AAPFU0939F1ZV")  # Maharashtra
    assert is_valid_gstin("07AABCU9603R1ZM")  # Delhi


def test_gstin_wrong_length():
    assert not is_valid_gstin("33AABCT1234A1Z")  # 14 chars
    assert not is_valid_gstin("33AABCT1234A1Z55")  # 16 chars
    assert not is_valid_gstin("")


def test_gstin_bad_structure():
    assert not is_valid_gstin("33aabct1234a1z5")  # lowercase
    assert not is_valid_gstin("33AABCT1234A1X5")  # 14th char must be Z
    assert not is_valid_gstin("33AABCT1234A0Z5")  # entity code cannot be 0
    assert not is_valid_gstin("3#AABCT1234A1Z5")  # junk characters
    assert not is_valid_gstin("AAABCT1234A1Z5X")  # no leading digits


def test_gstin_unknown_state_code():
    # "99" is not an Indian state code, even though the shape is right.
    assert not is_valid_gstin("99AABCT1234A1Z5")
    assert not is_valid_gstin("00AABCT1234A1Z5")


def test_gstin_non_string():
    assert not is_valid_gstin(None)
    assert not is_valid_gstin(33)


# --- Phone ---


def test_valid_phones():
    assert is_valid_phone("9876543210")
    assert is_valid_phone("+919876543210")
    assert is_valid_phone("0442345678")


def test_invalid_phones():
    assert not is_valid_phone("12345")  # too short
    assert not is_valid_phone("9876543210987654")  # 16 digits
    assert not is_valid_phone("98765 43210")  # spaces
    assert not is_valid_phone("98765-43210")  # dashes
    assert not is_valid_phone("phone")
    assert not is_valid_phone("")
    assert not is_valid_phone(None)


# --- Pincode ---


def test_valid_pincodes():
    assert is_valid_pincode("600001")
    assert is_valid_pincode("110001")


def test_invalid_pincodes():
    assert not is_valid_pincode("060001")  # cannot start with 0
    assert not is_valid_pincode("60001")  # 5 digits
    assert not is_valid_pincode("6000011")  # 7 digits
    assert not is_valid_pincode("6000A1")
    assert not is_valid_pincode("")
    assert not is_valid_pincode(None)
