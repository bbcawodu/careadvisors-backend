# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0013_auto_20170127_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumernote',
            name='consumer',
            field=models.ForeignKey(blank=True, null=True, to='picmodels.PICConsumer'),
        ),
    ]
