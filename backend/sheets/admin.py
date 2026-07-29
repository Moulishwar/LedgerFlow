from django.contrib import admin

from .models import Cell, Sheet


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ("name", "sheet_type", "sequence")
    list_filter = ("sheet_type",)
    search_fields = ("name",)


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ("sheet", "row", "col", "raw_value", "value_type")
    list_filter = ("value_type",)
