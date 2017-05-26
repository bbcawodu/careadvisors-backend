# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0029_healthcareplan_county'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_primary_care_physician_family_standard_cost',
        ),
        migrations.RemoveField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_primary_care_physician_individual_standard_cost',
        ),
        migrations.AddField(
            model_name='healthcareservicecostentry',
            name='plan_obj_for_primary_care_physician_standard_cost',
            field=models.ForeignKey(to='picmodels.HealthcarePlan', related_name='primary_care_physician_standard_cost', blank=True, null=True),
        ),
    ]
