"""
This file defines the data models for the picproject app
"""

from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class PICUser(models.Model):
    # one to one reference to django built in user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional fields for PICUser model
    address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=1000)

    # maps model to the picmodels module
    class Meta:
        app_label = 'picmodels'


class PICConsumer(models.Model):
    # fields for PICConsumer model
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(default="", max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=1000)
    preferred_language = models.CharField(max_length=1000)
    best_contact_time = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

        unique_together = ("first_name",
                           "last_name",
                           "email",
                           "phone",
                           "preferred_language",
                           "best_contact_time")


class Location(models.Model):
    # fields for Location model
    name = models.CharField(max_length=1000)
    address = models.CharField(max_length=2000)
    phone = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class PICStaff(models.Model):
    # fields for PICStaff model
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(default="", max_length=1000)
    email = models.EmailField()
    type = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class Appointment(models.Model):
    # fields for appointment model
    consumer = models.ForeignKey(PICConsumer, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    poc = models.ForeignKey(PICStaff, on_delete=models.CASCADE, blank=True, null=True)
    date = models.CharField(max_length=2000)
    start_time = models.CharField(max_length=1000)
    end_time = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class MetricsSubmission(models.Model):
    # fields for PICStaff model
    staff_member = models.ForeignKey(PICStaff, on_delete=models.CASCADE)
    received_education = models.IntegerField()
    applied_medicaid = models.IntegerField()
    selected_qhp = models.IntegerField()
    enrolled_shop = models.IntegerField()
    ref_medicaid_or_chip = models.IntegerField()
    ref_shop = models.IntegerField()
    filed_exemptions = models.IntegerField()
    rec_postenroll_support = models.IntegerField()
    trends = models.CharField(max_length=5000)
    success_story = models.CharField(max_length=5000)
    hardship_or_difficulty = models.CharField(max_length=5000)
    comments = models.CharField(max_length=5000, blank=True, null=True)
    outreach_stakeholder_activity = models.CharField(max_length=5000, blank=True, null=True)
    appointments_scheduled = models.IntegerField(null=True)
    confirmation_calls = models.IntegerField(null=True)
    appointments_held = models.IntegerField(null=True)
    appointments_over_hour = models.IntegerField(null=True)
    appointments_cmplx_market = models.IntegerField(null=True)
    appointments_cmplx_medicaid = models.IntegerField(null=True)
    appointments_postenroll_assistance = models.IntegerField(null=True)
    appointments_over_three_hours = models.IntegerField(null=True)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'