# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0076_auto_20180611_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSequences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Case Management Sequences',
            },
        ),
    ]
