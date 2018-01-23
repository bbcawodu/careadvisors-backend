# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0048_casemanagementstatus_contact_backup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picconsumer',
            name='cps_consumer',
        ),
        migrations.RemoveField(
            model_name='picconsumerbackup',
            name='cps_consumer',
        ),
    ]
