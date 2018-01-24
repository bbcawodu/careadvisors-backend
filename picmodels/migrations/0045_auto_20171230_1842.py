# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import oauth2client.contrib.django_util.models
import picmodels.models.chicago_public_schools.cps_staff_consumer_models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0044_auto_20171229_0048'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPSStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(max_length=1000, default='')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('type', models.CharField(max_length=1000)),
                ('county', models.CharField(null=True, default='', max_length=1000, blank=True)),
                ('region', models.CharField(null=True, default='', max_length=1000, blank=True)),
                ('cps_staff_pic', models.ImageField(upload_to=picmodels.models.chicago_public_schools.cps_staff_consumer_models.get_cps_staff_pic_file_path, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CPSGoogleCredential',
            fields=[
                ('id', models.ForeignKey(serialize=False, to='picmodels.CPSStaff', primary_key=True)),
                ('credential', oauth2client.contrib.django_util.models.CredentialsField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cpsstaff',
            name='base_locations',
            field=models.ManyToManyField(to='picmodels.NavMetricsLocation', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='cpsstaff',
            unique_together=set([('email',)]),
        ),
    ]
