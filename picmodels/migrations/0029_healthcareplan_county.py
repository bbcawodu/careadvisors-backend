# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0028_auto_20170525_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcareplan',
            name='county',
            field=models.CharField(max_length=1000, blank=True, null=True),
        ),
    ]
