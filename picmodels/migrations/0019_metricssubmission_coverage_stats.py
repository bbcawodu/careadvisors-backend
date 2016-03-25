# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0018_metricssubmission_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricssubmission',
            name='coverage_stats',
            field=models.TextField(default=b''),
        ),
    ]
