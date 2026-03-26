from django.db import models
from django.conf import settings
from feed_production.models import FeedBatch


class LarvaeGrowthRecord(models.Model):
    """Tracks BSF larvae growth at different stages."""
    STAGE_CHOICES = [
        ("egg", "Egg"),
        ("early_instar", "Early Instar"),
        ("mid_instar", "Mid Instar"),
        ("prepupae", "Prepupae"),
        ("pupae", "Pupae"),
    ]

    batch = models.ForeignKey(
        FeedBatch, on_delete=models.CASCADE, related_name="larvae_records"
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="larvae_records"
    )
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    average_weight_mg = models.DecimalField(max_digits=8, decimal_places=3)
    population_count = models.PositiveIntegerField()
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observations = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"[{self.batch.batch_code}] {self.stage} — {self.recorded_at.date()}"

    @property
    def total_biomass_g(self):
        return round((float(self.average_weight_mg) * self.population_count) / 1000, 3)


class InputOutputLog(models.Model):
    """Tracks material inputs and outputs for waste management and feed conversion."""
    LOG_TYPE_CHOICES = [
        ("input", "Input"),
        ("output", "Output"),
    ]
    MATERIAL_CHOICES = [
        ("organic_waste", "Organic Waste"),
        ("water", "Water"),
        ("bsf_larvae", "BSF Larvae"),
        ("feed_meal", "Feed Meal"),
        ("compost", "Compost"),
        ("other", "Other"),
    ]

    batch = models.ForeignKey(
        FeedBatch, on_delete=models.CASCADE, related_name="io_logs"
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="io_logs"
    )
    log_type = models.CharField(max_length=10, choices=LOG_TYPE_CHOICES)
    material = models.CharField(max_length=30, choices=MATERIAL_CHOICES)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=3)
    unit_cost_ngn = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                        help_text="Cost in Nigerian Naira")
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"[{self.log_type.upper()}] {self.material} — {self.quantity_kg} kg"