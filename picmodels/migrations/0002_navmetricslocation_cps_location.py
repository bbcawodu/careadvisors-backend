# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-16 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='navmetricslocation',
            name='cps_location',
            field=models.BooleanField(default=False),
        ),
    ]
