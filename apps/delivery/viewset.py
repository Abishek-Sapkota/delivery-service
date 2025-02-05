from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Delivery
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .serializers import DeliverySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class DeliveryFilter(django_filters.FilterSet):
    class Meta:
        model = Delivery
        fields = ['status']

class DeliveryViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet that provides full CRUD operations for the Delivery model.
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
 
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DeliveryFilter
    search_fields = ['recipient_name', 'address']
    ordering_fields = ['created_at', 'status']



    
    # Custom Action: GET /api/deliveries/status/
    @action(detail=False, methods=['get'])
    def status(self, request):
        return Response({"status": "Delivery service is active"}) 
    

    # Custom Action: POST /api/deliveries/{pk}/change_status/
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """
        Custom action to update the status of a specific delivery.
        Usage: POST /api/deliveries/{pk}/change_status/
        """
        try:
            delivery = self.get_object()  # Get the delivery instance
            new_status = request.data.get("status")  # Get new status from request

            if new_status not in ['pending', 'in_transit', 'delivered', 'canceled']:
                return Response({"error": "Invalid status"}, status=400)

            delivery.status = new_status
            delivery.save()
            return Response({"message": f"Delivery {pk} status updated to {new_status}"})
        except:
            return Response({"error": "Delivery not found"}, status=404)
