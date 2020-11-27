from rest_framework import serializers
from django.contrib.auth.models import User
from barber.models import Appointments

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class NewAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'
