# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0089_auto_20180718_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='referral_channel',
            field=models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Phone', 'Phone'), ('Email', 'Email'), ('Data', 'Data'), ('Not Available', 'Not Available')]),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='referral_channel',
            field=models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Phone', 'Phone'), ('Email', 'Email'), ('Data', 'Data'), ('Not Available', 'Not Available')]),
        ),
    ]
