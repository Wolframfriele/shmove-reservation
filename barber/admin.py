from django.contrib import admin
from .models import Appointments, Barbers, Employees, Worktimes, WorktimeSlices

# Register your models here.
admin.site.register(Appointments)
admin.site.register(Barbers)
admin.site.register(Employees)
admin.site.register(Worktimes)
admin.site.register(WorktimeSlices)
