# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0009_metricssubmission'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='picappointment',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='picappointment',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='picappointment',
            name='location',
        ),
        migrations.RemoveField(
            model_name='picappointment',
            name='poc',
        ),
        migrations.DeleteModel(
            name='PICAppointment',
        ),
    ]
