# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0022_auto_20161121_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('address_line1', models.CharField(max_length=45, verbose_name='Address line 1')),
                ('address_line2', models.CharField(blank=True, max_length=45, verbose_name='Address line 2')),
                ('zipcode', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('state_province', models.CharField(blank=True, max_length=40, verbose_name='State/Province')),
                ('country', models.ForeignKey(to='picmodels.Country')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('address_line1', 'address_line2', 'zipcode', 'city', 'state_province', 'country')]),
        ),
    ]
