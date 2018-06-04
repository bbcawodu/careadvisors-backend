# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0073_auto_20180525_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactlog',
            name='contact_type',
            field=models.CharField(max_length=1000, blank=True, null=True, default='not available', choices=[('Email', 'Email'), ('Text', 'Text'), ('Phone', 'Phone'), ('In-Person', 'In-Person'), ('not available', 'not available')]),
        ),
        migrations.AlterField(
            model_name='contactlog',
            name='status',
            field=models.CharField(max_length=1000, blank=True, null=True, default='not available', choices=[('Voice Message', 'Voice Message'), ('Completed', 'Completed'), ('not available', 'not available')]),
        ),
    ]
