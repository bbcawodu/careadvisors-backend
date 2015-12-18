# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0003_auto_20151217_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='PICAppointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consumer_f_name', models.CharField(max_length=1000)),
                ('consumer_l_name', models.CharField(default=b'', max_length=1000)),
                ('consumer_email', models.EmailField(max_length=254)),
                ('consumer_phone', models.CharField(max_length=1000)),
                ('consumer_preferred_language', models.CharField(max_length=1000)),
                ('consumer_best_contact_time', models.CharField(max_length=1000)),
                ('location_name', models.CharField(max_length=1000)),
                ('address', models.CharField(max_length=2000)),
                ('date', models.CharField(max_length=2000)),
                ('start_time', models.CharField(max_length=1000)),
                ('end_time', models.CharField(max_length=1000)),
                ('location_phone', models.CharField(max_length=1000)),
                ('poc_f_name', models.CharField(max_length=1000)),
                ('poc_l_name', models.CharField(max_length=1000)),
                ('poc_email', models.CharField(max_length=1000)),
                ('poc_type', models.CharField(max_length=1000)),
            ],
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.AlterUniqueTogether(
            name='picappointment',
            unique_together=set([('consumer_f_name', 'consumer_l_name', 'consumer_email', 'consumer_phone', 'consumer_preferred_language', 'consumer_best_contact_time', 'location_name', 'address', 'date', 'start_time', 'end_time', 'location_phone', 'poc_f_name', 'poc_l_name', 'poc_email', 'poc_type')]),
        ),
    ]
