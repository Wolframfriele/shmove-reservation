from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from datetime import datetime
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
    
    def __str__(self):
        return self.name
    
class WorktimeSlices(models.Model):
    """the free places in the agenda

    Args:
        models (DB model instance): [DB fields]
    """
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    
    def __str__(self):
        return str(self.time_from)+' to '+str(self.time_to)

class Worktimes(models.Model):
    # employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, default='<day>')
    # is_open = models.BooleanField(default=False)
    start = models.TimeField(default=datetime.now().time())
    end = models.TimeField(default=datetime.now().time())
    timeSlice = models.ManyToManyField(WorktimeSlices)
    last_edit = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.day)+' '+str(self.start)+' '+str(self.end)

class Employees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barbers, on_delete=models.CASCADE)
    avatar_path = models.CharField(max_length=400)
    made_on = models.DateTimeField(auto_now_add=True)
    work_time = models.ManyToManyField(Worktimes) # if the employee is deleted, his work times would be also deleted
    last_edit = models.DateTimeField(auto_now_add=True)  # moet updated bij elke verandering in die row.
    
    def __str__(self):
        return User.objects.get(id=self.user.pk).username


class Appointments(models.Model):
    customer_id = models.IntegerField(default=0) #if 0 get custome info from credentials model else get info fron User model
    date_booked_start = models.DateTimeField(default=datetime.now())
    date_booked_end = models.DateTimeField(default=datetime.now())
    date_requested = models.DateTimeField(auto_now_add=True)
    treatment = models.CharField(max_length=1500)
    employee_id = models.IntegerField(default=0) # if 0 no specific employee choosed else get data from employee model
    done = models.BooleanField(default=False)


class Credentials(models.Model):
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.firstname


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
    
    
#  class Worktimes(models.Model):
#     # employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
#     day = models.CharField(max_length=10, default='<day>')
#     # is_open = models.BooleanField(default=False)
#     time_open = models.TimeField(default=datetime.now().time())
#     time_close = models.TimeField(default=datetime.now().time())
#     last_edit = models.DateTimeField(auto_now_add=True)
    