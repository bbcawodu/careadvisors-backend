# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0030_auto_20161205_2034'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='picconsumer',
            unique_together=set([('email',)]),
        ),
        migrations.AlterUniqueTogether(
            name='picstaff',
            unique_together=set([('email',)]),
        ),
    ]
