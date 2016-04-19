# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.CharField(max_length=2000)),
                ('start_time', models.CharField(max_length=1000)),
                ('end_time', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000)),
                ('address', models.CharField(max_length=2000)),
                ('phone', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='MetricsSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('received_education', models.IntegerField()),
                ('applied_medicaid', models.IntegerField()),
                ('selected_qhp', models.IntegerField()),
                ('enrolled_shop', models.IntegerField()),
                ('ref_medicaid_or_chip', models.IntegerField()),
                ('ref_shop', models.IntegerField()),
                ('filed_exemptions', models.IntegerField()),
                ('rec_postenroll_support', models.IntegerField()),
                ('trends', models.CharField(default=b'', max_length=5000, blank=True)),
                ('success_story', models.CharField(max_length=5000)),
                ('hardship_or_difficulty', models.CharField(max_length=5000)),
                ('comments', models.CharField(default=b'', max_length=5000, blank=True)),
                ('outreach_stakeholder_activity', models.CharField(default=b'', max_length=5000, blank=True)),
                ('appointments_scheduled', models.IntegerField(null=True, blank=True)),
                ('confirmation_calls', models.IntegerField(null=True, blank=True)),
                ('appointments_held', models.IntegerField(null=True, blank=True)),
                ('appointments_over_hour', models.IntegerField(null=True, blank=True)),
                ('appointments_cmplx_market', models.IntegerField(null=True, blank=True)),
                ('appointments_cmplx_medicaid', models.IntegerField(null=True, blank=True)),
                ('appointments_postenroll_assistance', models.IntegerField(null=True, blank=True)),
                ('appointments_over_three_hours', models.IntegerField(null=True, blank=True)),
                ('submission_date', models.DateField(null=True, blank=True)),
                ('county', models.CharField(default=b'', max_length=1000)),
                ('zipcode', models.CharField(default=b'', max_length=1000)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PICConsumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(default=b'', max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=1000)),
                ('preferred_language', models.CharField(max_length=1000)),
                ('best_contact_time', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PICStaff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(default=b'', max_length=1000)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('type', models.CharField(max_length=1000)),
                ('county', models.CharField(default=b'', max_length=1000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PICUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=1000)),
                ('phone_number', models.CharField(max_length=1000)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlanStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_name', models.CharField(default=b'Miscellaneous', max_length=1000, choices=[(b'All Savers Insurance Company', b'All Savers Insurance Company'), (b'CareSource Indiana, Inc.', b'CareSource Indiana, Inc.'), (b'Humana Health Plan, Inc.', b'Humana Health Plan, Inc.'), (b'Health Alliance Medical Plans, Inc.', b'Health Alliance Medical Plans, Inc.'), (b'Blue Cross Blue Shield of Illinois', b'Blue Cross Blue Shield of Illinois'), (b'Coventry Health Care of Illinois, Inc.', b'Coventry Health Care of Illinois, Inc.'), (b'Coventry Health & Life Co.', b'Coventry Health & Life Co.'), (b'United Healthcare of the Midwest, Inc.', b'United Healthcare of the Midwest, Inc.'), (b'Celtic Insurance Company', b'Celtic Insurance Company'), (b'Harken Health Insurance Company', b'Harken Health Insurance Company'), (b'Aetna Health Inc.', b'Aetna Health Inc.'), (b'Southeastern Indiana Health Organization', b'Southeastern Indiana Health Organization'), (b'Anthem Ins Companies Inc(Anthem BCBS)', b'Anthem Ins Companies Inc(Anthem BCBS)'), (b'Physicians Health Plan of Northern Indiana, Inc.', b'Physicians Health Plan of Northern Indiana, Inc.'), (b'MDwise Marketplace, Inc.', b'MDwise Marketplace, Inc.'), (b'Indiana University Health Plans, Inc.', b'Indiana University Health Plans, Inc.'), (b'Miscellaneous', b'Miscellaneous')])),
                ('premium_type', models.CharField(default=b'Not Available', max_length=1000, blank=True, choices=[(b'HMO', b'HMO'), (b'PPO', b'PP0'), (b'Not Available', b'Not Available')])),
                ('metal_level', models.CharField(default=b'Not Available', max_length=1000, blank=True, choices=[(b'Bronze', b'Bronze'), (b'Silver', b'Silver'), (b'Gold', b'Gold'), (b'Catastrophic', b'Catastrophic'), (b'Not Available', b'Not Available')])),
                ('enrollments', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='picconsumer',
            unique_together=set([('first_name', 'last_name', 'email', 'phone', 'preferred_language', 'best_contact_time')]),
        ),
        migrations.AddField(
            model_name='metricssubmission',
            name='plan_stats',
            field=models.ManyToManyField(to='picmodels.PlanStat'),
        ),
        migrations.AddField(
            model_name='metricssubmission',
            name='staff_member',
            field=models.ForeignKey(to='picmodels.PICStaff'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='consumer',
            field=models.ForeignKey(blank=True, to='picmodels.PICConsumer', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(blank=True, to='picmodels.Location', null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='poc',
            field=models.ForeignKey(blank=True, to='picmodels.PICStaff', null=True),
        ),
    ]
