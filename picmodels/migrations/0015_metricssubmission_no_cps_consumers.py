# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0014_auto_20170128_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricssubmission',
            name='no_cps_consumers',
            field=models.IntegerField(default=0),
        ),
    ]
