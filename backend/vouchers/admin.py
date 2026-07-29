from django.contrib import admin

from .models import Voucher, VoucherEntry, VoucherItem


class VoucherItemInline(admin.TabularInline):
    model = VoucherItem
    extra = 0


class VoucherEntryInline(admin.TabularInline):
    model = VoucherEntry
    extra = 0


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = (
        "voucher_number",
        "voucher_type",
        "date",
        "party",
        "total_amount",
        "is_posted",
    )
    list_filter = ("voucher_type", "is_posted")
    search_fields = ("voucher_number", "reference_number")
    inlines = [VoucherItemInline, VoucherEntryInline]
