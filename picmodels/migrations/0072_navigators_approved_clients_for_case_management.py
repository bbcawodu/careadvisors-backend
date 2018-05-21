# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0071_auto_20180515_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigators',
            name='approved_clients_for_case_management',
            field=models.ManyToManyField(blank=True, related_name='approved_navigators_for_case_management', to='picmodels.CaseManagementClient'),
        ),
    ]
