# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picmodels.models.care_advisors.navigator_models.models
import custom_storages


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0064_auto_20180411_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navigators',
            name='resume_file',
            field=models.FileField(blank=True, null=True, upload_to=picmodels.models.care_advisors.navigator_models.get_nav_resume_file_path, storage=custom_storages.PublicMediaStorage()),
        ),
        migrations.AlterField(
            model_name='navigators',
            name='staff_pic',
            field=models.ImageField(blank=True, null=True, upload_to=picmodels.models.care_advisors.navigator_models.get_staff_pic_file_path, storage=custom_storages.PublicMediaStorage()),
        ),
    ]
