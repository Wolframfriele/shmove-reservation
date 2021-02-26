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
        # current_time = parse_time(today_datetime[1])
        while date_ <= end_date:
            count = 0
            # check for changes
            try:
                # if_changes = Changes.objects.get(date=date_).slice_count
                slice_count = iStandardWeek.objects.get(pk=weekday).slice_count
                slices = TimeSlices.objects.filter(
                    standardweek__pk=weekday).values()
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