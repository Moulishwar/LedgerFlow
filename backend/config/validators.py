"""
Django field validators wrapping the pure-Python checks in core/validators.py.

Field validators are skipped by Django on empty values, so blank=True fields
stay optional — these only fire when the user actually typed something.
"""

from django.core.exceptions import ValidationError

from core.validators import is_valid_gstin, is_valid_phone, is_valid_pincode


def validate_gstin(value):
    if not is_valid_gstin(value):
        raise ValidationError(
            "Enter a valid 15-character GSTIN (e.g. 33AABCT1234A1Z5). "
            "The first 2 digits must be a valid Indian state code."
        )


def validate_phone(value):
    if not is_valid_phone(value):
        raise ValidationError(
            "Enter a valid phone number: 7-15 digits, optionally starting with +."
        )


def validate_pincode(value):
    if not is_valid_pincode(value):
        raise ValidationError("Enter a valid 6-digit Indian PIN code.")
