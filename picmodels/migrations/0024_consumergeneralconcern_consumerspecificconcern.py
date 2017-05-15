# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0023_auto_20170424_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerGeneralConcern',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=1000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumerSpecificConcern',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('question', models.CharField(max_length=10000, unique=True)),
                ('research_weight', models.IntegerField(default=50, validators=[django.core.validators.MaxValueValidator(100)])),
                ('related_general_concerns', models.ManyToManyField(blank=True, related_name='related_specific_concerns', to='picmodels.ConsumerGeneralConcern')),
            ],
        ),
    ]
