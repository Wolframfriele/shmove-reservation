# Generated by Django 3.1.3 on 2020-12-18 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber', '0003_auto_20201217_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('day', models.CharField(max_length=10)),
                ('slice_count', models.IntegerField(default=3)),
            ],
        ),
        migrations.RemoveField(
            model_name='openinghours',
            name='slices',
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date_booked_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 18, 10, 14, 56, 699081)),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='date_booked_start',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 18, 10, 14, 56, 699081)),
        ),
        migrations.DeleteModel(
            name='Daily',
        ),
        migrations.DeleteModel(
            name='Openinghours',
        ),
    ]
