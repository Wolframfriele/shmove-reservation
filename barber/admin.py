from django.contrib import admin
from .models import Appointments, Credentials, Changes, StandardWeek, TimeSlices, Treatments

admin.site.register(Appointments)
admin.site.register(Credentials)
admin.site.register(Changes)
admin.site.register(StandardWeek)
admin.site.register(TimeSlices)
admin.site.register(Treatments)
