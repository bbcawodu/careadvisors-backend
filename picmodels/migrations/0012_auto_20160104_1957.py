# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0011_metricssubmission_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricssubmission',
            name='trends',
            field=models.CharField(max_length=5000, null=True, blank=True),
        ),
    ]
