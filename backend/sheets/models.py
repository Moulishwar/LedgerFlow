import uuid

from django.db import models


class Sheet(models.Model):
    SHEET_TYPE_FREE = "free"
    SHEET_TYPE_LEDGER = "ledger"
    SHEET_TYPE_CHOICES = (
        (SHEET_TYPE_FREE, "Free-form"),
        (SHEET_TYPE_LEDGER, "Ledger"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "company.Company", on_delete=models.CASCADE, related_name="sheets"
    )
    name = models.CharField(max_length=255)
    sheet_type = models.CharField(
        max_length=10, choices=SHEET_TYPE_CHOICES, default=SHEET_TYPE_FREE
    )
    sequence = models.PositiveIntegerField(default=0, help_text="Tab order")
    is_protected = models.BooleanField(
        default=False, help_text="System-generated report sheet"
    )
    row_count = models.PositiveIntegerField(default=100)
    col_count = models.PositiveIntegerField(default=26)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "name")
        ordering = ["sequence", "name"]

    def __str__(self):
        return self.name


class Cell(models.Model):
    VALUE_TYPE_TEXT = "text"
    VALUE_TYPE_NUMBER = "number"
    VALUE_TYPE_FORMULA = "formula"
    VALUE_TYPE_DATE = "date"
    VALUE_TYPE_BOOLEAN = "boolean"
    VALUE_TYPE_EMPTY = "empty"
    VALUE_TYPE_CHOICES = (
        (VALUE_TYPE_TEXT, "Text"),
        (VALUE_TYPE_NUMBER, "Number"),
        (VALUE_TYPE_FORMULA, "Formula"),
        (VALUE_TYPE_DATE, "Date"),
        (VALUE_TYPE_BOOLEAN, "Boolean"),
        (VALUE_TYPE_EMPTY, "Empty"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, related_name="cells")
    row = models.PositiveIntegerField(help_text="0-indexed")
    col = models.PositiveIntegerField(help_text="0-indexed, 0=A, 1=B, ...")
    raw_value = models.TextField(
        blank=True, help_text='What the user typed; starts with "=" if a formula'
    )
    computed_value = models.TextField(
        blank=True, help_text="Cached result of formula evaluation"
    )
    value_type = models.CharField(
        max_length=10, choices=VALUE_TYPE_CHOICES, default=VALUE_TYPE_TEXT
    )
    format_json = models.JSONField(
        default=dict,
        blank=True,
        help_text="bold, italic, fontSize, fontColor, bgColor, numberFormat, alignment, ...",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("sheet", "row", "col")
        indexes = [models.Index(fields=["sheet", "row", "col"])]
        ordering = ["row", "col"]

    def __str__(self):
        return f"{self.sheet.name}[{self.row},{self.col}]"
