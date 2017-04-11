# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0016_calltoaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthcareCarrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='HealthcarePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=10000)),
                ('carrier', models.ForeignKey(blank=True, null=True, to='picmodels.HealthcareCarrier')),
            ],
        ),
        migrations.CreateModel(
            name='ProviderLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=10000)),
                ('accepted_plans', models.ManyToManyField(to='picmodels.HealthcarePlan', blank=True)),
            ],
        ),
    ]
