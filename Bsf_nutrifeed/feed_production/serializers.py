from rest_framework import serializers
from .models import FeedBatch, ProductionLog


class ProductionLogSerializer(serializers.ModelSerializer):
    logged_by_username = serializers.ReadOnlyField(source="logged_by.username")

    class Meta:
        model = ProductionLog
        fields = ["id", "batch", "logged_by", "logged_by_username",
                  "activity", "quantity_kg", "remarks", "log_date"]
        read_only_fields = ["id", "logged_by", "log_date"]


class FeedBatchSerializer(serializers.ModelSerializer):
    farmer_username = serializers.ReadOnlyField(source="farmer.username")
    conversion_ratio = serializers.ReadOnlyField()
    logs = ProductionLogSerializer(many=True, read_only=True)

    class Meta:
        model = FeedBatch
        fields = [
            "id", "batch_code", "farmer", "farmer_username", "status",
            "bsf_larvae_kg", "organic_waste_kg", "water_liters", "additives_description",
            "feed_produced_kg", "protein_content_pct", "moisture_content_pct",
            "conversion_ratio", "notes", "production_date",
            "created_at", "updated_at", "logs",
        ]
        read_only_fields = ["id", "farmer", "created_at", "updated_at"]


class FeedBatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBatch
        fields = [
            "batch_code", "status", "bsf_larvae_kg", "organic_waste_kg",
            "water_liters", "additives_description", "feed_produced_kg",
            "protein_content_pct", "moisture_content_pct", "notes", "production_date",
        ]