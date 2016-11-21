# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0021_auto_20161121_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picconsumer',
            name='zipcode',
            field=models.CharField(default='', max_length=1000, blank=True),
        ),
    ]
