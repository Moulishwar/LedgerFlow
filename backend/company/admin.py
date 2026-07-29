from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "gstin", "state_code", "fy_start", "owner")
    search_fields = ("name", "legal_name", "gstin")
    list_filter = ("state_code",)
