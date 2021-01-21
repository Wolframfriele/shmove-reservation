from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core import serializers
from django.db.models import Q
from django.http import QueryDict
import json
from datetime import datetime, timedelta
# from django.contrib.auth.hashers import make_password
################################## DRF IMPORTS #######################################
from rest_framework import viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from dashboard.serializers import DashboardSerializer
from barber.models import Appointments, Credentials, Changes, StandardWeek, TimeSlices, Treatments
from barber.serializers import AppointmentSerializer

# Create your views here.


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    email = request.data['body']['email']
    password = request.data['body']['password']
    # get username and password count
    email_count = User.objects.filter(email=email).count()
    passsword_count = User.objects.filter(password=password).count()
    # check if user given email ans password exist in DB
    if email_count != 0:
        # verify if the user given password is correct
        currentUser = User.objects.get(email=email)
        if currentUser.check_password(password):
            # get username
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            # userToken(request, user)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,
                                 'id': token.user_id,
                                 'is_superuser': request.user.is_superuser,
                                 'authenticate': True},
                                status=HTTP_200_OK)
            else:
                print('Gebruiker bestaat niet')
        else:
            passwordContext = {
                'authenticate': False,
                'ww': password,
                'msg': 'Wachtwoord onjuist'
            }
            return Response(passwordContext)
    else:
        emailContext = {
            'authenticate': False,
            'msg': 'Email onjuist'
        }
        return Response(emailContext)


