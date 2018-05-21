# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0069_auto_20180514_1939'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='casemanagementclient',
            unique_together=set([]),
        ),
    ]
