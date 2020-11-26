from rest_framework import serializers
from django.contrib.auth.models import User
# from works.models import

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
