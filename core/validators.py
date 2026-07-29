"""
Pure Python format validators for LedgerSheet.

No Django imports here, ever — these are plain predicates returning bool,
reusable by the Django backend today and the PySide6 desktop app in Phase 2.
The Django layer wraps them into field/model validators.
"""

import re

from core.constants import INDIAN_STATE_CODES

# GSTIN: 2-digit state code, 5-letter PAN prefix, 4 PAN digits, 1 PAN letter,
# 1 entity code (1-9/A-Z), literal "Z", 1 checksum character.
GSTIN_RE = re.compile(r"^\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")

# 7-15 digits, optional leading "+" (fits a CharField of max_length 15).
PHONE_RE = re.compile(r"^\+?\d{7,15}$")

# Indian PIN codes are 6 digits and never start with 0.
PINCODE_RE = re.compile(r"^[1-9]\d{5}$")


def is_valid_gstin(gstin):
    """Format check + the first 2 digits must be a real Indian state code."""
    if not isinstance(gstin, str) or not GSTIN_RE.match(gstin):
        return False
    return gstin[:2] in INDIAN_STATE_CODES


def is_valid_phone(phone):
    return isinstance(phone, str) and bool(PHONE_RE.match(phone))


def is_valid_pincode(pincode):
    return isinstance(pincode, str) and bool(PINCODE_RE.match(pincode))
