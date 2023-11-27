from rest_framework import serializers
from .models import Service, Beautician, Appointment
from django.utils import timezone

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class BeauticianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beautician
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate_appointment_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Нельзя записаться на прошедшее время.")
        return value
