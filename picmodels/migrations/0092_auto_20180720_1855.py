# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0091_auto_20180719_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactlog',
            name='status',
            field=models.CharField(max_length=1000, blank=True, null=True, default='not available', choices=[('Open', 'Open'), ('Voice Message', 'Voice Message'), ('Completed', 'Completed'), ('not available', 'not available')]),
        ),
    ]
