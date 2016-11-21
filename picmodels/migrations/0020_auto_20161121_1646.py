# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0019_credentialsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picconsumer',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