class DashboardView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]

    # @csrf_exempt
    # @action(methods=['post'], detail=False)
    # def signup(self, request):
    #     """[
    #         create new user account
    #     ]
    #     Arguments:
    #         request {[form data]} -- [contains formated user form data]
    #     Returns:
    #         [dict] -- [ser account created status and accounts data]
    #     """
    #     # user signup data
    #     username = request.data['body']['username']
    #     email = request.data['body']['email']
    #     password = request.data['body']['password']

    #     if request.user is not None:
    #         # check if user already exist
    #         user_exist = user = User.objects.filter(
    #             Q(email=email) and Q(username=username)).count()
    #         if user_exist == 0:
    #             user = User.objects.create_user(
    #                 username=username, email=email, password=password, is_superuser=1, is_staff=1)

    #             token, _ = Token.objects.get_or_create(user=user)
    #             # log user in
    #             authenticate(username=username, password=password)
    #             return Response({'token': token.key,
    #                              'id': token.user_id,
    #                              'is_superuser': True,
    #                              'created': True},
    #                             status=HTTP_200_OK)
    #         else:
    #             return Response({'msg': 'Gebruikersnaam en/of Email bestaat al', 'created': False})

    #     else:
    #         return Response({'msg': 'Gebruikersnaam en/of Email bestaat al', 'created': False})

    @action(methods=['get'], detail=False)
    # @permission_classes((IsAuthenticated,))
    def signout(self, request):
        logout(request)
        return Response({'logout': True})

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def check_token(self, request):
        token_key = request.query_params.get('token')

        token = Token .objects.filter(key=token_key).count()
        if token > 0:
            return Response({'token': True})
        else:
            return Response({'token': False})

    def get_date_from_day(self, day_index):
        """get the date from a day index(0->monday, ... , 6->sunday)

        Args:
            day_index ([int]): [0->monday, ... , 6->sunday]

        Returns:
            [datetime obj]: [date]
        """
        date = None
        b_week = datetime.today() - timedelta(
            days=datetime.today().weekday() % 7
        )  # begin of week

        for d in range(7):
            # add 1 day to the begin day of the week
            updated_day = b_week + timedelta(days=d)
            if updated_day.weekday() == day_index:
                date = updated_day.date()

        return date

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_treatments(self, request):
        """
        get all treatments from DB

        Args:
            request (request): [request data dict]
        """
        treatments_arr = []
        treatments = Treatments.objects.all().values()

        for t in treatments:
            treatments_arr.append(
                {
                    'id': t['id'],
                    'treatment': t['treatment'],
                    'price': t['price']
                }
            )

        return Response(treatments_arr)

    @csrf_exempt
    @action(methods=['put'], detail=False)
    def update_treatments(self, request):
        """
        update treatment if it exists otherwise add it to DB

        Args:
            request (request): [request data dict]
        """
        treatment_name = request.data['body']['name']
        treatment_price = request.data['body']['price']

        update, created = Treatments.objects.update_or_create(
            treatment=treatment_name,
            defaults={'treatment': treatment_name, 'price': treatment_price}
        )

        if created:
            return Response({'msg': 'Behandeling {} aangemaakt'.format(treatment_name)})
        else:
            return Response({'msg': 'Behandeling {} aangepast'.format(treatment_name)})

    @csrf_exempt
    @action(methods=['delete'], detail=False)
    def delete_treatments(self, request):
        """
        remove a treatment from DB

        Args:
            request (request): [request data dict]
        """
        treatment_id = int(request.query_params.get('id'))

        treatment = Treatments.objects.filter(id=treatment_id).delete()

        if treatment:
            return Response({'msg': 'Behandeling verwijderd'})
        else:
            return Response({'msg': 'Er is iets mis gegaan'})

    # get days name from date: day=date.strftime('%A')
    # @csrf_exempt
    # @action(methods=['post'], detail=False)
    # def generate_week_dates(self, request):
    #     """
    #     take the begin, end current week dates and dates in between
    #     and generate them in the StandardWeek and StandardWeek_slices many to many table
    #
    #     Args:
    #         request ([request]): [request data]
    #
    #     Returns:
    #         [Response]: [retrun confirmation]
    #     """
    #     week_dates = []
    #     b_week = datetime.today() - timedelta(
    #         days=datetime.today().weekday() % 7
    #     )  # begin of week
    #     e_week = b_week + timedelta(days=6)  # end of week
    #     # get standard time slices
    #     timeslices = TimeSlices.objects.all()
    #     # generate current week dates
    #     for i in range(7):
    #         dates = b_week + timedelta(days=i)
    #         week_dates.append(dates.date())
    #     # check if Changes entity has already data in it
    #     if WeekDates.objects.all().count() == 0:
    #         for date in week_dates:
    #             # create 7 date in Changes base on the current week
    #             sd = WeekDates.objects.create(date=date)
    #             # add the standart time slices to the changes
    #             for ts in timeslices:
    #                 sd.slices.add(ts)
    #     else:
    #         if WeekDates.objects.filter(date=b_week).count() == 0:
    #             # delte all record in Changes table
    #             WeekDates.objects.all().delete()
    #             # delete all related many to many relationship record
    #             # regenerate
    #             self.generate_week_dates(request)
    #
    #     return Response('changes for {} to {} generated'.format(b_week, e_week))

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def add_time_slices(self, request):
        params = request.data['body']

        b_time = datetime.strptime(
            params['begin_time'], '%H:%M:%S').time()
        e_time = datetime.strptime(
            params['end_time'], '%H:%M:%S').time()
        day_index = int(params['day_index'])
        # get begin and end week date
        b_week = datetime.today() - timedelta(days=datetime.today().weekday() %
                                              7)  # begin of week
        # e_week = b_week + timedelta(days=6)  # end of week

        # store the date base on the sended day
        current_date = self.get_date_from_day(day_index)

        # create new Changes
        # changes = Changes.objects.get_or_create(date=current_date)
        # changes.save()
        try:
            changes = Changes.objects.get(date=current_date)
            # check if time slice exists
            ts = TimeSlices.objects.filter(
                Q(slice_start=b_time) & Q(slice_end=e_time))
            if ts.count() == 0:
                # add time slice
                new_slice = TimeSlices(slice_start=b_time, slice_end=e_time)
                new_slice.save()
                # add slice to changes
                changes.slices.add(new_slice)

                return Response({'added': True, 'msg': 'tijdslot toegevoegd'})
            else:
                return Response({'added': False, 'msg': 'tijdslot {} - {} bestaat al'.format(b_time, e_time)})
        except Changes.DoesNotExist:
            changes = Changes.objects.create(date=current_date)
            changes.save()
            # add time slice
            new_slice = TimeSlices(slice_start=b_time, slice_end=e_time)
            new_slice.save()
            # add slice to changes
            changes.slices.add(new_slice)

            return Response({'added': True, 'msg': 'tijdslot toegevoegd'})

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_timeslices(self, request):
        days_arr = ['monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
        slices_arr = []
        # get the standard weeks
        s_weeks = StandardWeek.objects.all().values()
        for i, s_week in enumerate(s_weeks):
            ts = TimeSlices.objects.filter(
                standardweek=s_week['id']).values()
            for tsl in ts:
                # print(
                #     {'bt': tsl['slice_start'], 'et': tsl['slice_end'], 'day': days_arr.index(days_arr[i])})
                slices_arr.append(
                    {
                        'start': tsl['slice_start'],
                        'end': tsl['slice_end'],
                        'day_id': days_arr.index(days_arr[i]),
                        'slice_id': tsl['id']
                    }
                )

        return Response(slices_arr)

    @csrf_exempt
    @action(methods=['put'], detail=False)
    def update_timeslices(self, request):
        # params = QueryDict(request.body)
        params = request.data['body']

        b_time = datetime.strptime(
            params['begin_time'], '%H:%M:%S').time()
        e_time = datetime.strptime(
            params['end_time'], '%H:%M:%S').time()
        slice_id = int(params['slice_id'])
        day_index = int(params['day_id'])
        # get date from day index
        date = self.get_date_from_day(day_index)
        # get changes base on date
        week_date = WeekDates.objects.filter(date=date).values()
        # check if changes exists
        if week_date.count() > 0:
            # filter and update slice
            TimeSlices.objects.filter(
                Q(changes__id=week_date[0]['id'])
                & Q(id=slice_id)
            ).update(slice_start=b_time, slice_end=e_time)

        return Response({'changed': True})

    @csrf_exempt
    @action(methods=['delete'], detail=False)
    # @permission_classes((AllowAny,))
    def remove_timeslices(self, request):
        params = request.query_params

        slice_id = int(params.get('slice_id'))
        day_index = int(params.get('day_id'))
        # get date from day index
        date = self.get_date_from_day(day_index)
        # get changes base on date
        change = WeekDates.objects.filter(date=date).values()
        # filter and delete slice
        TimeSlices.objects.filter(
            Q(changes__id=change[0]['id'])
            & Q(id=slice_id)
        ).delete()

        return Response({'deleted': True})
