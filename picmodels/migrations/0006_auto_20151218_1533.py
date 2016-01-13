# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0005_auto_20151217_2156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='location_phone',
            new_name='phone',
        ),
    ]
