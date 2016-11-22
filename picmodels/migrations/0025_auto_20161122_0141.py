# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0024_auto_20161121_2316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_line1',
            new_name='address_line_1',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='address_line2',
            new_name='address_line_2',
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('address_line_1', 'address_line_2', 'zipcode', 'city', 'state_province', 'country')]),
        ),
    ]
