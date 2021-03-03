# Create your views here.
from datetime import datetime, timedelta, date
import time
from decouple import config

from django.contrib.auth.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from django.core.mail import send_mail
# from django.contrib.auth.hashers import make_password
################################## DRF IMPORTS #######################################
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from barber.models import Appointments, Credentials, StandardWeek, TimeSlices, Treatments, Vacations
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


def create_appointment(request):
    dbs_string = getpost(request, 'date_booked_start')
    dbs_strings = dbs_string.split(', ')
    date_ = datetime.strptime(dbs_strings[0], '%d/%m/%Y')
    dbe_string = getpost(request, 'date_booked_end')
    dbe_strings = dbe_string.split(', ')
    time_start = dbs_strings[1]
    time_end = dbe_strings[1]

    treatment = getpost(request, 'treatment')
    reason = getpost(request, 'reason')

    first_name = getpost(request, 'first_name')
    last_name = getpost(request, 'last_name')
    email = getpost(request, 'email')
    phone_number = getpost(request, 'phone_number')

    valid = 0

    if treatment:
        valid += 1
    # if reason:
    #     valid += 1
    if first_name:
        valid += 1
    if last_name:
        valid += 1
    if email:
        valid += 1
    if phone_number:
        valid += 1

    if valid == 5:
        if dbs_string:
            valid += 1
        if dbe_string:
            valid += 1
        if valid == 7:
            get_slice = TimeSlices.objects.get(
                slice_start=time_start, slice_end=time_end).pk
            find_appointment = Appointments.objects.filter(
                date=date_, time_slice_id=get_slice).values()
            if find_appointment:
                return Response({"error": "Appointment_Taken"})
            else:
                try:
                    # credentials were found
                    make_credentials = Credentials.objects.get(email=email)
                except:
                    # credentials were not found
                    make_credentials = Credentials.objects.create(first_name=first_name, last_name=last_name,
                                                                  email=email, phone_number=phone_number)

                Appointments.objects.create(date=date_, start_time=time_start, end_time= time_end,
                                                               time_slice_id=get_slice, treatment=treatment,
                                                               reason=reason, credentials=make_credentials)
                try:
                    test_credentials = Credentials.objects.get(email=email)
                    try:
                        Appointments.objects.get(Q(treatment=treatment) & Q(reason=reason) &
                                                                    Q(credentials=test_credentials) &
                                                                    Q(date=date_) & Q(time_slice_id=get_slice))

                        real_date = datetime.strptime(
                            dbs_string, '%d/%m/%Y, %H:%M:%S').strftime("%d %b, %Y")
                        # sending a confirmation mail
                        port = 465
                        password = config('MAIL_PWD')
                        smtp_server = 'smtp.gmail.com'
                        sender_email = 'wolframfriele@gmail.com'
                        receiver_email = email
                        therapist_email = 'wolframfriele@gmail.com'

                        message = MIMEMultipart("alternative")
                        message["Subject"] = "Bevestiging Afspraak - IN-KI Shiatsu Delft"
                        message["From"] = sender_email
                        message["To"] = receiver_email

                        message_t = MIMEMultipart("alternative")
                        message_t["Subject"] = "Nieuwe Afspraak - {} {}".format(
                            first_name, last_name)
                        message_t["From"] = therapist_email
                        message_t["To"] = therapist_email

                        # Create the plain-text and HTML version of your message
                        text = """\
                            Beste heer/mevrouw {} {},\n
                        \n
                        Hartelijk bedankt voor uw online boeking bij IN-KI Shiatsu Delft!\n
                        We hebben uw boeking met de volgende details mogen ontvangen:\n
                        Afspraak voor: {}\n
                        Datum: {}\n
                        Tijd: {}\n
                        Opmerkingen/reden van bezoek: {}\n
                        Een aantal dagen voor de behandeling ontvangt u nog een mail met uitgebreide informatie.\n
                        Annuleren is kosteloos tot 48 uur van tevoren, daarna wordt de gereserveerde tijd in principe in rekening gebracht.\n
                        IN-KI Shiatsu Delft werkt in Corona tijd volgens de richtlijnen van het RIVM.\n
                        Heeft u nog vragen, laat het me weten!\n
                        \n
                        \n
                        \n
                        Hartelijke groet,\n
                        Inge Oostenbrink\n
                        \n
                        \n
                        IN-KI Shiatsu Delft\n
                        Doelenstraat 16\n
                        2611 NT Delft\n
                        \n
                        www.shiatsu-delft.nl\n
                        inge@shiatsu-delft.nl\n
                        06 4070 2497\n
                        """.format(first_name, last_name, treatment, real_date, time_start, reason)
                        html = """
                        <html><body>
                            <p>Beste heer/mevrouw {} {}, </p>
                            <br>
                            <p>Hartelijk bedankt voor uw online boeking bij IN-KI Shiatsu Delft!</p>
                            <p>We hebben uw boeking met de volgende details mogen ontvangen:</p>
                            <br>
                            <b><ul><li>Afspraak voor: {}</li>
                            <li>Datum: {}</li>
                            <li>Tijd: {}</li>
                            <li>Opmerkingen/reden van bezoek: {}</li></ul></b>
                            <p>Een aantal dagen voor de behandeling ontvangt u nog een mail met uitgebreide informatie.</p>
                            <p>Annuleren is kosteloos tot 48 uur van tevoren, daarna wordt de gereserveerde tijd in principe in rekening gebracht.</p>
                            <p>IN-KI Shiatsu Delft werkt in Corona tijd volgens de richtlijnen van het RIVM.</p>
                            <p>Heeft u nog vragen, laat het me weten!</p>
                            <br>
                            <br>
                            <br>
                            <p>Hartelijke groet,</p>
                            <p>Inge Oostenbrink</p>
                            <br>
                            <br>
                            <p>
                            IN-KI Shiatsu Delft<br>
                            Doelenstraat 16<br>
                            2611 NT Delft<br>
                            </p>
                    
                            <a href="https://www.shiatsu-delft.nl">www.shiatsu-delft.nl</a><br>
                            <a href="mailto:inge@shiatsu-delft.nl">inge@shiatsu-delft.nl</a><br>
                            <a href="tel:0640702497">06 4070 2497</a><br>
                        </body></html>
                        """.format(first_name, last_name, treatment, real_date, time_start, reason)

                        text_t = """\
                            {} {} heeft een afspraak gemaakt op {} om {}.
                            De gekozen behandeling is {} met de reden:
                            {}
                        """.format(first_name, last_name, real_date, time_start, treatment, reason)
                        html_t = """\
                        <html><body>
                        <p><b>{} {}</b> heeft een afspraak gemaakt op <b>{}</b> om <b>{}</b>.</p>
                        <p>De gekozen behandeling is <b>{}</b> met de reden:<br>
                            {}
                        </p></body></html>
                        """.format(first_name, last_name, real_date, time_start, treatment, reason)

                        # Turn these into plain/html MIMEText objects
                        part1 = MIMEText(text, "plain")
                        part2 = MIMEText(html, "html")
                        part1_t = MIMEText(text_t, "plain")
                        part2_t = MIMEText(html_t, "html")

                        # Add HTML/plain-text parts to MIMEMultipart message
                        # The email client will try to render the last part first
                        message.attach(part1)
                        message.attach(part2)
                        message_t.attach(part1_t)
                        message_t.attach(part2_t)

                        # Create a secure SSL context
                        context = ssl.create_default_context()

                        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                            server.login(sender_email, password)
                            server.sendmail(
                                sender_email, receiver_email, message.as_string())
                            server.sendmail(
                                therapist_email, therapist_email, message_t.as_string())

                        return Response({"error": "None",
                                         "first_name": first_name,
                                         "email": email,
                                         "phone_number": phone_number,
                                         "date": date_,
                                         "time_start": time_start,
                                         "time_end": time_end})

                    except Appointments.DoesNotExist:
                        return Response({"error": "Appointment_Failed"})
                except Credentials.DoesNotExist:
                    return Response({"error": "Credentials_Failed"})
        else:
            return Response({"error": "Empty_Internal_Field"})
    else:
        return Response({"error": "Empty_Field"})


