# Generated by Django 3.1.3 on 2020-12-09 22:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorktimeSlices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_from', models.DateTimeField()),
                ('time_to', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='answers',
            name='duration',
            field=models.TimeField(default=datetime.time(23, 27, 26, 841974)),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date_booked_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 9, 23, 27, 26, 841974)),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date_booked_start',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 9, 23, 27, 26, 841974)),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='time_close',
            field=models.TimeField(default=datetime.time(23, 27, 26, 841974)),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='time_open',
            field=models.TimeField(default=datetime.time(23, 27, 26, 841974)),
        ),
        migrations.AlterField(
            model_name='worktimes',
            name='end',
            field=models.TimeField(default=datetime.time(23, 27, 26, 841974)),
        ),
        migrations.AlterField(
            model_name='worktimes',
            name='start',
            field=models.TimeField(default=datetime.time(23, 27, 26, 841974)),
        ),
        migrations.AddField(
            model_name='worktimes',
            name='timeSlice',
            field=models.ManyToManyField(to='barber.WorktimeSlices'),
        ),
    ]
