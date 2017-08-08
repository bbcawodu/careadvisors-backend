# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0039_careadvisorcustomer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='careadvisorcustomer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='careadvisorcustomer',
            name='last_name',
        ),
        migrations.AddField(
            model_name='careadvisorcustomer',
            name='full_name',
            field=models.TextField(default='No name'),
            preserve_default=False,
        ),
    ]
