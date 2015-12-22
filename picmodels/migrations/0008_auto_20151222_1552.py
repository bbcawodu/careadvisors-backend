# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0007_auto_20151221_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picappointment',
            name='consumer_best_contact_time',
            field=models.CharField(max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='picappointment',
            name='consumer_preferred_language',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
