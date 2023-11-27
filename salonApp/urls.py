from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ServiceList, BeauticianViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'beauticians', BeauticianViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('services/<int:service_id>/', ServiceList.as_view()),
    path('', include(router.urls)),
]
