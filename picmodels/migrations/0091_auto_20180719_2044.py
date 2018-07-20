# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0090_auto_20180718_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='referral_type',
            field=models.ForeignKey(blank=True, null=True, related_name='consumers_referred_by_this_type', on_delete=django.db.models.deletion.SET_NULL, to='picmodels.HealthcareServiceExpertise'),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='referral_type',
            field=models.ForeignKey(blank=True, null=True, related_name='backup_consumers_referred_by_this_type', on_delete=django.db.models.deletion.SET_NULL, to='picmodels.HealthcareServiceExpertise'),
        ),
    ]
