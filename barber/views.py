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

from barber.models import Appointments, Credentials, Changes, StandardWeek, TimeSlices, Treatments, Vacations
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
                treatment_ = Treatments.objects.get(treatment=treatment)
                make_appointment = Appointments.objects.create(time_slice_id=get_slice, treatment=treatment_,
                                                               reason=reason, credentials=make_credentials,
                                                               date=date_)
                try:
                    test_credentials = Credentials.objects.get(first_name=first_name, last_name=last_name,
                                                               email=email, phone_number=phone_number)
                    try:
                        test_appointment = Appointments.objects.get(Q(treatment=treatment_) & Q(reason=reason) &
                                                                    Q(credentials=test_credentials) &
                                                                    Q(date=date_) & Q(time_slice_id=get_slice))
                        real_date = datetime.strptime(
                            dbs_string, '%d/%m/%Y, %H:%M:%S').strftime("%d %b, %Y")
                        # sending a confirmation mail
                        port = 465
                        password = config('MAIL_PWD')
                        smtp_server = 'smtp.gmail.com'
                        sender_email = 'trojo.mailtesting@gmail.com'
                        receiver_email = email
                        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA (change me)
                        therapist_email = 'tijmen.simons@gmail.com'

                        message = MIMEMultipart("alternative")
                        message["Subject"] = "Bevestiging Afspraak - IN-KI Shiatsu Delft"
                        message["From"] = sender_email
                        message["To"] = receiver_email

                        message_t = MIMEMultipart("alternative")
                        message_t["Subject"] = "Nieuwe Afspraak - {} {}".format(
                            first_name, last_name)
                        message_t["From"] = sender_email
                        message_t["To"] = receiver_email

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
                        """.format(first_name, last_name, treatment_.treatment, real_date, time_start, reason)
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
                        """.format(first_name, last_name, treatment_.treatment, real_date, time_start, reason)

                        text_t = """\
                            {} {} heeft een afspraak gemaakt op {} om {}.
                            De gekozen behandeling is {} met de reden:
                            {}
                        """.format(first_name, last_name, real_date, time_start, treatment_, reason)
                        html_t = """\
                        <html><body>
                        <p><b>{} {}</b> heeft een afspraak gemaakt op <b>{}</b> om <b>{}</b>.</p>
                        <p>De gekozen behandeling is <b>{}</b> met de reden:<br>
                            {}
                        </p></body></html>
                        """.format(first_name, last_name, real_date, time_start, treatment_, reason)

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
                                sender_email, therapist_email, message_t.as_string())

                        return Response({"error": "None",
                                         "first_name": first_name,
                                         "email": email,
                                         "phone_number": phone_number,
                                         "date": date_,
                                         "time_start": time_start,
                                         "time_end": time_end})
                    except:
                        return Response({"error": "Appointment_Failed"})
                except:
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
        start_date = parse_date(getpost(request, 'beginweek'))
        date_ = start_date
        end_date = parse_date(getpost(request, 'endweek'))
        delta = timedelta(days=1)

        date_timeslices = []
        # get the day of the week
        weekday = 1
        today_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
        # get today's date
        today_date = parse_date(today_datetime[0])
        current_time = parse_time(today_datetime[1])
        while date_ <= end_date:
            count = 0
            # check for changes
            try:
                if_changes = Changes.objects.get(date=date_).slice_count
                slice_count = int(if_changes)
                slices = TimeSlices.objects.filter(
                    changes__date=date_).values()
            except:
                # get the timeslices from the standardweek using the day value
                slice_count = StandardWeek.objects.get(pk=weekday).slice_count
                slices = TimeSlices.objects.filter(
                    standardweek__pk=weekday).values()
            # get the amount of appointments made for today to check if there is is still room left
            for i in slices:
                appointment_slices = Appointments.objects.filter(
                    time_slice_id=i['id'], date=date_)
                if appointment_slices:
                    count += 1
            for i in slices:
                slice_data = TimeSlices.objects.filter(pk=i['id']).values()
                # the check if there is still room left
                if count < slice_count and date_ > today_date:
                    available = 1
                    # check to see if there is a vacation
                    try:
                        vacations = Vacations.objects.filter(
                            start_date__lte=date_, end_date__gte=date_).values()
                        if vacations[0]:
                            available = 0
                    except:
                        pass
                else:
                    available = 0
                first_name = ""
                last_name = ""
                treatment = ""
                # get the appointment, if there is one, and get the name and treatment
                try:
                    appointment_slices = Appointments.objects.get(time_slice_id=i['id'], date=date_)
                    appointment_slices_id = appointment_slices.pk
                    credentials = Credentials.objects.get(pk=appointment_slices.credentials.pk)
                    first_name = credentials.first_name
                    last_name = credentials.last_name
                except:
                    appointment_slices_id = 0

                taken = appointment_id = 0
                if appointment_slices_id > 0:
                    taken = 1
                    appointment_id = appointment_slices_id
                    treatment = Treatments.objects.get(pk=appointment_slices.treatment.pk).treatment
                    available = 0
                date_timeslices.append({"start": "{} {}".format(date_, slice_data[0]["slice_start"]),
                                        "end": "{} {}".format(date_, slice_data[0]["slice_end"]),
                                        "taken": taken,
                                        "available": available,
                                        "appointment_id": appointment_id,
                                        "first_name": first_name,
                                        "last_name": last_name,
                                        "treatment": treatment})
            date_ += delta
            weekday += 1
            if weekday > 7:
                weekday -= 7
        return Response(date_timeslices)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def make_time_change(self, request):
        # get variables
        date_ = parse_date(getpost(request, 'date'))
        old_start_time = parse_time(getpost(request, 'old_start_time'))
        old_end_time = parse_time(getpost(request, 'old_end_time'))
        new_start_time = parse_time(getpost(request, 'new_start_time'))
        new_end_time = parse_time(getpost(request, 'new_end_time'))

        # get the day of the week (+1 because of the ID's in the table)
        weekday = datetime.strptime("{} {}".format(
            date_, old_start_time), '%Y-%m-%d %H:%M:%S').weekday() + 1
        standart_week = StandardWeek.objects.get(pk=weekday)
        # see if there were changes made previously
        try:
            change = Changes.objects.get(date=date_)
        except:
            # if there were no changes, just make them
            change = Changes.objects.create(
                date=date_, slice_count=standart_week.slice_count)
            slices = TimeSlices.objects.filter(standardweek__pk=weekday)
            for i in slices:
                change.slices.add(i)
        # find the old timeslice which is going to be changed
        try:
            old_slice = TimeSlices.objects.get(slice_start=old_start_time, slice_end=old_end_time,
                                               changes__pk=change.pk)
            print(old_slice)
        except:
            return Response("ERROR: No old slice found!")
        # find or make the new timeslice
        try:
            new_slice = TimeSlices.objects.get(
                slice_start=new_start_time, slice_end=new_end_time)
        except:
            new_slice = TimeSlices.objects.create(
                slice_start=new_start_time, slice_end=new_end_time)
        # apply the changes
        try:
            change.slices.remove(old_slice)
            change.slices.add(new_slice)
        except:
            return Response("ERROR: I don't really know what went wrong... Maybe try again or contact an admin ;-;")
        return Response("SUCCESS")

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def make_day_change(self, request):
        date_ = parse_date(getpost(request, 'date'))
        slice_count = getpost(request, 'slice_count')
        weekday = datetime.strptime("{} 01:00:00".format(date_), '%Y-%m-%d %H:%M:%S').weekday() + 1
        try:
            changes = Changes.objects.get(date=date_)
            changes.slice_count = slice_count
            changes.save()
        except:
            changes = Changes.objects.create(date=date_, slice_count=slice_count)
            slices = TimeSlices.objects.filter(standardweek__pk=weekday)
            for i in slices:
                changes.slices.add(i)
        return Response("Success")

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_appointment_data(self, request):
        appointment_id = request.query_params.get('appointment_id')
        result = []

        appointment = Appointments.objects.get(id=appointment_id)
        time_slice = TimeSlices.objects.get(id=appointment.time_slice_id)
        treatment = Treatments.objects.get(id=appointment.treatment_id)
        credential = Credentials.objects.get(id=appointment.credentials_id)

        result.append({
            'customer': serializers.serialize('json', [credential, ]),
            'appointment': serializers.serialize('json', [appointment, ]),
            'time_slice': serializers.serialize('json', [time_slice, ]),
            'treatment': serializers.serialize('json', [treatment, ]),
        })

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


