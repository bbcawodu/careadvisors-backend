# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0017_auto_20160114_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricssubmission',
            name='zipcode',
            field=models.CharField(default=b'', max_length=1000),
        ),
    ]
