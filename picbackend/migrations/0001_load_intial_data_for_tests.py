# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


from django.core.management import call_command

fixture = '01-23-2017.json'


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture)


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0005_auto_20170117_1652'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]