# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0020_auto_20161121_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picconsumer',
            name='address',
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='address_line_1',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
