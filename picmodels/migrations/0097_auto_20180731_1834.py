# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0096_auto_20180725_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picconsumer',
            name='gender',
            field=models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Traansgender'), ('Not Available', 'Not Available')]),
        ),
        migrations.AlterField(
            model_name='picconsumerbackup',
            name='gender',
            field=models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Traansgender'), ('Not Available', 'Not Available')]),
        ),
    ]
