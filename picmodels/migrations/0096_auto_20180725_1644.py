# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0095_auto_20180724_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultenrollmentstep1',
            name='appointment_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defaultenrollmentstep1',
            name='case_status',
            field=models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Active', 'Active'), ('In progress with benefits org', 'In progress with benefits org'), ('On hold', 'On hold'), ('Closed', 'Closed'), ('Not Available', 'Not Available')]),
        ),
        migrations.AddField(
            model_name='defaultenrollmentstep1',
            name='customer_service_success',
            field=models.CharField(max_length=500, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defaultenrollmentstep1',
            name='expedite_benefits_organization_contact_name',
            field=models.CharField(max_length=500, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defaultenrollmentstep1',
            name='expedite_benefits_organization_contact_phone',
            field=models.CharField(max_length=500, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defaultenrollmentstep1',
            name='policy_number',
            field=models.CharField(max_length=500, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defaultenrollmentstep1',
            name='primary_care_physician',
            field=models.CharField(max_length=500, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='defaultenrollmentstep1',
            name='resource_case_number',
            field=models.CharField(max_length=500, blank=True, null=True),
        ),
    ]
