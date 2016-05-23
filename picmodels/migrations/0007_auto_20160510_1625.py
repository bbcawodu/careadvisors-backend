# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0006_auto_20160428_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='address',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='household_size',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='met_nav_at',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='middle_name',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='plan',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='zipcode',
            field=models.CharField(default=b'', max_length=1000),
        ),
    ]
