# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0017_healthcarecarrier_healthcareplan_providerlocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderNetwork',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=10000)),
            ],
        ),
        migrations.AddField(
            model_name='providerlocation',
            name='provider_network',
            field=models.ForeignKey(blank=True, null=True, to='picmodels.ProviderNetwork'),
        ),
    ]
