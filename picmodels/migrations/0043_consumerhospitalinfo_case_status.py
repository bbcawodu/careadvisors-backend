# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0042_auto_20171129_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerhospitalinfo',
            name='case_status',
            field=models.CharField(default='Not Available', max_length=1000, choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Not Available', 'Not Available')], blank=True, null=True),
        ),
    ]
