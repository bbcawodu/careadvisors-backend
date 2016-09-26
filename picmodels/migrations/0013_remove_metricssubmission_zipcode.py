# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0012_auto_20160920_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metricssubmission',
            name='zipcode',
        ),
    ]
