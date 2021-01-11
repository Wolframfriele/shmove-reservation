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
from barber.serializers import TestSerializer, AppointmentSerializer

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
        dbs_string = getpost(request, 'date_booked_start')
        dbs_strings = dbs_string.split()
        date_ = dbs_strings[0]
        dbe_string = getpost(request, 'date_booked_end')
        dbe_strings = dbe_string.split()
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
                get_slice = TimeSlices.objects.get(slice_start=time_start, slice_end=time_end).pk
                find_appointment = Appointments.objects.filter(date=date_, time_slice_id=get_slice).values()
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

                    treatment_ = Treatments.objects.get(pk=treatment)
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
                            real_date = datetime.strptime(dbs_string, '%Y-%m-%d %H:%M:%S').strftime("%d %b, %Y")
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
                                server.sendmail(sender_email, receiver_email, message.as_string())

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

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_free_places(self, request):
        # get variables
        date_ = parse_date(getpost(request, 'beginweek'))
        endweek = parse_date(getpost(request, 'endweek'))
        delta = timedelta(days=1)

        date_timeslices = []
        # get the day of the week
        weekday = datetime.now().weekday() + 1
        today_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()
        # get today's date
        today_date = parse_date(today_datetime[0])
        current_time = parse_time(today_datetime[1])
        # check if the received date is earlier than today
        if date_ < today_date:
            date_ = today_date
        # loop through all days between the 2 received dates
        while date_ <= endweek:
            slice_array = []
            count = 0
            # test if there is a entry in the model "Changes"
            try:
                if_changes = Changes.objects.get(date=date_).slice_count
                slice_count = int(if_changes)
                slices = TimeSlices.objects.filter(changes__date=date_).values()
            except:
                # get the timeslices from the standardweek using the day value
                slices = TimeSlices.objects.filter(standardweek__pk=weekday).values()
                slice_count = StandardWeek.objects.get(pk=weekday).slice_count

            # for every timeslice connected to this date, check if there is an appointment affiliated
            for f in slices:
                appointment_slices = Appointments.objects.filter(time_slice_id=f['id'], date=date_)
                if appointment_slices:
                    # if an appointment is affiliated
                    count += 1
                else:
                    # if no appointment is affiliated
                    slice_array.append(f['id'])

            # only send back the timeslices when there are less slices on this day than set as "slice_count"
            if count < slice_count:
                for i in slice_array:
                    slice_data = TimeSlices.objects.filter(pk=i).values()
                    # make sure no past time_slices get sent
                    if slice_data[0]["slice_start"] > current_time:
                        date_timeslices.append({"start": "{} {}".format(date_, slice_data[0]["slice_start"]),
                                                "end": "{} {}".format(date_, slice_data[0]["slice_end"]),
                                                "taked": "{} {}".format(date_, slice_data[0]["slice_end"])
                                                })
            date_ += delta
            weekday += 1
        return Response(date_timeslices)

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
        print(date_)
        print(today_date)
        current_time = parse_time(today_datetime[1])
        while date_ <= endweek:
            count = 0
            try:
                if_changes = Changes.objects.get(date=date_).slice_count
                slice_count = int(if_changes)
                slices = TimeSlices.objects.filter(changes__date=date_).values()
            except:
                # get the timeslices from the standardweek using the day value
                slice_count = StandardWeek.objects.get(pk=weekday).slice_count
                slices = TimeSlices.objects.filter(standardweek__pk=weekday).values()
            # test if there is still enough room for more appointments
            for i in slices:
                appointment_slices = Appointments.objects.filter(time_slice_id=i['id'], date=date_)
                if appointment_slices:
                    count += 1
            county_boi = 0
            for i in slices:
                county_boi += 1
                slice_data = TimeSlices.objects.filter(pk=county_boi).values()
                if count < slice_count and date_ >= today_date:
                    available = 1
                    if date_ == today_date and current_time > slice_data[0]['slice_start']:
                        available = 0
                else:
                    available = 0
                try:
                    appointment_slices = Appointments.objects.get(time_slice_id=i['id'], date=date_).pk
                except:
                    appointment_slices = 0
                taken = appointment_id = 0
                if appointment_slices > 0:
                    taken = 1
                    appointment_id = appointment_slices
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


    # @csrf_exempt
    # @action(methods=['get'], detail=False)
    # def get_appointments_customer(self, request):
    #     dates = []
    #     start_day = datetime.strptime(getpost(request, 'start_day'), '%d/%m/%Y, %H:%M:%S')
    #     end_day = datetime.strptime(getpost(request, 'end_day'), '%d/%m/%Y, %H:%M:%S')
    #     employee_id = getpost(request, 'employee_id')
    #     appointments = Appointments.objects.filter(employee_id=employee_id, date_booked_start__gte=start_day,
    #                                                date_booked_start__lte=end_day).values()
    #     for appointment in appointments:
    #         dates.append({'date_end': appointment['date_booked_end'], 'date_start': appointment['date_booked_start']})
    #     return Response(dates)
    #
    # @csrf_exempt
    # @action(methods=['get'], detail=False)
    # def get_appointments_barber(self, request):
    #
    #     start_day = datetime.strptime(getpost(request, 'start_day'), '%Y-%m-%d')
    #     end_day = datetime.strptime(getpost(request, 'end_day'), '%Y-%m-%d')
    #     barber_id = getpost(request, 'barber_id')
    #
    #     the_info = []
    #     employee_ids = []
    #     get_ids = Employees.objects.filter(barber_id=barber_id).values()
    #     for mini_id in get_ids:
    #         employee_ids.append(mini_id['id'])
    #     appointments = Appointments.objects.filter(date_booked_start__gte=start_day, date_booked_start__lte=end_day,
    #                                                employee_id__in=employee_ids).values()
    #     for appointment in appointments:
    #         if appointment['customer_id'] == 0:
    #             cust_data = Credentials.objects.get(pk=appointment['id'])
    #         else:
    #             cust_data = User.objects.get(pk=appointment['customer_id'])
    #
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
    #
    # @csrf_exempt
    # @action(methods=['get'], detail=False)
    # def get_appointments_barber(self, request):
    #
    #     return request("Grave Pain")

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
