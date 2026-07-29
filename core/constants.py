"""
Pure Python constants for LedgerSheet's accounting domain.

No Django imports here, ever. This module must remain importable standalone
(e.g. from a future PySide6 desktop app) without pulling in a web framework.
"""

from decimal import Decimal

# ---------------------------------------------------------------------------
# Indian states / union territories — GST state codes (first 2 digits of GSTIN)
# ---------------------------------------------------------------------------

INDIAN_STATES = (
    ("01", "Jammu and Kashmir"),
    ("02", "Himachal Pradesh"),
    ("03", "Punjab"),
    ("04", "Chandigarh"),
    ("05", "Uttarakhand"),
    ("06", "Haryana"),
    ("07", "Delhi"),
    ("08", "Rajasthan"),
    ("09", "Uttar Pradesh"),
    ("10", "Bihar"),
    ("11", "Sikkim"),
    ("12", "Arunachal Pradesh"),
    ("13", "Nagaland"),
    ("14", "Manipur"),
    ("15", "Mizoram"),
    ("16", "Tripura"),
    ("17", "Meghalaya"),
    ("18", "Assam"),
    ("19", "West Bengal"),
    ("20", "Jharkhand"),
    ("21", "Odisha"),
    ("22", "Chhattisgarh"),
    ("23", "Madhya Pradesh"),
    ("24", "Gujarat"),
    ("25", "Daman and Diu"),
    ("26", "Dadra and Nagar Haveli and Daman and Diu"),
    ("27", "Maharashtra"),
    ("28", "Andhra Pradesh (Before Division)"),
    ("29", "Karnataka"),
    ("30", "Goa"),
    ("31", "Lakshadweep"),
    ("32", "Kerala"),
    ("33", "Tamil Nadu"),
    ("34", "Puducherry"),
    ("35", "Andaman and Nicobar Islands"),
    ("36", "Telangana"),
    ("37", "Andhra Pradesh (Newly Added)"),
    ("38", "Ladakh"),
)

INDIAN_STATE_CODES = {code for code, _ in INDIAN_STATES}

# ---------------------------------------------------------------------------
# GST
# ---------------------------------------------------------------------------

GST_SLABS = (
    Decimal("0"),
    Decimal("0.1"),
    Decimal("0.25"),
    Decimal("3"),
    Decimal("5"),
    Decimal("12"),
    Decimal("18"),
    Decimal("28"),
)

GST_SLAB_CHOICES = tuple((str(rate), f"{rate}%") for rate in GST_SLABS)

# ---------------------------------------------------------------------------
# Account nature
# ---------------------------------------------------------------------------

NATURE_ASSET = "asset"
NATURE_LIABILITY = "liability"
NATURE_INCOME = "income"
NATURE_EXPENSE = "expense"

ACCOUNT_NATURE_CHOICES = (
    (NATURE_ASSET, "Asset"),
    (NATURE_LIABILITY, "Liability"),
    (NATURE_INCOME, "Income"),
    (NATURE_EXPENSE, "Expense"),
)

# ---------------------------------------------------------------------------
# Account groups — Tally-compatible primary groups + default sub-groups
# ---------------------------------------------------------------------------

# 16 primary groups. is_revenue=True => appears on P&L, False => Balance Sheet.
PRIMARY_ACCOUNT_GROUPS = (
    {"name": "Capital Account", "nature": NATURE_LIABILITY, "is_revenue": False},
    {"name": "Current Assets", "nature": NATURE_ASSET, "is_revenue": False},
    {"name": "Current Liabilities", "nature": NATURE_LIABILITY, "is_revenue": False},
    {"name": "Fixed Assets", "nature": NATURE_ASSET, "is_revenue": False},
    {"name": "Investments", "nature": NATURE_ASSET, "is_revenue": False},
    {"name": "Loans (Liability)", "nature": NATURE_LIABILITY, "is_revenue": False},
    {"name": "Loans & Advances (Asset)", "nature": NATURE_ASSET, "is_revenue": False},
    {"name": "Misc. Expenses (Asset)", "nature": NATURE_ASSET, "is_revenue": False},
    {"name": "Suspense Account", "nature": NATURE_ASSET, "is_revenue": False},
    {"name": "Branch / Divisions", "nature": NATURE_LIABILITY, "is_revenue": False},
    {"name": "Sales Accounts", "nature": NATURE_INCOME, "is_revenue": True},
    {"name": "Purchase Accounts", "nature": NATURE_EXPENSE, "is_revenue": True},
    {"name": "Direct Expenses", "nature": NATURE_EXPENSE, "is_revenue": True},
    {"name": "Direct Incomes", "nature": NATURE_INCOME, "is_revenue": True},
    {"name": "Indirect Expenses", "nature": NATURE_EXPENSE, "is_revenue": True},
    {"name": "Indirect Incomes", "nature": NATURE_INCOME, "is_revenue": True},
)

