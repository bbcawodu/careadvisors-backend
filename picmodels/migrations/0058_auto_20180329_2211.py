# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0057_auto_20180329_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='Resume',
            new_name='resume',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='Resume',
            new_name='resume',
        ),
    ]
