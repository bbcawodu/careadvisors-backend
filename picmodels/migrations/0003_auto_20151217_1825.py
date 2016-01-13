# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0002_auto_20151217_1802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='consumer_name',
            new_name='consumer_first_name',
        ),
        migrations.AddField(
            model_name='appointment',
            name='consumer_last_name',
            field=models.CharField(default=b'', max_length=1000),
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set([('consumer_first_name', 'consumer_last_name', 'consumer_email', 'consumer_phone', 'consumer_preferred_language', 'consumer_best_contact_time', 'appointment_location_name', 'appointment_address', 'appointment_date', 'appointment_start_time', 'appointment_end_time', 'appointment_location_phone', 'appointment_poc_name', 'appointment_poc_email', 'appointment_poc_type')]),
        ),
    ]
