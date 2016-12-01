# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0028_picconsumer_date_met_nav'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='picconsumer',
            unique_together=set([('first_name', 'last_name', 'email', 'phone', 'address', 'preferred_language', 'best_contact_time', 'date_met_nav')]),
        ),
    ]
