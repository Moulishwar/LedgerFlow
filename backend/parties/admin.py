from django.contrib import admin

from .models import Party


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "party_type",
        "gstin",
        "state_code",
        "credit_days",
        "is_active",
    )
    list_filter = ("party_type", "is_active")
    search_fields = ("name", "gstin", "contact_person")
