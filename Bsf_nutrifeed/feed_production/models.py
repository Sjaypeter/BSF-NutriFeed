from django.db import models
from django.conf import settings


class FeedBatch(models.Model):          # ← must be named exactly FeedBatch
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feed_batches"
    )
    batch_code = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    bsf_larvae_kg = models.DecimalField(max_digits=8, decimal_places=2)
    organic_waste_kg = models.DecimalField(max_digits=8, decimal_places=2)
    water_liters = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    additives_description = models.TextField(blank=True)
    feed_produced_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    protein_content_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    moisture_content_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    production_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-production_date"]

    def __str__(self):
        return f"Batch {self.batch_code} — {self.farmer.username}"

    @property
    def conversion_ratio(self):
        if self.feed_produced_kg and self.bsf_larvae_kg:
            return round(float(self.feed_produced_kg) / float(self.bsf_larvae_kg), 2)
        return None


class ProductionLog(models.Model):
    batch = models.ForeignKey(FeedBatch, on_delete=models.CASCADE, related_name="logs")
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="production_logs"
    )
    activity = models.CharField(max_length=200)
    quantity_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True)
    log_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-log_date"]

    def __str__(self):
        return f"Log [{self.batch.batch_code}] — {self.activity}"