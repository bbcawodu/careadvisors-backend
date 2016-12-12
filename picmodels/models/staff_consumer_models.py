"""
This file defines the data models for the picproject app
"""

from django.db import models
from picmodels.models import NavMetricsLocation, Address
from django.contrib import admin
from oauth2client.contrib.django_util.models import CredentialsField


class PICStaff(models.Model):
    # fields for PICStaff model
    REGIONS = {"1": ["cook",
                     "collar",
                     "lake",
                     "mchenry",
                     "kane",
                     "kendall",
                     "dupage",
                     "will"],
               "2": ["stephenson",
                     "winnebago",
                     "ogle",
                     "lee",
                     "bureau",
                     "lasalle",
                     "peoria",
                     "livingston",
                     "iroquois",
                     "champaign"],
               "3": ["pike",
                     "scott",
                     "morgan",
                     "calhoun",
                     "greene",
                     "macoupin",
                     "jersey",
                     "montgomery",
                     "fayette",
                     "bond",
                     "marion",
                     "madison",
                     "clinton",
                     "st. clair",
                     "washington",
                     "monroe",
                     "randolph",
                     "perry",
                     "jackson"]}
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(default="", max_length=1000)
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=1000)
    county = models.CharField(blank=True, null=True, max_length=1000, default="")
    region = models.CharField(blank=True, null=True, max_length=1000, default="")
    mpn = models.CharField(blank=True, max_length=1000, default="")
    base_locations = models.ManyToManyField(NavMetricsLocation, blank=True)

    def return_values_dict(self):
        consumers = PICConsumer.objects.filter(navigator=self.id)
        consumer_list = []
        for consumer in consumers:
            consumer_list.append(consumer.return_values_dict()["Database ID"])
        valuesdict = {"First Name": self.first_name,
                      "Last Name": self.last_name,
                      "MPN": self.mpn,
                      "Email": self.email,
                      "Authorized Credentials": False,
                      "Type": self.type,
                      "Database ID": self.id,
                      "County": self.county,
                      "Region": None,
                      "Base Locations": [],
                      "Consumers": consumer_list}

        if self.county:
            for region in self.REGIONS:
                if self.county.lower() in self.REGIONS[region]:
                    valuesdict["Region"] = region
                    break

        base_locations = self.base_locations.all()
        if base_locations:
            for base_location in base_locations:
                valuesdict["Base Locations"].append(base_location.return_values_dict())

        try:
            credentials_object = CredentialsModel.objects.get(id=self.id)
            if credentials_object.credential.invalid:
                credentials_object.delete()
            else:
                valuesdict["Authorized Credentials"] = True
        except CredentialsModel.DoesNotExist:
            pass

        return valuesdict

    def save(self, *args, **kwargs):
        if self.county or self.county != "":
            for region in self.REGIONS:
                if self.county.lower() in self.REGIONS[region]:
                    self.region = region
                    break

        super(PICStaff, self).save(*args, **kwargs)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


# Maybe add some sort of authorization to our API? OAuth? OAuth2? Some shit?
class CredentialsModel(models.Model):
    id = models.ForeignKey(PICStaff, primary_key=True)
    credential = CredentialsField()

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class CredentialsAdmin(admin.ModelAdmin):
    pass


class PICConsumer(models.Model):
    # fields for PICConsumer model
    first_name = models.CharField(max_length=1000)
    middle_name = models.CharField(max_length=1000, blank=True, null=True)
    last_name = models.CharField(default="", max_length=1000)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=1000, blank=True, null=True)
    preferred_language = models.CharField(max_length=1000, blank=True, null=True)
    best_contact_time = models.CharField(max_length=1000, blank=True, null=True)
    navigator = models.ForeignKey(PICStaff, on_delete=models.SET_NULL, blank=True, null=True)

    address = models.ForeignKey(Address, blank=True, null=True)
    household_size = models.IntegerField()
    plan = models.CharField(max_length=1000, blank=True, null=True)
    met_nav_at = models.CharField(max_length=1000)
    date_met_nav = models.DateField(blank=True, null=True)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

        unique_together = ("first_name",
                           "middle_name",
                           "last_name",
                           "email",
                           "phone",
                           "address",
                           "preferred_language",
                           "best_contact_time",
                           "date_met_nav")

    def return_values_dict(self):
        valuesdict = {"First Name": self.first_name,
                      "Middle Name": self.middle_name,
                      "Last Name": self.last_name,
                      "Email": self.email,
                      "Phone Number": self.phone,
                      "Preferred Language": self.preferred_language,
                      "address": None,
                      "Household Size": self.household_size,
                      "Plan": self.plan,
                      "Met Navigator At": self.met_nav_at,
                      "Best Contact Time": self.best_contact_time,
                      "Navigator": "{!s} {!s}".format(self.navigator.first_name, self.navigator.last_name),
                      "Navigator Notes": None,
                      "date_met_nav": None,
                      "Database ID": self.id}

        if self.date_met_nav is not None:
            valuesdict["date_met_nav"] = self.date_met_nav.isoformat()

        navigator_note_objects = ConsumerNote.objects.filter(consumer=self.id)
        navigator_note_list = []
        for navigator_note in navigator_note_objects:
            navigator_note_list.append(navigator_note.navigator_notes)
        valuesdict["Navigator Notes"] = navigator_note_list

        if self.address:
            valuesdict["address"] = {}
            address_values = self.address.return_values_dict()
            for key in address_values:
                valuesdict["address"][key] = address_values[key]

        return valuesdict


class ConsumerNote(models.Model):
    consumer = models.ForeignKey(PICConsumer, on_delete=models.CASCADE)
    navigator_notes = models.TextField(blank=True, default="")

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'