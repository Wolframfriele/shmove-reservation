from rest_framework import serializers
from django.contrib.auth.models import User
# from dashboard.models import Appointments


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser')
