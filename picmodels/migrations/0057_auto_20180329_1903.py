# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0056_auto_20180329_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='major',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='education',
            name='school',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=2000),
        ),
    ]
