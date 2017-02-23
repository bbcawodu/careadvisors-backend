# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0010_auto_20170125_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumercpsinfoentry',
            name='primary_dependent',
            field=models.ForeignKey(null=True, to='picmodels.PICConsumer', on_delete=django.db.models.deletion.SET_NULL, related_name='primary_guardian', blank=True),
        ),
        migrations.AlterField(
            model_name='picconsumer',
            name='cps_info',
            field=models.ForeignKey(null=True, to='picmodels.ConsumerCPSInfoEntry', on_delete=django.db.models.deletion.SET_NULL, blank=True),
        ),
        migrations.AlterField(
            model_name='picconsumerbackup',
            name='cps_info',
            field=models.ForeignKey(null=True, to='picmodels.ConsumerCPSInfoEntry', on_delete=django.db.models.deletion.SET_NULL, blank=True),
        ),
    ]
