# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0019_auto_20170414_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthcareplan',
            name='metal_level',
            field=models.CharField(null=True, choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold'), ('Platinum', 'Platinum'), ('Catastrophic', 'Catastrophic'), ('Not Available', 'Not Available')], blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='healthcareplan',
            name='premium_type',
            field=models.CharField(null=True, choices=[('HMO', 'HMO'), ('PPO', 'PPO'), ('POS', 'POS'), ('EPO', 'EPO'), ('Not Available', 'Not Available')], blank=True, max_length=1000),
        ),
    ]
