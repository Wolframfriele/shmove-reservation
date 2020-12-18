from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime
from datetime import datetime
from django.db import models
from django.utils import timezone

# class Users(models.Model):
#     user = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.CharField(max_length=200)
#     phone_number = models.IntegerField(max_length=10)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     employed_rank = models.IntegerField(max_length=1)
#     # deciding how many ranks there will be.... (0 = normal user, 1 = a 'kapper', 2 = idk)
#     preset_last_used = models.IntegerField(max_length=3)
#     presets = models.CharField(max_length=100)

# timeSlice = models.ManyToManyField(WorktimeSlices)


class Day(models.Model):
    date = models.DateField(auto_now_add=False)
    day = models.CharField(max_length=10)
    slice_count = models.IntegerField(default=3)


class Timeslices(models.Model):
    slice_start = models.TimeField()
    slice_end = models.TimeField()
    # day_id = models.ForeignKey(Day, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.slice_start) + ' to ' + str(self.slice_end)


class Credentials(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name  # was eerst 'firstname'


class Appointments(models.Model):
    date_booked_start = models.DateTimeField(default=datetime.now())
    date_booked_end = models.DateTimeField(default=datetime.now())
    date_requested = models.DateTimeField(auto_now_add=True)
    treatment = models.TextField(max_length=1500)
    reason = models.TextField(max_length=3000)
    done = models.BooleanField(default=False)
    credentials = models.ForeignKey(Credentials, on_delete=models.CASCADE)


class Treatments(models.Model):
    treatment = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
