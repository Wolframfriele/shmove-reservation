
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core import serializers
from django.db.models import Q
import json
# from django.contrib.auth.hashers import make_password
################################## DRF IMPORTS #######################################
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from barber.models import Appointments
from barber.serializers import TestSerializer, NewAppointmentSerializer
from django.core.files import File
from django.conf import settings
from datetime import datetime
# Create your views here.

class TestView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = TestSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_user(self, request):
        user_id = request.query_params.get('user_id')

        serializer = User.objects.filter(id=user_id)
        return Response(serializers.serialize('json', serializer))


class NewAppointments(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = NewAppointmentSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_appointment(self, request):
        customer_id = 75643
        name = "name"
        email = "email"
        phone_number = "phone_number"
        date_booked = datetime.now()
        booked_time_start = datetime.now().time()
        booked_time_end = datetime.now().time()
        treatment_array = "<question1>, <answer1>, <question2>, <answer2>, <question3>, <answer3>, etc..."
        employee_id = 375646
        serializer = Appointments.objects.create(customer_id=customer_id, name=name, email=email,
                                                 phone_number=phone_number, date_booked=date_booked,
                                                 booked_time_start=booked_time_start, booked_time_end=booked_time_end,
                                                 treatment_array=treatment_array, employee_id=employee_id)
        return Response('Appointment has been submitted. :)')


def new_appointment():
    user = User.objects.get(id=1)
    customer_id = user
    name = "name"
    email = "email"
    phone_number = "phone_number"
    date_booked = datetime.now()
    booked_time_start = datetime.now().time()
    booked_time_end = datetime.now().time()
    treatment_array = "<question1>, <answer1>, <question2>, <answer2>, <question3>, <answer3>, etc..."
    employee_id = "Yanick"
    serializer = Appointments.objects.create(customer_id=customer_id, name=name, email=email,
                                             phone_number=phone_number, date_booked=date_booked,
                                             booked_time_start=booked_time_start, booked_time_end=booked_time_end,
                                             treatment_array=treatment_array, employee_id=employee_id)


new_appointment()