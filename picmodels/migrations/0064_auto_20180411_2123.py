# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0063_auto_20180410_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='degree_type',
            field=models.CharField(max_length=100, blank=True, null=True, default='Not Available', choices=[('undergraduate', 'undergraduate'), ('graduate', 'graduate'), ('bachelors', 'bachelors'), ('masters', 'masters'), ('high school', 'high school'), ('associate', 'associate'), ('Not Available', 'Not Available')]),
        ),
    ]
