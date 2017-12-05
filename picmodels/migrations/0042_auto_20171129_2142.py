# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0041_auto_20171129_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picconsumer',
            name='address',
            field=models.ForeignKey(to='picmodels.Address', on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='picconsumerbackup',
            name='address',
            field=models.ForeignKey(to='picmodels.Address', on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True),
        ),
    ]
