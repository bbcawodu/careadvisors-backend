# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0084_testenrollmentstep1'),
    ]

    operations = [
        migrations.AddField(
            model_name='stepsforcmsequences',
            name='rest_url',
            field=models.CharField(max_length=500, unique=True, blank=True, null=True),
        ),
    ]
