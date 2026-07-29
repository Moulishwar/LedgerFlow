import uuid

from django.db import models

from core.constants import ACCOUNT_NATURE_CHOICES


class AccountGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="account_groups"
    )
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    nature = models.CharField(max_length=10, choices=ACCOUNT_NATURE_CHOICES)
    is_revenue = models.BooleanField(
        default=False, help_text="True for P&L groups, False for Balance Sheet groups"
    )
    is_system = models.BooleanField(
        default=False, help_text="Auto-created group; cannot be deleted"
    )
    sequence = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "name", "parent")
        ordering = ["sequence", "name"]

    def __str__(self):
        return self.name

    @property
    def full_path(self):
        if self.parent_id:
            return f"{self.parent.full_path} > {self.name}"
        return self.name


class Ledger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="ledgers"
    )
    group = models.ForeignKey(
        AccountGroup, on_delete=models.PROTECT, related_name="ledgers"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    opening_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text="Positive = debit, negative = credit",
    )
    party = models.OneToOneField(
        "parties.Party",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ledger",
    )
    default_gst_rate = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    default_hsn_code = models.CharField(max_length=8, blank=True)
    is_system = models.BooleanField(
        default=False, help_text="System ledger; cannot be deleted"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name
