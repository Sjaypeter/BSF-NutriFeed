from django.contrib import admin
from .models import LarvaeGrowthRecord, InputOutputLog


@admin.register(LarvaeGrowthRecord)
class LarvaeGrowthAdmin(admin.ModelAdmin):
    list_display = ["batch", "stage", "average_weight_mg", "population_count", "temperature_celsius", "recorded_at"]
    list_filter = ["stage", "recorded_at"]


@admin.register(InputOutputLog)
class InputOutputLogAdmin(admin.ModelAdmin):
    list_display = ["batch", "log_type", "material", "quantity_kg", "unit_cost_ngn", "recorded_at"]
    list_filter = ["log_type", "material"]