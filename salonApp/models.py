from django.db import models
from simple_history.models import HistoricalRecords

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Beautician(models.Model):
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=100)
    services = models.ManyToManyField(Service)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    customer_name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    beautician = models.ForeignKey(Beautician, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.customer_name} - {self.service.name}"