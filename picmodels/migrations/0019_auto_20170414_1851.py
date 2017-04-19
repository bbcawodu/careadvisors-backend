# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0018_auto_20170410_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcareplan',
            name='metal_level',
            field=models.CharField(null=True, blank=True, max_length=1000, default='Not Available', choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold'), ('Platinum', 'Platinum'), ('Catastrophic', 'Catastrophic'), ('Not Available', 'Not Available')]),
        ),
        migrations.AddField(
            model_name='healthcareplan',
            name='premium_type',
            field=models.CharField(null=True, blank=True, max_length=1000, default='Not Available', choices=[('HMO', 'HMO'), ('PPO', 'PPO'), ('POS', 'POS'), ('EPO', 'EPO'), ('Not Available', 'Not Available')]),
        ),
    ]
