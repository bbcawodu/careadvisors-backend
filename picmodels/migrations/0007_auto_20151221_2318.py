# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0006_auto_20151218_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='consumer',
            field=models.ForeignKey(blank=True, to='picmodels.PICConsumer', null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(blank=True, to='picmodels.Location', null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='poc',
            field=models.ForeignKey(blank=True, to='picmodels.PICStaff', null=True),
        ),
    ]
