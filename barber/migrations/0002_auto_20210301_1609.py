# Generated by Django 3.1.3 on 2021-03-01 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barber', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='credentials',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='barber.credentials'),
        ),
        migrations.AlterField(
            model_name='credentials',
            name='last_name',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]