# 15 default sub-groups, each nested under one of the primary groups above.
DEFAULT_SUB_ACCOUNT_GROUPS = (
    {"name": "Bank Accounts", "parent": "Current Assets", "nature": NATURE_ASSET},
    {"name": "Cash-in-Hand", "parent": "Current Assets", "nature": NATURE_ASSET},
    {"name": "Sundry Debtors", "parent": "Current Assets", "nature": NATURE_ASSET},
    {"name": "Stock-in-Hand", "parent": "Current Assets", "nature": NATURE_ASSET},
    {"name": "Deposits (Asset)", "parent": "Current Assets", "nature": NATURE_ASSET},
    {"name": "Sundry Creditors", "parent": "Current Liabilities", "nature": NATURE_LIABILITY},
    {"name": "Duties & Taxes", "parent": "Current Liabilities", "nature": NATURE_LIABILITY},
    {"name": "Provisions", "parent": "Current Liabilities", "nature": NATURE_LIABILITY},
    {"name": "Bank OD / OCC", "parent": "Loans (Liability)", "nature": NATURE_LIABILITY},
    {"name": "Secured Loans", "parent": "Loans (Liability)", "nature": NATURE_LIABILITY},
    {"name": "Unsecured Loans", "parent": "Loans (Liability)", "nature": NATURE_LIABILITY},
    {"name": "Advances to Suppliers", "parent": "Loans & Advances (Asset)", "nature": NATURE_ASSET},
    {"name": "Advances to Employees", "parent": "Loans & Advances (Asset)", "nature": NATURE_ASSET},
    {"name": "Administrative Expenses", "parent": "Indirect Expenses", "nature": NATURE_EXPENSE},
    {"name": "Selling Expenses", "parent": "Indirect Expenses", "nature": NATURE_EXPENSE},
)

# ---------------------------------------------------------------------------
# System ledgers — auto-created for every new company.
# `group` is a sub-group name if the ledger sits under one, otherwise a
# primary group name for ledgers that hang directly off a primary group.
# ---------------------------------------------------------------------------

SYSTEM_LEDGERS = (
    {"name": "Cash", "group": "Cash-in-Hand"},
    {"name": "CGST Input", "group": "Duties & Taxes"},
    {"name": "SGST Input", "group": "Duties & Taxes"},
    {"name": "IGST Input", "group": "Duties & Taxes"},
    {"name": "CGST Output", "group": "Duties & Taxes"},
    {"name": "SGST Output", "group": "Duties & Taxes"},
    {"name": "IGST Output", "group": "Duties & Taxes"},
    {"name": "GST Payable", "group": "Duties & Taxes"},
    {"name": "Sales Account", "group": "Sales Accounts"},
    {"name": "Purchase Account", "group": "Purchase Accounts"},
    {"name": "Profit & Loss A/c", "group": "Capital Account"},
)

# ---------------------------------------------------------------------------
# Vouchers / parties
# ---------------------------------------------------------------------------

VOUCHER_TYPE_SALES = "sales"
VOUCHER_TYPE_PURCHASE = "purchase"
VOUCHER_TYPE_PAYMENT = "payment"
VOUCHER_TYPE_RECEIPT = "receipt"
VOUCHER_TYPE_JOURNAL = "journal"
VOUCHER_TYPE_CONTRA = "contra"
VOUCHER_TYPE_CREDIT_NOTE = "credit_note"
VOUCHER_TYPE_DEBIT_NOTE = "debit_note"

VOUCHER_TYPE_CHOICES = (
    (VOUCHER_TYPE_SALES, "Sales"),
    (VOUCHER_TYPE_PURCHASE, "Purchase"),
    (VOUCHER_TYPE_PAYMENT, "Payment"),
    (VOUCHER_TYPE_RECEIPT, "Receipt"),
    (VOUCHER_TYPE_JOURNAL, "Journal"),
    (VOUCHER_TYPE_CONTRA, "Contra"),
    (VOUCHER_TYPE_CREDIT_NOTE, "Credit Note"),
    (VOUCHER_TYPE_DEBIT_NOTE, "Debit Note"),
)

# Voucher types that carry commercial line items (VoucherItem rows).
ITEMIZED_VOUCHER_TYPES = (
    VOUCHER_TYPE_SALES,
    VOUCHER_TYPE_PURCHASE,
    VOUCHER_TYPE_CREDIT_NOTE,
    VOUCHER_TYPE_DEBIT_NOTE,
)

PARTY_TYPE_CUSTOMER = "customer"
PARTY_TYPE_SUPPLIER = "supplier"
PARTY_TYPE_BOTH = "both"

PARTY_TYPE_CHOICES = (
    (PARTY_TYPE_CUSTOMER, "Customer"),
    (PARTY_TYPE_SUPPLIER, "Supplier"),
    (PARTY_TYPE_BOTH, "Both"),
)

# Sub-group a Party's auto-created Ledger is filed under, by party_type.
PARTY_LEDGER_GROUP = {
    PARTY_TYPE_CUSTOMER: "Sundry Debtors",
    PARTY_TYPE_SUPPLIER: "Sundry Creditors",
    PARTY_TYPE_BOTH: "Sundry Debtors",
}

# ---------------------------------------------------------------------------
# Double-entry
# ---------------------------------------------------------------------------

ENTRY_TYPE_DEBIT = "dr"
ENTRY_TYPE_CREDIT = "cr"

ENTRY_TYPE_CHOICES = (
    (ENTRY_TYPE_DEBIT, "Debit"),
    (ENTRY_TYPE_CREDIT, "Credit"),
)
