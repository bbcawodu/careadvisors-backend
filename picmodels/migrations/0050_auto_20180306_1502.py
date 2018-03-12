# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0049_auto_20180117_1949'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PICStaff',
            new_name='Navigators',
        ),
    ]
