from django.core.management.base import BaseCommand
from salonApp.models import Service

class Command(BaseCommand):
    help = 'Генерирует отчет о всех услугах салона красоты'

    def handle(self, *args, **kwargs):
        services = Service.objects.all()

        if not services:
            self.stdout.write(self.style.WARNING('Нет доступных услуг для отчета'))
            return

        for service in services:
            self.stdout.write(f'Услуга: {service.name}, Цена: {service.price}')

        self.stdout.write(self.style.SUCCESS('Отчет об услугах успешно сгенерирован'))
