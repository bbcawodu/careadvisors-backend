# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 08:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0002_navmetricslocation_cps_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerCPSInfoEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='cps_consumer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='consumercpsinfoentry',
            name='consumer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cps_info', to='picmodels.PICConsumer'),
        ),
        migrations.AddField(
            model_name='consumercpsinfoentry',
            name='cps_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='picmodels.NavMetricsLocation'),
        ),
        migrations.AddField(
            model_name='consumercpsinfoentry',
            name='primary_dependent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_guardian', to='picmodels.PICConsumer'),
        ),
        migrations.AddField(
            model_name='consumercpsinfoentry',
            name='secondary_dependents',
            field=models.ManyToManyField(blank=True, related_name='secondary_guardians', to='picmodels.PICConsumer'),
        ),
    ]