# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0013_metricssubmission_submission_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricssubmission',
            name='county',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='picstaff',
            name='county',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
