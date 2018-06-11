# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0075_followupnotices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casemanagementclient',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
