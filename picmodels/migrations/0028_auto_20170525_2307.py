# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0027_auto_20170525_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthcareservicecostentry',
            name='coinsurance',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(100)], null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='healthcareservicecostentry',
            name='copay',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
