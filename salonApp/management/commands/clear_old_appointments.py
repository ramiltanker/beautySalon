from django.core.management.base import BaseCommand, CommandError
from salonApp.models import Appointment
from django.utils import timezone

class Command(BaseCommand):
    help = 'Удаляет старые записи на услуги, которые уже прошли'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        old_appointments = Appointment.objects.filter(appointment_time__lt=now)

        if not old_appointments:
            self.stdout.write(self.style.WARNING('Нет старых записей для удаления'))
            return

        count = old_appointments.count()
        old_appointments.delete()

        self.stdout.write(self.style.SUCCESS(f'Удалено {count} старых записей'))
