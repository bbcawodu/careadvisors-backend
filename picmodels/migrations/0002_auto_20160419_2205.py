# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metricssubmission',
            old_name='outreach_stakeholder_activity',
            new_name='outreach_activity',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='appointments_cmplx_market',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='appointments_cmplx_medicaid',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='appointments_held',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='appointments_over_hour',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='appointments_over_three_hours',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='appointments_postenroll_assistance',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='appointments_scheduled',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='confirmation_calls',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='enrolled_shop',
        ),
        migrations.RemoveField(
            model_name='metricssubmission',
            name='ref_shop',
        ),
        migrations.AlterField(
            model_name='planstat',
            name='premium_type',
            field=models.CharField(default=b'Not Available', max_length=1000, blank=True, choices=[(b'HMO', b'HMO'), (b'PPO', b'PPO'), (b'Not Available', b'Not Available')]),
        ),
    ]
