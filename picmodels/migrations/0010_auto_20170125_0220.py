# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0009_remove_consumercpsinfoentry_consumer'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='cps_info',
            field=models.ForeignKey(to='picmodels.ConsumerCPSInfoEntry', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='cps_info',
            field=models.ForeignKey(to='picmodels.ConsumerCPSInfoEntry', null=True, blank=True),
        ),
    ]