class AppointmentsView(viewsets.ModelViewSet):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_appointment(self, request):
        return create_appointment(request)

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def delete_vacation(self, request):
        vacation_id = getpost(request, 'id')
        try:
            Vacations.objects.filter(pk=vacation_id).delete()
        except:
            return Response('Fail')
        return Response('Success')


    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_appointments_customer(self, request):
        # get and set variables
        date_ = parse_date(getpost(request, 'beginweek'))
        endweek = parse_date(getpost(request, 'endweek'))
        delta = timedelta(days=1)
        date_timeslices = []
        # get the day of the week
        today_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
        # get today's date
        today_date = parse_date(today_datetime[0])
        # check if the received date is earlier than today
        if date_ <= today_date:
            date_ = today_date + delta
        # get the weekday (monday, tuesday, etc (+1 because of the ID's in the database))
        weekday = datetime.strptime('{} 01:00:00'.format(
            date_), '%Y-%m-%d %H:%M:%S').weekday() + 1
        # loop through all days between the 2 received dates
        while date_ <= endweek:
            # check for a vacation
            try:
                vacations = Vacations.objects.filter(
                    start_date__lte=date_, end_date__gte=date_).values()
                if vacations[0]:
                    pass
            except:
                # get the all the timeslices within the range of the date's
                # check for changes
                try:
                    if_changes = Changes.objects.get(date=date_).slice_count
                    slice_count = int(if_changes)
                    slices = TimeSlices.objects.filter(
                        changes__date=date_).values()
                except:
                    slices = TimeSlices.objects.filter(
                        standardweek__pk=weekday).values()
                    slice_count = StandardWeek.objects.get(
                        pk=weekday).slice_count
                count = 0
                slice_array = []
                # check per slice if there is an appointment connected to it
                for i in slices:
                    appointment_slices = Appointments.objects.filter(
                        time_slice_id=i['id'], date=date_)
                    if appointment_slices:
                        count += 1
                    else:
                        slice_array.append(i['id'])
                # check of there is still space left for a new appointment
                if count < slice_count:
                    # add all results to the final array
                    for i in slice_array:
                        slice_data = TimeSlices.objects.get(pk=i)
                        date_timeslices.append({"start": "{} {}".format(date_, slice_data.slice_start),
                                                "end": "{} {}".format(date_, slice_data.slice_end)})
            date_ += delta
            weekday += 1
        return Response(date_timeslices)
