# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0026_auto_20161122_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentialsmodel',
            name='id',
            field=models.ForeignKey(to='picmodels.PICStaff', primary_key=True, serialize=False),
        ),
    ]
