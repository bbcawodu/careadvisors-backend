# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0017_auto_20161028_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerNote',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('navigator_notes', models.TextField(default='', blank=True)),
                ('consumer', models.ForeignKey(to='picmodels.PICConsumer')),
            ],
        ),
    ]
