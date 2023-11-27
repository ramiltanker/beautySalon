import os
import django
import random
from faker import Faker
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beautySalon.settings')
django.setup()

from salonApp.models import Service, Beautician, Appointment

fake = Faker()

# Очистка существующих данных
Service.objects.all().delete()
Beautician.objects.all().delete()
Appointment.objects.all().delete()

# Генерация услуг
for _ in range(23):
    service = Service(
        name=fake.word().capitalize(),
        description=fake.text(max_nb_chars=200),
        price=round(random.uniform(50.0, 200.0), 2)
    )
    service.save()
    print(f"Создана услуга: {service.name}")

# Генерация мастеров
for _ in range(8):
    beautician = Beautician(
        name=fake.name(),
        expertise=random.choice(['Массаж', 'Маникюр', 'Педикюр', 'Парикмахерские услуги'])
    )
    beautician.save()
    beautician.services.add(*Service.objects.order_by('?')[:3])
    print(f"Создан мастер: {beautician.name}")

# Генерация записей на услуги (доработать)
services = list(Service.objects.all())
beauticians = list(Beautician.objects.all())

for _ in range(31):
    appointment = Appointment(
        customer_name=fake.name(),
        service=random.choice(services),
        beautician=random.choice(beauticians),
        appointment_time=fake.future_datetime(end_date="+30d", tzinfo=timezone.utc)
    )
    try:
        appointment.save()
        print(f"Создана запись: {appointment.customer_name} на {appointment.appointment_time}")
    except Exception as e:
        print(f"Ошибка при создании записи: {e}")
