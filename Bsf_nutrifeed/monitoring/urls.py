from django.urls import path
from .views import (
    LarvaeGrowthListCreateView, LarvaeGrowthDetailView,
    InputOutputLogListCreateView, MonitoringSummaryView,
)

urlpatterns = [
    path("larvae/", LarvaeGrowthListCreateView.as_view(), name="larvae-list-create"),
    path("larvae/<int:pk>/", LarvaeGrowthDetailView.as_view(), name="larvae-detail"),
    path("io-logs/", InputOutputLogListCreateView.as_view(), name="io-log-list-create"),
    path("summary/", MonitoringSummaryView.as_view(), name="monitoring-summary"),
]