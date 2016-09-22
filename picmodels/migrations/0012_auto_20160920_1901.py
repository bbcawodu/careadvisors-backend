# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0011_auto_20160915_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricssubmission',
            name='location',
            field=models.ForeignKey(blank=True, to='picmodels.NavMetricsLocation', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='navmetricslocation',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
