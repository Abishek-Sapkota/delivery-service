from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.delivery.viewset import DeliveryViewSet  # Import the viewset

# Initialize the router
router = DefaultRouter()

# Register a simple viewset with the router
router.register(r'deliveries', DeliveryViewSet, basename='delivery')


urlpatterns = [
    path('', include(router.urls)),
]