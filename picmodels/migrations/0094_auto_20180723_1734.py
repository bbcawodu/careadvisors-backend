# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0093_auto_20180723_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picconsumer',
            name='consumer_hospital_data',
        ),
        migrations.RemoveField(
            model_name='picconsumerbackup',
            name='consumer_hospital_data',
        ),
        migrations.AddField(
            model_name='consumerhospitaldata',
            name='consumer',
            field=models.ForeignKey(blank=True, null=True, to='picmodels.PICConsumer'),
        ),
        migrations.AddField(
            model_name='consumerhospitaldata',
            name='consumer_backup',
            field=models.ForeignKey(blank=True, null=True, to='picmodels.PICConsumerBackup'),
        ),
    ]
