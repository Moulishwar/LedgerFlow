import uuid

from django.core.exceptions import ValidationError
from django.db import models

from config.validators import validate_gstin, validate_phone, validate_pincode
from core.constants import INDIAN_STATES, PARTY_TYPE_CHOICES


class Party(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="parties"
    )
    name = models.CharField(max_length=255)
    party_type = models.CharField(max_length=10, choices=PARTY_TYPE_CHOICES)
    gstin = models.CharField(max_length=15, blank=True, validators=[validate_gstin])
    state_code = models.CharField(max_length=2, choices=INDIAN_STATES)
    contact_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True, validators=[validate_phone])
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True, validators=[validate_pincode])
    credit_days = models.PositiveIntegerField(
        default=0, help_text="Default credit period, in days"
    )
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "parties"
        unique_together = ("company", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.gstin and self.state_code and self.gstin[:2] != self.state_code:
            raise ValidationError(
                {"gstin": "GSTIN state code (first 2 digits) must match the selected state."}
            )

    @property
    def is_intra_state(self):
        return self.state_code == self.company.state_code
