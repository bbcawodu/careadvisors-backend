# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0067_auto_20180430_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='cm_client_for_routing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='picmodels.CaseManagementClient'),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='cm_client_for_routing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='picmodels.CaseManagementClient'),
        ),
    ]
