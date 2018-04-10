# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0062_navigators_resume_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='navorgsfromonlineform',
            name='appointment_datetime_2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='navorgsfromonlineform',
            name='appointment_datetime_3',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
