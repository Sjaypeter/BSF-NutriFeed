from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Avg
from .models import LarvaeGrowthRecord, InputOutputLog
from .serializers import LarvaeGrowthRecordSerializer, InputOutputLogSerializer


class LarvaeGrowthListCreateView(generics.ListCreateAPIView):
    """List or record larvae growth data."""
    serializer_class = LarvaeGrowthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["recorded_at", "stage"]

    def get_queryset(self):
        user = self.request.user
        qs = LarvaeGrowthRecord.objects.all() if user.is_staff else \
            LarvaeGrowthRecord.objects.filter(batch__farmer=user)
        batch_id = self.request.query_params.get("batch")
        if batch_id:
            qs = qs.filter(batch_id=batch_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)


class LarvaeGrowthDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LarvaeGrowthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LarvaeGrowthRecord.objects.all()
        return LarvaeGrowthRecord.objects.filter(batch__farmer=user)


class InputOutputLogListCreateView(generics.ListCreateAPIView):
    """Log and list material inputs/outputs."""
    serializer_class = InputOutputLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["recorded_at", "log_type", "material"]

    def get_queryset(self):
        user = self.request.user
        qs = InputOutputLog.objects.all() if user.is_staff else \
            InputOutputLog.objects.filter(batch__farmer=user)
        batch_id = self.request.query_params.get("batch")
        log_type = self.request.query_params.get("type")
        if batch_id:
            qs = qs.filter(batch_id=batch_id)
        if log_type:
            qs = qs.filter(log_type=log_type)
        return qs

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)


class MonitoringSummaryView(APIView):
    """Per-batch monitoring summary."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        batch_id = request.query_params.get("batch")
        user = request.user

        larvae_qs = LarvaeGrowthRecord.objects.filter(batch__farmer=user) if not user.is_staff \
            else LarvaeGrowthRecord.objects.all()
        io_qs = InputOutputLog.objects.filter(batch__farmer=user) if not user.is_staff \
            else InputOutputLog.objects.all()

        if batch_id:
            larvae_qs = larvae_qs.filter(batch_id=batch_id)
            io_qs = io_qs.filter(batch_id=batch_id)

        larvae_stats = larvae_qs.aggregate(
            avg_weight_mg=Avg("average_weight_mg"),
            avg_temperature=Avg("temperature_celsius"),
            avg_humidity=Avg("humidity_pct"),
            total_records=Sum("population_count"),
        )

        io_stats = {
            "total_input_kg": io_qs.filter(log_type="input").aggregate(t=Sum("quantity_kg"))["t"],
            "total_output_kg": io_qs.filter(log_type="output").aggregate(t=Sum("quantity_kg"))["t"],
        }

        return Response({
            "larvae_stats": larvae_stats,
            "io_stats": io_stats,
        })