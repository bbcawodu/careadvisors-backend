# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0077_cmsequences'),
    ]

    operations = [
        migrations.AddField(
            model_name='casemanagementclient',
            name='cm_sequences',
            field=models.ManyToManyField(blank=True, related_name='cm_clients_that_use_this_sequence', to='picmodels.CMSequences'),
        ),
    ]
