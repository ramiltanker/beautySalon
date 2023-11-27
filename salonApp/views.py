from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Service, Beautician, Appointment
from .serializers import ServiceSerializer, BeauticianSerializer, AppointmentSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


def search_services(query):
    return Service.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

def find_beauticians_by_service_and_expertise(service_id, expertise):
    return Beautician.objects.filter(Q(services__id=service_id) & Q(expertise__icontains=expertise))

def get_appointments_in_time_range(start_date, end_date):
    return Appointment.objects.filter(Q(appointment_time__gte=start_date) & Q(appointment_time__lte=end_date))

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = LargeResultsSetPagination

    @action(detail=False, methods=['get'])
    def available_services(self, request):
        available_services = self.queryset.filter(available=True)
        page = self.paginate_queryset(available_services)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(available_services, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', '')
        services = Service.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        page = self.paginate_queryset(services)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

class ServiceList(APIView):
    def get(self, request):
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        name = request.query_params.get('name')

        services = Service.objects.all()

        if name:
            services = services.filter(name__icontains=name)
        if min_price:
            services = services.filter(price__gte=min_price)
        if max_price:
            services = services.filter(price__lte=max_price)

        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

class BeauticianViewSet(viewsets.ModelViewSet):
    queryset = Beautician.objects.all()
    serializer_class = BeauticianSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['expertise']

    @action(detail=False, methods=['get'])
    def filter_by_service_and_expertise(self, request):
        service_id = request.query_params.get('service_id')
        expertise = request.query_params.get('expertise', '')

        beauticians = Beautician.objects.filter(Q(services__id=service_id) & Q(expertise__icontains=expertise))
        serializer = self.get_serializer(beauticians, many=True)
        return Response(serializer.data)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['customer_name']

    @action(detail=False, methods=['get'])
    def get_appointments_in_range(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        appointments = Appointment.objects.filter(Q(appointment_time__gte=start_date) & Q(appointment_time__lte=end_date))
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reschedule(self, request, pk=None):
        appointment = self.get_object()
        new_time = request.data.get('new_time')

        if not new_time:
            return Response({"error": "Новое время не указано."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_time = timezone.datetime.fromisoformat(new_time)
        except ValueError:
            return Response({"error": "Некорректный формат времени."}, status=status.HTTP_400_BAD_REQUEST)

        if new_time < timezone.now():
            return Response({"error": "Нельзя перенести запись на прошедшее время."}, status=status.HTTP_400_BAD_REQUEST)

        appointment.appointment_time = new_time
        appointment.save()

        return Response({"message": "Время записи успешно изменено."}, status=status.HTTP_200_OK)