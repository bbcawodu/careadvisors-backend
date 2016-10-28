# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0016_auto_20161028_0858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picstaff',
            name='base_location',
        ),
        migrations.AddField(
            model_name='picstaff',
            name='base_locations',
            field=models.ManyToManyField(blank=True, to='picmodels.NavMetricsLocation'),
        ),
    ]
