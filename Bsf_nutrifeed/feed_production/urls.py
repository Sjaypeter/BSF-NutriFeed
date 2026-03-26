from django.urls import path
from .views import (
    FeedBatchListCreateView, FeedBatchDetailView,
    ProductionLogCreateView, DashboardMetricsView,
)

urlpatterns = [
    path("batches/", FeedBatchListCreateView.as_view(), name="batch-list-create"),
    path("batches/<int:pk>/", FeedBatchDetailView.as_view(), name="batch-detail"),
    path("logs/", ProductionLogCreateView.as_view(), name="log-create"),
    path("dashboard/", DashboardMetricsView.as_view(), name="dashboard-metrics"),
]