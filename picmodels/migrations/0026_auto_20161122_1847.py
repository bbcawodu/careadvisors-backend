# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0025_auto_20161122_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='picconsumer',
            name='address',
            field=models.ForeignKey(blank=True, to='picmodels.Address', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='picconsumer',
            unique_together=set([('first_name', 'last_name', 'email', 'phone', 'address', 'preferred_language', 'best_contact_time')]),
        ),
        migrations.RemoveField(
            model_name='picconsumer',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='picconsumer',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='picconsumer',
            name='zipcode',
        ),
    ]
