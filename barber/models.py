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


class Barbers(models.Model):
    name = models.CharField(max_length=200)


class Employees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barbers, on_delete=models.CASCADE)
    avatar_path = models.CharField(max_length=400)
    made_on = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)  # moet updated bij elke verandering in die row.


class Appointments(models.Model):
    customer_id = models.IntegerField(default=0)
    date_booked_start = models.DateTimeField(default=datetime.now())
    date_booked_end = models.DateTimeField(default=datetime.now())
    date_requested = models.DateTimeField(auto_now_add=True)
    treatment = models.CharField(max_length=1500)
    employee_id = models.IntegerField(default=0)
    done = models.BooleanField(default=False)


class Credentials(models.Model):
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)


class Openinghours(models.Model):
    barber = models.ForeignKey(Barbers, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, default='<day>')
    is_open = models.BooleanField(default=False)
    time_open = models.TimeField(default=datetime.now().time())
    time_close = models.TimeField(default=datetime.now().time())
    last_edit = models.DateTimeField(auto_now_add=True)


class Questions(models.Model):
    barber = models.ForeignKey(Barbers, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    made_on = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)  # moet updated bij elke verandering in die row.


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    duration = models.TimeField(default=datetime.now().time())
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    made_on = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now_add=True)  # moet updated bij elke verandering in die row.


class Worktimes(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, default='<day>')
    is_open = models.BooleanField(default=False)
    time_open = models.TimeField(default=datetime.now().time())
    time_close = models.TimeField(default=datetime.now().time())
    last_edit = models.DateTimeField(auto_now_add=True)

