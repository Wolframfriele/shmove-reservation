from rest_framework import serializers
from django.contrib.auth.models import User
from barber.models import Appointments


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'


class DashAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
