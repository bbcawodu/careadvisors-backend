# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0004_auto_20160428_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picstaff',
            name='consumers',
        ),
        migrations.AddField(
            model_name='picconsumer',
            name='navigator',
            field=models.ForeignKey(blank=True, to='picmodels.PICStaff', null=True),
        ),
    ]
