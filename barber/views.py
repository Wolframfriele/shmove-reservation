from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from barber.models import Appointments, Barbers, Employees, Credentials, Worktimes, WorktimeSlices
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


from barber.serializers import TestSerializer, AppointmentSerializer
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


def getpost(request, x):
    return request.data['body'][x]


class AppointmentsView(viewsets.ModelViewSet):
    # probeer de view.py class naam niet te noemen naar de model namen
    # als de class een api is probeer View achter de naam te zetten voor de duidelijkheid
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_appointment(self, request):
        customer_id = getpost(request, 'customer_id')
        name = getpost(request, 'firstname')
        email = getpost(request, 'email')
        phone_number = getpost(request, 'phone_number')
        start = datetime.strptime(getpost(request, 'start'), '%d/%m/%Y, %H:%M:%S')
        end = datetime.strptime(getpost(request, 'end'), '%d/%m/%Y, %H:%M:%S')
        # split and send the treatments as string
        treatment = ','.join(getpost(request, 'treatment'))
        employee_id = getpost(request, 'employee_id') 
        
        # create appointment
        make_appointment = Appointments.objects.create(customer_id=customer_id,
                                                 date_booked_start=start, date_booked_end=end,
                                                 treatment=treatment, employee_id=employee_id)
        if customer_id == 0:
            make_credentials = Credentials.objects.create(appointment_id=make_appointment.pk, first_name=name, email=email, phone_number=phone_number)
        else:
            # snap de else statement hier niet
            name = User.objects.get(pk=customer_id).first_name
            email = User.objects.get(pk=customer_id).email
            # phone_number = User.objects.get(pk=customer_id).phone_number
        return Response({"created": True, "name": name, "email": email, "phone_number": phone_number, "date": start})


    @csrf_exempt
    @action(methods=['post'], detail=False)
    def get_appointments_customer(self, request):
        dates = []
        start_day = datetime.strptime(getpost(request, 'start_day'), '%Y-%m-%d')
        end_day = datetime.strptime(getpost(request, 'end_day'), '%Y-%m-%d')
        employee_id = getpost(request, 'employee_id')
        appointments = Appointments.objects.filter(employee_id=employee_id, date_booked_start__gte=start_day,
                                                   date_booked_start__lte=end_day).values()
        for appointment in appointments:
            dates.append({'date_end': appointment['date_booked_end'], 'date_start': appointment['date_booked_start']})
        return Response(dates)

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def get_appointments_barber(self, request):
        the_info = []
        start_day = datetime.strptime(getpost(request, 'start_day'), '%Y-%m-%d')
        end_day = datetime.strptime(getpost(request, 'end_day'), '%Y-%m-%d')
        appointments = Appointments.objects.filter(date_booked_start__gte=start_day,
                                                   date_booked_start__lte=end_day).values()
        for appointment in appointments:
            if appointment['customer_id'] == 0:
                cust_data = Credentials.objects.get(pk=appointment['id'])
            else:
                cust_data = User.objects.get(pk=appointment['customer_id'])

            the_info.append({'date_end': appointment['date_booked_end'],
                             'date_start': appointment['date_booked_start'],
                             'done': appointment['done'],
                             'treatment': appointment['treatment'],
                             'customer_first_name': cust_data.first_name,
                             'customer_last_name': cust_data.last_name,
                             'customer_email': cust_data.email,
                             # phone_number
                             'employee_id': appointment['employee_id']
                             })
        return Response(the_info)
    
    @csrf_exempt
    @action(methods=['post'], detail=False)
    def get_free_places(self, request):
        date_times_arr = []
        time_slices = WorktimeSlices.objects.values()
        
        for t in time_slices:
            str_tf = datetime.strftime(t['time_from'], '%Y-%m-%d %H:%M') # time frome to string
            str_tt = datetime.strftime(t['time_to'], '%Y-%m-%d %H:%M') # time to to string
            # format date time obj
            obj_tf = datetime.strptime(str_tf, '%Y-%m-%d %H:%M')
            obj_tt = datetime.strptime(str_tt, '%Y-%m-%d %H:%M')
            # check if time already taked
            time_taked = Appointments.objects.filter(
                Q(date_booked_start=t['time_from']) & 
                Q(date_booked_end=t['time_to'])
            ).count()
            
            if time_taked == 0:
                # append the formatted date time
                date_times_arr.append({'start': obj_tf, 'end': obj_tt, 'taked': False})
            else:
                # append the formatted date time
                date_times_arr.append({'start': obj_tf, 'end': obj_tt, 'taked': True})
            
        return Response(date_times_arr)
        
        
        
        
        
# serializers.serialize('json', appointments)


# class NewAppointments(viewsets.ModelViewSet):
#     queryset = Appointments.objects.all()
#     serializer_class = NewAppointmentSerializer
#     permission_classes = [AllowAny]

    # @csrf_exempt
    # @action(methods=['post'], detail=False)
    # def new_appointment(self, request):
    #     customer_id = request.data['body']['customer_id']
    #     name = getpost(request, 'name')
    #     email = getpost(request, 'email')
    #     phone_number = getpost(request, 'phone_number')
    #     start = datetime.strptime(getpost(request, 'start'), '%Y-%m-%d %H:%M')
    #     end = datetime.strptime(getpost(request, 'end'), '%Y-%m-%d %H:%M')
    #     treatment = getpost(request, 'treatment')
    #     employee_id = getpost(request, 'employee_id')
    #     make_appointment = Appointments.objects.create(customer_id=customer_id,
    #                                              date_booked_start=start, date_booked_end=end,
    #                                              treatment=treatment, employee_id=employee_id)
    #     if customer_id == 0:
    #         make_credentials = Credentials.objects.create(appointment_id=make_appointment.pk, name=name, email=email, phone_number=phone_number)
    #     else:
    #         name = User.objects.get(pk=customer_id).first_name
    #         email = User.objects.get(pk=customer_id).email
    #         # phone_number = User.objects.get(pk=customer_id).phone_number
    #     return Response({"created": True, "name": name, "email": email, "phone_number": phone_number, "date": start})


# def new_barber():
#     name = "Shmoving Test"
#     serializer = Barbers.objects.create(name=name)


# def new_employee():
#     user_id =
#     barber_id =
#     avatar_path = "image.png"
#     last_edit = datetime.now().time()
#     serializer = Barbers.objects.create(user_id=user_id, barber_id=barber_id, avatar_path=avatar_path,
#                                         last_edit=last_edit)


# def new_appointment():
#     user = User.objects.get(id=1)
#     customer_id = user
#     name = "name"
#     email = "email"
#     phone_number = "phone_number"
#     date_booked = datetime.now()
#     booked_time_start = datetime.now().time()
#     booked_time_end = datetime.now().time()
#     treatment_array = "<question1>, <answer1>, <question2>, <answer2>, <question3>, <answer3>, etc..."
#     employee_id = "Yanick"
#     serializer = Appointments.objects.create(customer_id=customer_id, name=name, email=email,
#                                              phone_number=phone_number, date_booked=date_booked,
#                                              booked_time_start=booked_time_start, booked_time_end=booked_time_end,
#                                              treatment_array=treatment_array, employee_id=employee_id)
#
#
# new_appointment()
