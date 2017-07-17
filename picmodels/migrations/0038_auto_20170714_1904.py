# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0037_auto_20170629_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumercpsinfoentry',
            name='point_of_origin',
            field=models.CharField(null=True, max_length=1000, choices=[('Walk-in', 'Walk-in'), ('Appointment', 'Appointment'), ('Referral from call', 'Referral from call'), ('Referral from school letter', 'Referral from school letter'), ('Enrollment event', 'Enrollment event'), ('Not Available', 'Not Available')], default='Not Available', blank=True),
        ),
        migrations.AlterField(
            model_name='consumercpsinfoentry',
            name='app_type',
            field=models.CharField(null=True, max_length=1000, choices=[('Medicaid', 'Medicaid'), ('SNAP', 'SNAP'), ('Medicaid/SNAP', 'Medicaid/SNAP'), ('Redetermination', 'Redetermination'), ('Plan Selection', 'Plan Selection'), ('Fax FCRC', 'Fax FCRC'), ('Education', 'Education'), ('MMCO', 'MMCO'), ('Not Available', 'Not Available')], default='Not Available', blank=True),
        ),
    ]
