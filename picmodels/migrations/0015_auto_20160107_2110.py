# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0014_auto_20160107_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricssubmission',
            name='appointments_cmplx_market',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='appointments_cmplx_medicaid',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='appointments_held',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='appointments_over_hour',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='appointments_over_three_hours',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='appointments_postenroll_assistance',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='appointments_scheduled',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='comments',
            field=models.CharField(default=b'', max_length=5000, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='confirmation_calls',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='county',
            field=models.CharField(default=b'', max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='outreach_stakeholder_activity',
            field=models.CharField(default=b'', max_length=5000, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='submission_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='trends',
            field=models.CharField(default=b'', max_length=5000, blank=True),
        ),
        migrations.AlterField(
            model_name='picstaff',
            name='county',
            field=models.CharField(default=b'', max_length=1000, blank=True),
        ),
    ]
