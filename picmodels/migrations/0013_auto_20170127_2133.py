# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0012_consumernote_consumer_backup'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='picconsumer',
            unique_together=set([]),
        ),
    ]
