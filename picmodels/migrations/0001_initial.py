# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consumer_name', models.CharField(max_length=1000)),
                ('consumer_email', models.EmailField(max_length=254)),
                ('consumer_phone', models.CharField(max_length=1000)),
                ('consumer_preferred_language', models.CharField(max_length=1000)),
                ('consumer_best_contact_time', models.CharField(max_length=1000)),
                ('appointment_location_name', models.CharField(max_length=1000)),
                ('appointment_address', models.CharField(max_length=2000)),
                ('appointment_date', models.CharField(max_length=1000)),
                ('appointment_start_time', models.CharField(max_length=1000)),
                ('appointment_end_time', models.CharField(max_length=1000)),
                ('appointment_location_phone', models.CharField(max_length=1000)),
                ('appointment_poc_name', models.CharField(max_length=1000)),
                ('appointment_poc_email', models.CharField(max_length=1000)),
                ('appointment_poc_type', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PICUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=1000)),
                ('phone_number', models.CharField(max_length=1000)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set([('consumer_name', 'consumer_email', 'consumer_phone', 'consumer_preferred_language', 'consumer_best_contact_time', 'appointment_location_name', 'appointment_address', 'appointment_date', 'appointment_start_time', 'appointment_end_time', 'appointment_location_phone', 'appointment_poc_name', 'appointment_poc_email', 'appointment_poc_type')]),
        ),
    ]