class DashboardAppointmentView(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_appointment(self, request):
        return create_appointment(request)

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def cancel_appointment(self, request):
        appointment = getpost(request, 'appointment_id')
        try:
            Appointments.objects.get(pk=appointment).delete()
            msg = 'Success'
        except:
            msg = 'Fail'
        return Response(msg)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_appointments(self, request):
        # get variables
        start_search_date = parse_date(getpost(request, 'beginweek'))
        end_search_date = parse_date(getpost(request, 'endweek'))
        search_duration = end_search_date - start_search_date
        today = date.today()
        search_array = []

        # fill array with dates to be searched in
        for i in range(search_duration.days + 1):
            day = start_search_date + timedelta(days=i)
            search_array.append(day)

        events = []

        # get the vacations

        vacations = Vacations.objects.filter(
                            start_date__lte=end_search_date, end_date__gte=start_search_date).values()

        if len(vacations) > 0:

            for vacation in vacations:
                # add the vacations to event array
                events.append({"type": "2",
                               "start": "{} 9:30".format(vacation['start_date']),
                               "end": "{} 20:00".format(vacation['end_date']),
                               "name": "{}".format(vacation['name'])
                               })
                # remove vacations from search array
                vacation_duration = vacation['end_date'] - vacation['start_date']

                for i in range(vacation_duration.days + 1):
                    day = vacation['start_date'] + timedelta(days=i)
                    if day in search_array:
                        search_array.remove(day)

        # Check for appointments
        for search_date in search_array:
            if search_date <= today:
                try:
                    appointments = Appointments.objects.filter(date=search_date)
                    if len(appointments) > 0:
                        for appointment in appointments:
                            if not appointment.blocked:
                                credentials = Credentials.objects.get(pk=appointment.credentials.pk)
                                events.append({"type": "0",
                                               "start": "{} {}".format(appointment.date, appointment.start_time),
                                               "end": "{} {}".format(appointment.date, appointment.end_time),
                                               "name": "{} {}".format(credentials.first_name, credentials.last_name),
                                               "appointment_id": "{}".format(appointment.pk)
                                               })
                except:
                    pass

            else:
                # Find the day's time slices
                weekday = search_date.weekday() + 1
                slices = TimeSlices.objects.filter(standardweek__pk=weekday)
                try:
                    max_appointment = StandardWeek.objects.get(pk=weekday).slice_count
                    
                except:
                    max_appointment = 0

                appointments = Appointments.objects.filter(date=search_date)
                if len(appointments) == 0:
                    for slice in slices:
                        events.append({"type": "1",
                                       "start": "{} {}".format(search_date, slice.slice_start),
                                       "end": "{} {}".format(search_date, slice.slice_end)
                                       })
                else:
                    appointment_counter = 0
                    for appointment in appointments:
                        if appointment.blocked:
                            events.append({"type": "3",
                                           "start": "{} {}".format(appointment.date, appointment.start_time),
                                           "end": "{} {}".format(appointment.date, appointment.end_time),
                                           "appointment_id": "{}".format(appointment.pk)
                                           })
                            slices = slices.exclude(pk=appointment.time_slice.pk)
                        else:
                            credentials = Credentials.objects.get(pk=appointment.credentials.pk)
                            events.append({"type": "0",
                                           "start": "{} {}".format(appointment.date, appointment.start_time),
                                           "end": "{} {}".format(appointment.date, appointment.end_time),
                                           "name": "{} {}".format(credentials.first_name, credentials.last_name),
                                           "appointment_id": "{}".format(appointment.pk)
                                           })
                            slices = slices.exclude(pk=appointment.time_slice.pk)
                            appointment_counter += 1

                    if appointment_counter < max_appointment:
                        for slice in slices:
                            events.append({"type": "1",
                                           "start": "{} {}".format(search_date, slice.slice_start),
                                           "end": "{} {}".format(search_date, slice.slice_end)
                                           })
                    else:
                        for slice in slices:
                            events.append({"type": "4",
                                           "start": "{} {}".format(search_date, slice.slice_start),
                                           "end": "{} {}".format(search_date, slice.slice_end)
                                           })
        return Response(events)


    @csrf_exempt
    @action(methods=['post'], detail=False)
    def change_appointment(self, request):
        # get variables
        appointment_id = getpost(request, 'appointment_id')
        begin_time = getpost(request, 'begin_time')
        end_time = getpost(request, 'end_time')
        treatment = getpost(request, 'treatment')
        customer_id = getpost(request, 'customer_id')
        reason = getpost(request, 'reason')

        appointment = Appointments.objects.get(pk=appointment_id)
        appointment.start_time = begin_time
        appointment.end_time = end_time
        appointment.treatment = treatment
        appointment.reason = reason
        appointment.credentials_id = customer_id
        appointment.save()

        return Response("SUCCESS")


    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_appointment_data(self, request):
        appointment_id = request.query_params.get('appointment_id')
        result = []

        appointment = Appointments.objects.get(id=appointment_id)
        credential = Credentials.objects.get(id=appointment.credentials_id)

        result.append({
            "date": appointment.date,
            "start_time": appointment.start_time,
            "end_time": appointment.end_time,
            "blocked": appointment.blocked,
            "treatment": appointment.treatment,
            "reason": appointment.reason,
            "credential_id": appointment.credentials_id,
            "first_name": credential.first_name,
            "last_name": credential.last_name,
            "email": credential.email,
            "phone_number": credential.phone_number
        })

        return Response(result)


    @csrf_exempt
    @action(methods=['post'], detail=False)
    def block_appointment(self, request):
        dbs_string = getpost(request, 'start')
        dbs_strings = dbs_string.split(' ')
        date_ = datetime.strptime(dbs_strings[0], '%Y-%m-%d')
        dbe_string = getpost(request, 'end')
        dbe_strings = dbe_string.split(' ')
        time_start = dbs_strings[1]
        time_end = dbe_strings[1]

        get_slice = TimeSlices.objects.get(
            slice_start=time_start, slice_end=time_end).pk

        Appointments.objects.create(date=date_, start_time=time_start, end_time=time_end,
                                    time_slice_id=get_slice, blocked=True)
        result = "blocked"
        return Response(result)


    @csrf_exempt
    @action(methods=['post'], detail=False)
    def set_vacation(self, request):
        name = getpost(request, 'name')
        start_date = parse_date(getpost(request, 'start_date'))
        end_date = parse_date(getpost(request, 'end_date'))
        delta = timedelta(days=1)
        date_ = start_date
        while date_ <= end_date:
            try:
                Appointments.objects.get(date=date_)
                return Response("Error_Appointment")
            except:
                pass
            date_ += delta
        try:
            Vacations.objects.get(start_date=start_date, end_date=end_date)
            return Response("Error_Vacation")
        except:
            Vacations.objects.create(
                name=name, start_date=start_date, end_date=end_date)
        return Response("Success")

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_vacations(self, request):
        vacations = []
        all_vacations = Vacations.objects.filter().values()
        for i in all_vacations:
            vacations.append({"id": i['id'],
                              "name": i['name'],
                              "start_date": i['start_date'],
                              "end_date": i['end_date']})
        return Response(vacations)

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def change_vacation(self, request):
        vacation_id = getpost(request, 'id')
        name = getpost(request, 'name')
        start_date = parse_date(getpost(request, 'start_date'))
        end_date = parse_date(getpost(request, 'end_date'))
        try:
            vacation = Vacations.objects.get(pk=vacation_id)
            vacation.name = name
            vacation.start_date = start_date
            vacation.end_date = end_date
            vacation.save()
        except:
            return Response('Fail')
        return Response('Success')

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def delete_vacation(self, request):
        vacation_id = getpost(request, 'id')
        try:
            Vacations.objects.filter(pk=vacation_id).delete()
        except:
            return Response('Fail')
        return Response('Success')


class AppointmentsView(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_appointment(self, request):
        return create_appointment(request)


    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_appointments_customer(self, request):
        # get variables
        start_search_date = parse_date(getpost(request, 'beginweek'))
        end_search_date = parse_date(getpost(request, 'endweek'))
        today = date.today()

        events = []
        search_array = []

        # set search duration
        # if the whole request duration is in the past return no events
        if end_search_date < today:
            return Response(events)

        # if today is halfway through the request duration, only return events after today
        elif start_search_date < today:
            search_duration = end_search_date - today

            # fill array with dates to be searched in
            for i in range(search_duration.days):
                day = (today + timedelta(days=1)) + timedelta(days=i)
                search_array.append(day)

        # if the entire request duration is in the future, return events for all days
        else:
            search_duration = end_search_date - start_search_date

            # fill array with dates to be searched in
            for i in range(search_duration.days + 1):
                day = start_search_date + timedelta(days=i)
                search_array.append(day)

        # get the vacations

        vacations = Vacations.objects.filter(
                            start_date__lte=end_search_date, end_date__gte=start_search_date).values()

        if len(vacations) > 0:
            for vacation in vacations:
                # remove vacations from search array
                vacation_duration = vacation['end_date'] - vacation['start_date']

                for i in range(vacation_duration.days + 1):
                    day = vacation['start_date'] + timedelta(days=i)
                    if day in search_array:
                        search_array.remove(day)

        # Check for appointments
        for search_date in search_array:
            # Find the day's time slices
            weekday = search_date.weekday() + 1
            try:
                max_appointment = StandardWeek.objects.get(pk=weekday).slice_count
            except:
                max_appointment = 0
            slices = TimeSlices.objects.filter(standardweek__pk=weekday)

            appointments = Appointments.objects.filter(date=search_date)
            if len(appointments) == 0:
                for slice in slices:
                    events.append({"start": "{} {}".format(search_date, slice.slice_start),
                                   "end": "{} {}".format(search_date, slice.slice_end)
                                   })
            else:
                appointment_counter = 0
                for appointment in appointments:
                    if appointment.blocked:
                        slices = slices.exclude(pk=appointment.time_slice.pk)
                    else:
                        slices = slices.exclude(pk=appointment.time_slice.pk)
                        appointment_counter += 1

                if appointment_counter < max_appointment:
                    for slice in slices:
                        events.append({"start": "{} {}".format(search_date, slice.slice_start),
                                       "end": "{} {}".format(search_date, slice.slice_end)
                                       })
        return Response(events)
