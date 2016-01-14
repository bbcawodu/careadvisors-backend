# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0016_auto_20160107_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picstaff',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
    ]
