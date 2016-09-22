# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0010_auto_20160912_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='NavMetricsLocation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('address_line1', models.CharField(verbose_name='Address line 1', max_length=45)),
                ('address_line2', models.CharField(blank=True, verbose_name='Address line 2', max_length=45)),
                ('zipcode', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('state_province', models.CharField(blank=True, verbose_name='State/Province', max_length=40)),
                ('country', models.ForeignKey(to='picmodels.Country')),
            ],
            options={
                'verbose_name_plural': 'Navigator Metrics Locations',
            },
        ),
        migrations.AlterUniqueTogether(
            name='navmetricslocation',
            unique_together=set([('name', 'address_line1', 'address_line2', 'zipcode', 'city', 'state_province', 'country')]),
        ),
    ]
