# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0060_navorgsfromonlineform'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigators',
            name='navigator_organization',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
