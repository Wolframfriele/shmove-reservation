from django.contrib import admin
from .models import Appointments, Credentials, Daily, Openinghours, Timeslices

# Register your models here.
admin.site.register(Appointments)
admin.site.register(Credentials)
admin.site.register(Daily)
admin.site.register(Openinghours)
admin.site.register(Timeslices)
