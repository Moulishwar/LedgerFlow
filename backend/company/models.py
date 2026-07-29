import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from config.validators import validate_gstin, validate_phone
from core.constants import INDIAN_STATES


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="companies"
    )
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    gstin = models.CharField(max_length=15, blank=True, validators=[validate_gstin])
    state_code = models.CharField(max_length=2, choices=INDIAN_STATES)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True, validators=[validate_phone])
    email = models.EmailField(blank=True)
    fy_start = models.DateField(help_text="Financial year start, e.g. 2026-04-01")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "companies"
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
    def fy_end(self):
        from datetime import timedelta

        return self.fy_start.replace(year=self.fy_start.year + 1) - timedelta(days=1)

    @property
    def fy_label(self):
        start_year = self.fy_start.year
        end_year = self.fy_end.year
        return f"FY {start_year}-{str(end_year)[-2:]}"
