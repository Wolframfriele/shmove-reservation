from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime
from datetime import datetime
from django.db import models
from django.utils import timezone


class TimeSlices(models.Model):
    slice_start = models.TimeField()
    slice_end = models.TimeField()

    def __str__(self):
        return str(self.slice_start) + ' to ' + str(self.slice_end)


class StandardWeek(models.Model):
    day = models.CharField(max_length=10)
    slice_count = models.IntegerField(default=3)
    slices = models.ManyToManyField(TimeSlices)

    def __str__(self):
        return str(self.day)


class Credentials(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(db_index=True, max_length=200)
    email = models.CharField(db_index=True, max_length=60)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name


class Treatments(models.Model):
    treatment = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.treatment) + " --- €" + str(self.price)


class Appointments(models.Model):
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    time_slice = models.ForeignKey(TimeSlices, on_delete=models.DO_NOTHING)
    treatment = models.CharField(max_length=200, null=True)
    reason = models.TextField(null=True)
    blocked = models.BooleanField(default=False)
    credentials = models.ForeignKey(Credentials, on_delete=models.DO_NOTHING, null=True)
    #
    # def __str__(self):
    #     return "Date: " + str(self.date) + ". Treatment: " + str(self.treatment)


class Vacations(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
