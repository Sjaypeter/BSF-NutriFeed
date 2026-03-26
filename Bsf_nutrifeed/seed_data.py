import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bsf_nutrifeed.settings")
django.setup()

from django.utils import timezone
from datetime import date, timedelta
from users.models import User
from feed_production.models import FeedBatch, ProductionLog
from monitoring.models import LarvaeGrowthRecord, InputOutputLog

# ── Users ────
admin = User.objects.create_superuser(
    username="admin", email="admin@bsfnutrifeed.com",
    password="Admin@1234", role="admin", is_verified=True,
)
farmer1 = User.objects.create_user(
    username="farmer_amaka", email="amaka@farm.ng",
    password="Farmer@1234", role="farmer",
    farm_name="Amaka Poultry Farm", farm_location="Enugu, Nigeria",
    first_name="Amaka", last_name="Obi", is_verified=True,
)
farmer2 = User.objects.create_user(
    username="farmer_seun", email="seun@farm.ng",
    password="Farmer@1234", role="farmer",
    farm_name="Seun's Agro Hub", farm_location="Ibadan, Nigeria",
    first_name="Seun", last_name="Adeyemi", is_verified=True,
)

# ── Feed Batches ───────────────────────────────────────────────────────────
batch1 = FeedBatch.objects.create(
    farmer=farmer1, batch_code="BSF-2026-001", status="completed",
    bsf_larvae_kg=50, organic_waste_kg=200, water_liters=30,
    feed_produced_kg=42.5, protein_content_pct=38.2, moisture_content_pct=8.5,
    production_date=date.today() - timedelta(days=7),
    notes="First batch of the season. Good conversion rate.",
)
batch2 = FeedBatch.objects.create(
    farmer=farmer1, batch_code="BSF-2026-002", status="in_progress",
    bsf_larvae_kg=75, organic_waste_kg=300, water_liters=45,
    production_date=date.today() - timedelta(days=2),
)
batch3 = FeedBatch.objects.create(
    farmer=farmer2, batch_code="BSF-2026-003", status="completed",
    bsf_larvae_kg=100, organic_waste_kg=400, water_liters=60,
    feed_produced_kg=87, protein_content_pct=40.1, moisture_content_pct=7.9,
    production_date=date.today() - timedelta(days=5),
)

# ── Production Logs ───
ProductionLog.objects.create(batch=batch1, logged_by=farmer1, activity="Added organic waste substrate", quantity_kg=200)
ProductionLog.objects.create(batch=batch1, logged_by=farmer1, activity="Introduced BSF larvae", quantity_kg=50)
ProductionLog.objects.create(batch=batch1, logged_by=farmer1, activity="Harvested dry feed meal", quantity_kg=42.5)

# ── Larvae Growth Records ───
LarvaeGrowthRecord.objects.create(
    batch=batch1, recorded_by=farmer1, stage="early_instar",
    average_weight_mg=2.1, population_count=50000,
    temperature_celsius=27.5, humidity_pct=70.0,
    observations="Healthy early growth. Good feeding rate."
)
LarvaeGrowthRecord.objects.create(
    batch=batch1, recorded_by=farmer1, stage="prepupae",
    average_weight_mg=180.0, population_count=45000,
    temperature_celsius=26.8, humidity_pct=68.0,
    observations="Ready for harvest. Minimal mortality."
)
LarvaeGrowthRecord.objects.create(
    batch=batch2, recorded_by=farmer1, stage="mid_instar",
    average_weight_mg=55.3, population_count=72000,
    temperature_celsius=28.1, humidity_pct=72.5,
)

# ── Input/Output Logs ─────
InputOutputLog.objects.create(batch=batch1, recorded_by=farmer1, log_type="input", material="organic_waste", quantity_kg=200, unit_cost_ngn=500)
InputOutputLog.objects.create(batch=batch1, recorded_by=farmer1, log_type="input", material="bsf_larvae", quantity_kg=50, unit_cost_ngn=2000)
InputOutputLog.objects.create(batch=batch1, recorded_by=farmer1, log_type="output", material="feed_meal", quantity_kg=42.5, unit_cost_ngn=8500)
InputOutputLog.objects.create(batch=batch1, recorded_by=farmer1, log_type="output", material="compost", quantity_kg=15, unit_cost_ngn=300)

print("✅ Seed data created successfully!")
print("   Admin:   admin / Admin@1234")
print("   Farmer1: farmer_amaka / Farmer@1234")
print("   Farmer2: farmer_seun / Farmer@1234")