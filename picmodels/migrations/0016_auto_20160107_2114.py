# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0015_auto_20160107_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricssubmission',
            name='county',
            field=models.CharField(default=b'', max_length=1000),
        ),
    ]
