from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime

from django.db import models
from django.utils import timezone

# class Users(models.Model):
#     user_id = models.AutoField(primary_key=True)
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

class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    # customer_id = models.ForeignKey(Users, on_delete=models.CASCADE)  # not sure
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.IntegerField(max_length=10)
    date_booked = models.DateTimeField(auto_now_add=True)  # idk
    date_requested = models.DateTimeField(auto_now_add=True)
    treatment_array = models.CharField(max_length=1500)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # not sure
    done = models.BooleanField(default=False)

class TreatmentQuestions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1000)
    answers = models.CharField(max_length=10000)
    made_on = models.DateTimeField(auto_now_add=True)

class QuestionConnections(models.Model):
    question_id = models.ForeignKey(TreatmentQuestions, on_delete=models.CASCADE)  # not sure
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # not sure

class Presets(models.Model):
    preset_id = models.AutoField(primary_key=True)
    preset = models.CharField(max_length=1500)  # same as 'treatment_array' in Appointments
    made_on = models.DateTimeField(auto_now_add=True)
