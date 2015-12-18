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
    consumer = models.ForeignKey(PICConsumer, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    poc = models.ForeignKey(PICStaff, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.CharField(max_length=2000)
    start_time = models.CharField(max_length=1000)
    end_time = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class PICAppointment(models.Model):
    # fields for appointment model
    consumer = models.ForeignKey(PICConsumer, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    poc = models.ForeignKey(PICStaff, on_delete=models.SET_NULL, blank=True, null=True)
    consumer_f_name = models.CharField(max_length=1000)
    consumer_l_name = models.CharField(default="", max_length=1000)
    consumer_email = models.EmailField()
    consumer_phone = models.CharField(max_length=1000)
    consumer_preferred_language = models.CharField(max_length=1000)
    consumer_best_contact_time = models.CharField(max_length=1000)
    location_name = models.CharField(max_length=1000)
    address = models.CharField(max_length=2000)
    date = models.CharField(max_length=2000)
    start_time = models.CharField(max_length=1000)
    end_time = models.CharField(max_length=1000)
    location_phone = models.CharField(max_length=1000)
    poc_f_name = models.CharField(max_length=1000)
    poc_l_name = models.CharField(max_length=1000)
    poc_email = models.CharField(max_length=1000)
    poc_type = models.CharField(max_length=1000)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

        unique_together = ("consumer_f_name",
                           "consumer_l_name",
                           "consumer_email",
                           "consumer_phone",
                           "consumer_preferred_language",
                           "consumer_best_contact_time",
                           "location_name",
                           "address",
                           "date",
                           "start_time",
                           "end_time",
                           "location_phone",
                           "poc_f_name",
                           "poc_l_name",
                           "poc_email",
                           "poc_type")
