from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Avg, Count
from .models import FeedBatch, ProductionLog
from .serializers import FeedBatchSerializer, FeedBatchCreateSerializer, ProductionLogSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.role == "admin":
            return True
        return obj.farmer == request.user


class FeedBatchListCreateView(generics.ListCreateAPIView):
    """List all feed batches for the authenticated farmer, or create a new one."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["batch_code", "status"]
    ordering_fields = ["production_date", "created_at", "feed_produced_kg"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, "role", "") == "admin":
            return FeedBatch.objects.all()
        return FeedBatch.objects.filter(farmer=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FeedBatchCreateSerializer
        return FeedBatchSerializer

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch = serializer.save(farmer=request.user)
        return Response(
            FeedBatchSerializer(batch).data,
            status=status.HTTP_201_CREATED,
        )


class FeedBatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific feed batch."""
    serializer_class = FeedBatchSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, "role", "") == "admin":
            return FeedBatch.objects.all()
        return FeedBatch.objects.filter(farmer=user)


class ProductionLogCreateView(generics.CreateAPIView):
    """Add a production log entry to a batch."""
    serializer_class = ProductionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(logged_by=self.request.user)


class DashboardMetricsView(APIView):
    """Aggregated dashboard metrics for the current user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = FeedBatch.objects.filter(farmer=user) if not user.is_staff else FeedBatch.objects.all()

        metrics = qs.aggregate(
            total_batches=Count("id"),
            total_feed_produced_kg=Sum("feed_produced_kg"),
            total_larvae_used_kg=Sum("bsf_larvae_kg"),
            avg_protein_content=Avg("protein_content_pct"),
        )

        status_breakdown = {
            item["status"]: item["count"]
            for item in qs.values("status").annotate(count=Count("id"))
        }

        return Response({
            "metrics": metrics,
            "status_breakdown": status_breakdown,
            "recent_batches": FeedBatchSerializer(
                qs.order_by("-created_at")[:5], many=True
            ).data,
        })