# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0031_auto_20161222_2043'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='navmetricslocation',
            unique_together=set([('address',)]),
        ),
    ]
