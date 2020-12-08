# Generated by Django 3.1.3 on 2020-12-08 09:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber', '0007_auto_20201207_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='duration',
            field=models.TimeField(default=datetime.time(10, 2, 56, 671085)),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date_booked_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 8, 10, 2, 56, 667087)),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date_booked_start',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 8, 10, 2, 56, 667087)),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='time_close',
            field=models.TimeField(default=datetime.time(10, 2, 56, 669086)),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='time_open',
            field=models.TimeField(default=datetime.time(10, 2, 56, 669086)),
        ),
        migrations.AlterField(
            model_name='worktimes',
            name='time_close',
            field=models.TimeField(default=datetime.time(10, 2, 56, 673084)),
        ),
        migrations.AlterField(
            model_name='worktimes',
            name='time_open',
            field=models.TimeField(default=datetime.time(10, 2, 56, 673084)),
        ),
    ]
