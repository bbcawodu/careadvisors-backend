# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0058_auto_20180329_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='major',
            field=models.CharField(blank=True, null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='education',
            name='school',
            field=models.CharField(blank=True, null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.CharField(blank=True, null=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(blank=True, null=True, max_length=2000),
        ),
    ]
