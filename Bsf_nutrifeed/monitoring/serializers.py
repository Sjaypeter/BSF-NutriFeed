from rest_framework import serializers
from .models import LarvaeGrowthRecord, InputOutputLog


class LarvaeGrowthRecordSerializer(serializers.ModelSerializer):
    recorded_by_username = serializers.ReadOnlyField(source="recorded_by.username")
    total_biomass_g = serializers.ReadOnlyField()

    class Meta:
        model = LarvaeGrowthRecord
        fields = [
            "id", "batch", "recorded_by", "recorded_by_username",
            "stage", "average_weight_mg", "population_count",
            "temperature_celsius", "humidity_pct", "total_biomass_g",
            "observations", "recorded_at",
        ]
        read_only_fields = ["id", "recorded_by", "recorded_at"]


class InputOutputLogSerializer(serializers.ModelSerializer):
    recorded_by_username = serializers.ReadOnlyField(source="recorded_by.username")

    class Meta:
        model = InputOutputLog
        fields = [
            "id", "batch", "recorded_by", "recorded_by_username",
            "log_type", "material", "quantity_kg", "unit_cost_ngn",
            "notes", "recorded_at",
        ]
        read_only_fields = ["id", "recorded_by", "recorded_at"]