# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0020_auto_20170414_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthcareplan',
            name='carrier',
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='carriers',
            field=models.ManyToManyField(to='picmodels.HealthcareCarrier', blank=True),
        ),
    ]
