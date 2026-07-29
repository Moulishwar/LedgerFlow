import uuid

from django.db import models

from core.constants import ENTRY_TYPE_CHOICES, VOUCHER_TYPE_CHOICES


class Voucher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="vouchers"
    )
    voucher_type = models.CharField(max_length=15, choices=VOUCHER_TYPE_CHOICES)
    voucher_number = models.CharField(max_length=50)
    date = models.DateField()
    party = models.ForeignKey(
        "parties.Party",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vouchers",
    )
    reference_number = models.CharField(
        max_length=100, blank=True, help_text="Supplier invoice no., cheque no."
    )
    narration = models.TextField(blank=True)
    total_taxable_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_cgst = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_sgst = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_igst = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_posted = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "voucher_type", "voucher_number")
        ordering = ["-date", "-voucher_number"]

    def __str__(self):
        return f"{self.voucher_number} ({self.get_voucher_type_display()})"


class VoucherItem(models.Model):
    """Commercial line item — only for sales, purchase, credit_note, debit_note vouchers."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=500)
    hsn_sac_code = models.CharField(max_length=8, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    unit = models.CharField(max_length=20, blank=True, default="Nos")
    rate = models.DecimalField(
        max_digits=15, decimal_places=2, help_text="Price per unit before GST"
    )
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="qty * rate * (1 - discount/100)",
    )
    gst_rate = models.DecimalField(max_digits=4, decimal_places=2, default=18)
    cgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, help_text="taxable + GST"
    )
    ledger = models.ForeignKey(
        "accounts.Ledger",
        on_delete=models.PROTECT,
        related_name="voucher_items",
        help_text="Income/expense ledger to post to",
    )
    sequence = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sequence"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="voucheritem_quantity_gt_0",
                violation_error_message="Quantity must be greater than zero.",
            ),
            models.CheckConstraint(
                condition=models.Q(rate__gte=0),
                name="voucheritem_rate_gte_0",
                violation_error_message="Rate cannot be negative.",
            ),
            models.CheckConstraint(
                condition=models.Q(discount_percent__gte=0)
                & models.Q(discount_percent__lte=100),
                name="voucheritem_discount_0_100",
                violation_error_message="Discount must be between 0 and 100 percent.",
            ),
        ]

    def __str__(self):
        return f"{self.description} ({self.voucher.voucher_number})"


class VoucherEntry(models.Model):
    """The double-entry leg. Sum of dr amounts must equal sum of cr amounts per voucher."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name="entries")
    ledger = models.ForeignKey(
        "accounts.Ledger", on_delete=models.PROTECT, related_name="voucher_entries"
    )
    entry_type = models.CharField(max_length=2, choices=ENTRY_TYPE_CHOICES)
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, help_text="Always positive; entry_type sets direction"
    )
    description = models.CharField(max_length=500, blank=True)
    sequence = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "voucher entries"
        ordering = ["sequence"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="voucherentry_amount_gt_0",
                violation_error_message="Entry amount must be greater than zero.",
            ),
        ]

    def __str__(self):
        return f"{self.ledger.name} {self.get_entry_type_display()} {self.amount}"
