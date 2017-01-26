# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0011_auto_20170125_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumernote',
            name='consumer_backup',
            field=models.ForeignKey(blank=True, null=True, to='picmodels.PICConsumerBackup'),
        ),
    ]
