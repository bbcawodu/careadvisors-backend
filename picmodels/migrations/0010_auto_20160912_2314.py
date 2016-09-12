# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0009_picstaff_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metricssubmission',
            name='plan_stats',
        ),
        migrations.AddField(
            model_name='planstat',
            name='metrics_submission',
            field=models.ForeignKey(to='picmodels.MetricsSubmission', null=True, blank=True),
        ),
    ]
