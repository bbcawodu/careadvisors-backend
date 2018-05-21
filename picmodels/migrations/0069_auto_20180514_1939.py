# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0068_auto_20180501_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casemanagementclient',
            options={'verbose_name_plural': 'Case Management Clients'},
        ),
    ]
