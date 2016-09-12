# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0008_auto_20160912_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='picstaff',
            name='region',
            field=models.CharField(max_length=1000, blank=True, null=True, default=''),
        ),
    ]
