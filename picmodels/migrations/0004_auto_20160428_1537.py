# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0003_picstaff_consumers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricssubmission',
            name='outreach_activity',
            field=models.CharField(default=b'', max_length=5000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='metricssubmission',
            name='trends',
            field=models.CharField(default=b'', max_length=5000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='picconsumer',
            name='best_contact_time',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='picconsumer',
            name='phone',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='picconsumer',
            name='preferred_language',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='picstaff',
            name='county',
            field=models.CharField(default=b'', max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planstat',
            name='metal_level',
            field=models.CharField(default=b'Not Available', max_length=1000, null=True, blank=True, choices=[(b'Bronze', b'Bronze'), (b'Silver', b'Silver'), (b'Gold', b'Gold'), (b'Catastrophic', b'Catastrophic'), (b'Not Available', b'Not Available')]),
        ),
        migrations.AlterField(
            model_name='planstat',
            name='premium_type',
            field=models.CharField(default=b'Not Available', max_length=1000, null=True, blank=True, choices=[(b'HMO', b'HMO'), (b'PPO', b'PPO'), (b'Not Available', b'Not Available')]),
        ),
    ]
