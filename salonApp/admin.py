from django.contrib import admin
from .models import Service, Beautician, Appointment
from simple_history.admin import SimpleHistoryAdmin
from import_export.formats import base_formats
from import_export.admin import ImportExportModelAdmin

class ServiceAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    formats = [base_formats.CSV, base_formats.XLS, base_formats.XLSX]

class BeauticianAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    formats = [base_formats.CSV, base_formats.XLS, base_formats.XLSX]

class AppointmentAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    formats = [base_formats.CSV, base_formats.XLS, base_formats.XLSX]

admin.site.register(Service, ServiceAdmin)
admin.site.register(Beautician, BeauticianAdmin)
admin.site.register(Appointment, AppointmentAdmin)