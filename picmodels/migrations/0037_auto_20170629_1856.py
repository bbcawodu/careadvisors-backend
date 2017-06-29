# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0036_auto_20170609_2005'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='picstaff',
            unique_together=set([('email',)]),
        ),
    ]
