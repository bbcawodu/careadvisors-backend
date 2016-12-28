# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0032_auto_20161222_2106'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='picconsumer',
            unique_together=set([('first_name', 'last_name', 'met_nav_at', 'household_size')]),
        ),
    ]
