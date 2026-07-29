from django.contrib import admin

from .models import AccountGroup, Ledger


@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "nature", "is_revenue", "is_system", "company")
    list_filter = ("nature", "is_revenue", "is_system")
    search_fields = ("name",)


@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "opening_balance", "is_system", "company")
    list_filter = ("group__nature", "is_system")
    search_fields = ("name",)
