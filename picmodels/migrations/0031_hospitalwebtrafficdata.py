# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0030_auto_20170526_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalWebTrafficData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('hospital_name', models.CharField(max_length=10000)),
                ('monthly_visits', models.IntegerField(null=True, blank=True)),
            ],
        ),
    ]
