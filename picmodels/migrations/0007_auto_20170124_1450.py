# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0006_auto_20170123_2150'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='picconsumer',
            unique_together=set([('first_name', 'last_name', 'navigator')]),
        ),
    ]