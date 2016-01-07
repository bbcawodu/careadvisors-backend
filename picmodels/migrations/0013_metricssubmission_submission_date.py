# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0012_auto_20160104_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricssubmission',
            name='submission_date',
            field=models.DateField(null=True),
        ),
    ]
