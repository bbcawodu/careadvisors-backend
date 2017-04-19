# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0021_auto_20170417_2353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthcareplan',
            name='carriers',
        ),
        migrations.AddField(
            model_name='healthcarecarrier',
            name='state_province',
            field=models.CharField(null=True, verbose_name='State/Province', max_length=40, blank=True),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='carrier',
            field=models.ForeignKey(null=True, blank=True, to='picmodels.HealthcareCarrier'),
        ),
    ]
