# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picmodels.models.care_advisors.navigator_models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0034_auto_20170609_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picstaff',
            name='staff_pic',
            field=models.ImageField(upload_to=picmodels.models.care_advisors.navigator_models.get_staff_pic_file_path, blank=True, null=True),
        ),
    ]
