# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0088_defaultenrollmentstepcomplete'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='datetime_received_by_client',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='datetime_received_by_client',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
