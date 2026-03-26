from django.contrib import admin
from .models import FeedBatch, ProductionLog


@admin.register(FeedBatch)
class FeedBatchAdmin(admin.ModelAdmin):
    list_display = ["batch_code", "farmer", "status", "bsf_larvae_kg", "feed_produced_kg", "production_date"]
    list_filter = ["status", "production_date"]
    search_fields = ["batch_code", "farmer__username"]


@admin.register(ProductionLog)
class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ["batch", "logged_by", "activity", "quantity_kg", "log_date"]
    list_filter = ["log_date"]