# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0010_auto_20151229_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricssubmission',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
