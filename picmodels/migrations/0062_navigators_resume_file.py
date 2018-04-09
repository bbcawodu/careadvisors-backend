# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import picmodels.models.care_advisors.navigator_models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0061_navigators_navigator_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigators',
            name='resume_file',
            field=models.FileField(blank=True, upload_to=picmodels.models.care_advisors.navigator_models.get_nav_resume_file_path, null=True),
        ),
    ]
