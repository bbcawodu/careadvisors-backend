# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0043_consumerhospitalinfo_case_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navmetricslocation',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='picmodels.Address'),
        ),
    ]
