# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0002_auto_20160419_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='picstaff',
            name='consumers',
            field=models.ManyToManyField(to='picmodels.PICConsumer'),
        ),
    ]
