# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0007_auto_20170124_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='PICConsumerBackup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=1000)),
                ('middle_name', models.CharField(null=True, max_length=1000, blank=True)),
                ('last_name', models.CharField(max_length=1000, default='')),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('phone', models.CharField(null=True, max_length=1000, blank=True)),
                ('preferred_language', models.CharField(null=True, max_length=1000, blank=True)),
                ('best_contact_time', models.CharField(null=True, max_length=1000, blank=True)),
                ('household_size', models.IntegerField()),
                ('plan', models.CharField(null=True, max_length=1000, blank=True)),
                ('met_nav_at', models.CharField(max_length=1000)),
                ('date_met_nav', models.DateField(null=True, blank=True)),
                ('cps_consumer', models.BooleanField(default=False)),
                ('address', models.ForeignKey(null=True, blank=True, to='picmodels.Address')),
                ('navigator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='picmodels.PICStaff')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
