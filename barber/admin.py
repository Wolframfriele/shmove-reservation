from django.contrib import admin
from .models import Appointments, Credentials, StandardWeek, TimeSlices, Treatments

admin.site.register(Appointments)
admin.site.register(Credentials)
admin.site.register(StandardWeek)
admin.site.register(TimeSlices)
admin.site.register(Treatments)
