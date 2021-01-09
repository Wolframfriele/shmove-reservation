# Create your views here.
from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from django.core.mail import send_mail
# from django.contrib.auth.hashers import make_password
################################## DRF IMPORTS #######################################
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

from barber.models import Appointments, Credentials, Changes, StandardWeek, TimeSlices, Treatments
from barber.serializers import AppointmentSerializer

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create your views here.


def getpost(request, x):
    if request.method == 'POST':
        return request.data['body'][x]
    else:
        return request.query_params.get(x)


# serializers.serialize('json', appointments)


class AppointmentsView(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_appointment(self, request):
        treatment_arr = []
        dbs_string = getpost(request, 'date_booked_start')
        dbs_strings = dbs_string.split(',')
        # => de datum komt vanaf de frontend op deze format: %d/%m/%Y
        # => en de Db heeft deze format %Y-%m-%d nodig. vandaar de onderstaan wijzigingen
        # => convert date to datetinme object
        date_obj = datetime.strptime(dbs_strings[0], '%d/%m/%Y').date()
        # => get date and change format
        date_ = date_obj.strftime('%Y-%m-%d')
        dbe_string = getpost(request, 'date_booked_end')
        dbe_strings = dbe_string.split(',')
        # => remove leading whitespace in splited daet time
        time_start = dbs_strings[1].strip()
        # => remove leading whitespace in splited daet time
        time_end = dbe_strings[1].strip()

        # return Response('hallo')

        treatment = getpost(request, 'treatment')
        reason = getpost(request, 'reason')

        first_name = getpost(request, 'first_name')
        last_name = getpost(request, 'last_name')
        email = getpost(request, 'email')
        phone_number = getpost(request, 'phone_number')

        valid = 0

        if treatment:
            valid += 1
        if reason:
            valid += 1
        if first_name:
            valid += 1
        if last_name:
            valid += 1
        if email:
            valid += 1
        if phone_number:
            valid += 1

        if valid == 6:
            if dbs_string:
                valid += 1
            if dbe_string:
                valid += 1
            if valid == 8:
                get_slice = TimeSlices.objects.get(
                    slice_start=time_start, slice_end=time_end).pk
                find_appointment = Appointments.objects.filter(
                    date=date_, time_slice_id=get_slice).values()
                if find_appointment:
                    return Response({"error": "Appointment_Taken"})
                else:
                    try:
                        # credentials were found
                        make_credentials = Credentials.objects.get(first_name=first_name, last_name=last_name,
                                                                   email=email, phone_number=phone_number)
                    except:
                        # credentials were not found
                        make_credentials = Credentials.objects.create(first_name=first_name, last_name=last_name,
                                                                      email=email, phone_number=phone_number)

                    treatment_ = Treatments.objects.get(treatment=treatment[0])
                    make_appointment = Appointments.objects.create(time_slice_id=get_slice, treatment=treatment_,
                                                                   reason=reason, credentials=make_credentials,
                                                                   date=date_)

                    # => heb test_appointment en test_credentials om te checken of het toevoegen goed gegaan is of niet eruit gehaald
                    # => je zou een try en except bij Appointments.objects.create met een exception InternalError
                    # => om te checken of het toevoeging goed ging
                    # => meer info: https://docs.djangoproject.com/en/3.1/ref/exceptions/
                    real_date = datetime.strptime(
                        dbs_string, '%d/%m/%Y, %H:%M:%S').strftime("%d %b, %Y")
                    # sending a confirmation mail
                    port = 465
                    password = 'donthackme1'
                    smtp_server = 'smtp.gmail.com'
                    sender_email = 'trojo.mailtesting@gmail.com'
                    receiver_email = email

                    message = MIMEMultipart("alternative")
                    message["Subject"] = "Bevestiging Afspraak - IN-KI Shiatsu Delft"
                    message["From"] = sender_email
                    message["To"] = receiver_email

                    # Create the plain-text and HTML version of your message
                    text = """\
                            Bedankt voor het maken van een afspraak bij IN-KI Shiatsu Delft, {}.<br><br>
                                De afspraak is op {} om {}.<br>
                                U heeft gekozen voor {}.<br>
                                Met de reden '{}'.
                            """.format(first_name, real_date, time_start, treatment_, reason)
                    html = """\
                            <html><body><p>
                                Bedankt voor het maken van een afspraak bij IN-KI Shiatsu Delft, {}.<br><br>
                                De afspraak is op {} om {}.<br>
                                U heeft gekozen voor {}.<br>
                                Met de reden '{}'.
                            </p></body></html>
                            """.format(first_name, real_date, time_start, treatment_, reason)

                    # Turn these into plain/html MIMEText objects
                    part1 = MIMEText(text, "plain")
                    part2 = MIMEText(html, "html")

                    # Add HTML/plain-text parts to MIMEMultipart message
                    # The email client will try to render the last part first
                    message.attach(part1)
                    message.attach(part2)

                    # Create a secure SSL context
                    context = ssl.create_default_context()

                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(
                            sender_email, receiver_email, message.as_string())

                    return Response({"error": "None",
                                     "first_name": first_name,
                                     "email": email,
                                     "phone_number": phone_number,
                                     "date": date_,
                                     "time_start": time_start,
                                     "time_end": time_end})
                    # try:
                    #     test_credentials = Credentials.objects.get(first_name=first_name, last_name=last_name,
                    # except:
                    #     return Response({"error": "Credentials_Failed"})
            else:
                return Response({"error": "Empty_Internal_Field"})
        else:
            return Response({"error": "Empty_Field"})

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_appointments(self, request):
        # get variables
        date_ = parse_date(getpost(request, 'beginweek'))
        endweek = parse_date(getpost(request, 'endweek'))
        delta = timedelta(days=1)

        date_timeslices = []
        # get the day of the week
        weekday = 1
        today_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
        # get today's date
        today_date = parse_date(today_datetime[0])
        current_time = parse_time(today_datetime[1])
        while date_ <= endweek:
            print("BIG loop start ----------------------------------------")
            count = 0
            print('count = ', count)
            try:
                if_changes = Changes.objects.get(date=date_).slice_count
                slice_count = int(if_changes)
                slices = TimeSlices.objects.filter(
                    changes__date=date_).values()
                print("there were changes")
            except:
                # get the timeslices from the standardweek using the day value
                slice_count = StandardWeek.objects.get(pk=weekday).slice_count
                slices = TimeSlices.objects.filter(
                    standardweek__pk=weekday).values()
                print("there were no changes")
            print("slice_count = ", slice_count)
            # test if there is still enough room for more appointments
            for i in slices:
                appointment_slices = Appointments.objects.filter(
                    time_slice_id=i['id'], date=date_)
                if appointment_slices:
                    count += 1
            print('count = ', count)
            if count < slice_count:
                available = 1
            else:
                available = 0
            print("available = ", available)
            county_boi = 0
            for i in slices:
                print(" - small loop start -")
                county_boi += 1
                try:
                    appointment_slices = Appointments.objects.get(
                        time_slice_id=i['id'], date=date_).pk
                except:
                    appointment_slices = 0
                taken = appointment_id = 0
                if appointment_slices > 0:
                    taken = 1
                    appointment_id = appointment_slices
                print("   taken = ", taken)
                print("   appointment_id = ", appointment_id)
                slice_data = TimeSlices.objects.filter(pk=county_boi).values()
                date_timeslices.append({"start": "{} {}".format(date_, slice_data[0]["slice_start"]),
                                        "end": "{} {}".format(date_, slice_data[0]["slice_end"]),
                                        "appointment_id": appointment_id,
                                        "taken": taken,
                                        "available": available})
            date_ += delta
            weekday += 1
            print("date = ", date_)
            if weekday == 8:
                weekday = 1
            print("weekday = ", weekday)
        return Response(date_timeslices)
