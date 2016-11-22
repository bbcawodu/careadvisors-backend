# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0023_auto_20161121_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='navmetricslocation',
            name='address',
            field=models.ForeignKey(null=True, blank=True, to='picmodels.Address'),
        ),
        migrations.AlterUniqueTogether(
            name='navmetricslocation',
            unique_together=set([('name', 'address')]),
        ),
        migrations.RemoveField(
            model_name='navmetricslocation',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='navmetricslocation',
            name='address_line2',
        ),
        migrations.RemoveField(
            model_name='navmetricslocation',
            name='city',
        ),
        migrations.RemoveField(
            model_name='navmetricslocation',
            name='country',
        ),
        migrations.RemoveField(
            model_name='navmetricslocation',
            name='state_province',
        ),
        migrations.RemoveField(
            model_name='navmetricslocation',
            name='zipcode',
        ),
    ]
