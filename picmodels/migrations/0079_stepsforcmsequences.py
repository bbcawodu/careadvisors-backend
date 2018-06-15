# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0078_casemanagementclient_cm_sequences'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepsForCMSequences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('step_name', models.CharField(max_length=500, unique=True)),
                ('step_table_name', models.CharField(max_length=500, unique=True)),
                ('step_class_name', models.CharField(max_length=500, unique=True)),
                ('step_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name_plural': 'Steps for Case Management Sequences',
            },
        ),
    ]
