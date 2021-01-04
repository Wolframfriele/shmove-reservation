
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from barber.models import Appointments, Credentials, Daily, Openinghours, Timeslices
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


from barber.serializers import AppointmentSerializer
from django.core.files import File
from django.conf import settings
from datetime import datetime
# Create your views here.


def getpost(request, x):
    if request.method == "POST":
        return request.data['body'][x]
    else:
        return request.query_params.get(x)


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
        start = datetime.strptime(
            getpost(request, 'start'), '%d/%m/%Y, %H:%M:%S')
        end = datetime.strptime(getpost(request, 'end'), '%d/%m/%Y, %H:%M:%S')
        # split and send the treatments as string
        treatment = ','.join(getpost(request, 'treatment'))
        employee_id = getpost(request, 'employee_id')

        # create appointment
        make_appointment = Appointments.objects.create(customer_id=customer_id,
                                                       date_booked_start=start, date_booked_end=end,
                                                       treatment=treatment, employee_id=employee_id)
        if customer_id == 0:
            make_credentials = Credentials.objects.create(
                appointment_id=make_appointment.pk, first_name=name, email=email, phone_number=phone_number)
        else:
            # snap de else statement hier niet
            name = User.objects.get(pk=customer_id).first_name
            email = User.objects.get(pk=customer_id).email
            # phone_number = User.objects.get(pk=customer_id).phone_number
        return Response({"created": True, "name": name, "email": email, "phone_number": phone_number, "date": start})

    # @csrf_exempt
    # @action(methods=['post'], detail=False)
    # def get_appointments_customer(self, request):
    #     dates = []
    #     start_day = datetime.strptime(getpost(request, 'start_day'), '%Y-%m-%d')
    #     end_day = datetime.strptime(getpost(request, 'end_day'), '%Y-%m-%d')
    #     employee_id = getpost(request, 'employee_id')
    #     appointments = Appointments.objects.filter(employee_id=employee_id, date_booked_start__gte=start_day,
    #                                                date_booked_start__lte=end_day).values()
    #     for appointment in appointments:
    #         dates.append({'date_end': appointment['date_booked_end'], 'date_start': appointment['date_booked_start']})
    #     return Response(dates)

    # @csrf_exempt
    # @action(methods=['post'], detail=False)
    # def get_appointments_barber(self, request):
    #     the_info = []
    #     start_day = datetime.strptime(getpost(request, 'start_day'), '%Y-%m-%d')
    #     end_day = datetime.strptime(getpost(request, 'end_day'), '%Y-%m-%d')
    #     appointments = Appointments.objects.filter(date_booked_start__gte=start_day,
    #                                                date_booked_start__lte=end_day).values()
    #     for appointment in appointments:
    #         if appointment['customer_id'] == 0:
    #             cust_data = Credentials.objects.get(pk=appointment['id'])
    #         else:
    #             cust_data = User.objects.get(pk=appointment['customer_id'])

    #         the_info.append({'date_end': appointment['date_booked_end'],
    #                          'date_start': appointment['date_booked_start'],
    #                          'done': appointment['done'],
    #                          'treatment': appointment['treatment'],
    #                          'customer_first_name': cust_data.first_name,
    #                          'customer_last_name': cust_data.last_name,
    #                          'customer_email': cust_data.email,
    #                          # phone_number
    #                          'employee_id': appointment['employee_id']
    #                          })
    #     return Response(the_info)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_free_places(self, request):
        """get times from timeslices model on a weekly or monthly base

        Args:
            request ([request]): [contains sended data]

        Returns:
            [arr]: [time slices obj]
        """
        date_times_arr = []
        data = False  # for testing
        start_date = getpost(
            request, 'start') if data else datetime(2020, 12, 14)
        end_date = getpost(
            request, 'start') if data else datetime(2020, 12, 20)

        dailies = Daily.objects.filter(
            Q(date__gte=start_date) & Q(date__lte=end_date) & Q(is_open=1))
        for daily in dailies.values():
            daily_id = daily['id']
            # turn daily date obj to string
            daily_date = daily['date'].strftime('%Y-%m-%d')
            # get time slices
            time_slices = Timeslices.objects.filter(daily__id=daily_id)
            for time_slice in time_slices.values():
                # turn start time and end time datetime obj to string
                # to be able to join it and give it as param in appointment
                time_start = time_slice['slice_start'].strftime('%H:%M:%S')
                time_end = time_slice['slice_end'].strftime('%H:%M:%S')
                # join daily date and timeslices times
                join_date_time_start = daily_date+','+time_start
                join_date_time_end = daily_date+','+time_end
                # turn joined daily date and timeslices times strings to datetime object
                date_time_start = datetime.strptime(
                    join_date_time_start, '%Y-%m-%d,%H:%M:%S')
                date_time_end = datetime.strptime(
                    join_date_time_end, '%Y-%m-%d,%H:%M:%S')

                # check if timeslices exists in appointment
                appointment = Appointments.objects.filter(
                    Q(date_booked_start=date_time_start) &
                    Q(date_booked_end=date_time_end)
                )

                if appointment.count() == 0:
                    # append the formated date time
                    date_times_arr.append(
                        {'start': date_time_start, 'end': date_time_end, 'taked': False, 'appointment_id': None})
                else:
                    # append the formated date time
                    date_times_arr.append({'start': date_time_start, 'end': date_time_end,
                                           'taked': True, 'appointment_id': appointment.values()[0]['id']})

        return Response(date_times_arr)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def block_times_lice(self, request):
        """remove a specific time slice from agenda

        Args:
            request ([request]): [contains sended data]
        Return:
            type: arr: status of the query
        """
        pass

    def get_register_customer_data(self, id):
        """get customer with account data fron the User model

        Args:
            id ([int]): [customer id]
        """
        data = {}

        try:
            # remenber to add a profile model to get register customer tel numer and other info nor available in de User model
            user = User.objects.get(id=id)
            data = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': 'comming soon'
            }
        except:
            data = 'Customer not found'

        return data,

    def get_unregister_customer_data(self, id):
        """get customer without account data fron the Credentials model

        Args:
            id ([int]): [appointment id]
        """
        data = {}

        try:
            credentials = Credentials.objects.get(id=id)
            data = {
                'first_name': credentials.first_name,
                'last_name': credentials.last_name,
                'email': credentials.email,
                'phone_number': credentials.phone_number,
            }
        except:
            data = 'Customer credentials not found'

        return data,

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_appointment_data(self, request):
        """get appointment data and user info

        Args:
            request ([request]): [contains sended data]

        Returns:
            [arr]: [appointment data obj and user info obj]
        """
        appointment_id = request.query_params.get('appointment_id')
        result = []

        try:
            appointment_info = Appointments.objects.get(id=appointment_id)
            # check if customer have an account or not
            if appointment_info.customer_id == 0:
                result.append({
                    'customer': self.get_unregister_customer_data(appointment_info.credentials_id),
                    'appointment': serializers.serialize('json', [appointment_info, ]),
                })
            else:
                result.append({
                    'appointment': self.get_serializer(appointment_info).data,
                    'customer': self.get_register_customer_data(
                        appointment_info.customer_id),
                })
        except:
            result.append('No appointment')

        return Response(result)
