# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picmodels', '0074_auto_20180529_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUpNotices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('status', models.CharField(max_length=1000, blank=True, null=True, default='not available', choices=[('Open', 'Open'), ('Completed', 'Completed'), ('not available', 'not available')])),
                ('severity', models.CharField(max_length=1000, blank=True, null=True, default='not available', choices=[('Low', 'Low'), ('Normal', 'Normal'), ('HIGH', 'HIGH'), ('Urgent', 'Urgent'), ('not available', 'not available')])),
                ('date_created', models.DateTimeField(null=True, auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('consumer', models.ForeignKey(to='picmodels.PICConsumer')),
                ('navigator', models.ForeignKey(to='picmodels.Navigators')),
            ],
        ),
    ]
