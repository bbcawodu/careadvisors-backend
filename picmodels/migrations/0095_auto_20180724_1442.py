# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0094_auto_20180723_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerPayerData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('member_id_number', models.CharField(max_length=5000, blank=True, null=True)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('risk', models.CharField(max_length=5000, blank=True, null=True)),
                ('coverage_type', models.CharField(max_length=1000, blank=True, null=True, default='Not Available', choices=[('Private', 'Private'), ('ACA', 'ACA'), ('FHP', 'FHP'), ('Medicare', 'Medicare'), ('Dual Eligible', 'Dual Eligible'), ('Not Available', 'Not Available')])),
                ('case_type', models.ForeignKey(blank=True, null=True, related_name='payer_data_for_cases_of_this_type', on_delete=django.db.models.deletion.SET_NULL, to='picmodels.CMSequences')),
                ('consumer', models.ForeignKey(blank=True, null=True, to='picmodels.PICConsumer')),
                ('consumer_backup', models.ForeignKey(blank=True, null=True, to='picmodels.PICConsumerBackup')),
            ],
        ),
        migrations.AlterField(
            model_name='contactlog',
            name='contact_type',
            field=models.CharField(max_length=1000, blank=True, null=True, default='not available', choices=[('Email', 'Email'), ('Text', 'Text'), ('Phone', 'Phone'), ('In-Person', 'In-Person'), ('Mail', 'Mail'), ('Home Visit', 'Home Visit'), ('On Site', 'On Site'), ('not available', 'not available')]),
        ),
        migrations.AlterField(
            model_name='contactlog',
            name='status',
            field=models.CharField(max_length=1000, blank=True, null=True, default='not available', choices=[('Open', 'Open'), ('Voice Message', 'Voice Message'), ('Completed', 'Completed'), ('Pending', 'Pending'), ('WCB', 'WCB'), ('BT', 'BT'), ('NS', 'NS'), ('WN', 'WN'), ('not available', 'not available')]),
        ),
    ]
