# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0008_picconsumerbackup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumercpsinfoentry',
            name='consumer',
        ),
    ]
