from django.contrib import admin

from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "invoice_date", "due_date", "is_sent")
    list_filter = ("is_sent",)
    search_fields = ("invoice_number",)
