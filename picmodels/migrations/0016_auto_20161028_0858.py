# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0015_auto_20161028_0031'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='navmetricslocation',
            unique_together=set([('address_line1', 'address_line2', 'zipcode', 'city', 'state_province', 'country')]),
        ),
    ]
