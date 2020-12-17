# Generated by Django 3.1.3 on 2020-12-16 23:21

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('barber', '0003_auto_20201209_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('is_open', models.BooleanField(default=False)),
                ('slice_count', models.IntegerField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Timeslices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slice_start', models.TimeField()),
                ('slice_end', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='employees',
            name='barber',
        ),
        migrations.RemoveField(
            model_name='employees',
            name='user',
        ),
        migrations.RemoveField(
            model_name='employees',
            name='work_time',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='barber',
        ),
        migrations.RemoveField(
            model_name='worktimes',
            name='timeSlice',
        ),
        migrations.RemoveField(
            model_name='appointments',
            name='employee_id',
        ),
        migrations.RemoveField(
            model_name='credentials',
            name='appointment',
        ),
        migrations.RemoveField(
            model_name='openinghours',
            name='barber',
        ),
        migrations.RemoveField(
            model_name='openinghours',
            name='is_open',
        ),
        migrations.RemoveField(
            model_name='openinghours',
            name='last_edit',
        ),
        migrations.RemoveField(
            model_name='openinghours',
            name='time_close',
        ),
        migrations.RemoveField(
            model_name='openinghours',
            name='time_open',
        ),
        migrations.AddField(
            model_name='appointments',
            name='credentials',
            field=models.ManyToManyField(to='barber.Credentials'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='reason',
            field=models.TextField(default=django.utils.timezone.now, max_length=3000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date_booked_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 0, 21, 27, 362324)),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date_booked_start',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 0, 21, 27, 362324)),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='treatment',
            field=models.TextField(max_length=1500),
        ),
        migrations.DeleteModel(
            name='Answers',
        ),
        migrations.DeleteModel(
            name='Barbers',
        ),
        migrations.DeleteModel(
            name='Employees',
        ),
        migrations.DeleteModel(
            name='Questions',
        ),
        migrations.DeleteModel(
            name='Worktimes',
        ),
        migrations.DeleteModel(
            name='WorktimeSlices',
        ),
        migrations.AddField(
            model_name='daily',
            name='slices',
            field=models.ManyToManyField(to='barber.Timeslices'),
        ),
        migrations.AddField(
            model_name='openinghours',
            name='slices',
            field=models.ManyToManyField(to='barber.Timeslices'),
        ),
    ]
