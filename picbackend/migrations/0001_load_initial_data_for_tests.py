# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


from django.core.management import call_command

fixture = '12-27-2016.json'


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture)


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0032_auto_20161222_2106'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]