# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0047_casemanagementstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='casemanagementstatus',
            name='contact_backup',
            field=models.ForeignKey(null=True, to='picmodels.PICConsumerBackup', blank=True),
        ),
    ]
