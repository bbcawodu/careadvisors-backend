# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0085_stepsforcmsequences_rest_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='date_created',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='date_modified',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='date_created',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='date_modified',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
