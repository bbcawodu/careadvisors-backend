# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0070_auto_20180515_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='referring_cm_clients',
            field=models.ManyToManyField(blank=True, related_name='referred_consumers_for_cm', to='picmodels.CaseManagementClient'),
        ),
        migrations.AddField(
            model_name='picconsumerbackup',
            name='referring_cm_clients',
            field=models.ManyToManyField(blank=True, related_name='referred_consumer_backups_for_cm', to='picmodels.CaseManagementClient'),
        ),
        migrations.AlterField(
            model_name='picconsumer',
            name='cm_client_for_routing',
            field=models.ForeignKey(blank=True, null=True, related_name='consumers_for_routing', on_delete=django.db.models.deletion.SET_NULL, to='picmodels.CaseManagementClient'),
        ),
        migrations.AlterField(
            model_name='picconsumerbackup',
            name='cm_client_for_routing',
            field=models.ForeignKey(blank=True, null=True, related_name='consumer_backups_for_routing', on_delete=django.db.models.deletion.SET_NULL, to='picmodels.CaseManagementClient'),
        ),
    ]
