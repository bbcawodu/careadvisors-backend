from django.db import models
from picmodels.models.care_advisors import NavMetricsLocation
from django.contrib import admin
from oauth2client.contrib.django_util.models import CredentialsField
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import URLValidator

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

from .services.read import retrieve_navigator_data_by_id
from .services.read import retrieve_navigator_data_by_f_and_l_name
from .services.read import retrieve_navigator_data_by_first_name
from .services.read import retrieve_navigator_data_by_last_name
from .services.read import retrieve_navigator_data_by_email
from .services.read import retrieve_navigator_data_by_county
from .services.read import retrieve_navigator_data_by_region
from .services.read import retrieve_navigator_data_by_mpn


import uuid
import os


def get_staff_pic_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('staff_pics', filename)


class Navigators(models.Model):
    # fields for Navigators model
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
    staff_pic = models.ImageField(upload_to=get_staff_pic_file_path, blank=True, null=True)
    base_locations = models.ManyToManyField(NavMetricsLocation, blank=True)

    # Navigator Sign Up fields/columns
    healthcare_locations_worked = models.ManyToManyField(
        'ProviderLocation',
        related_name='navigators_working_here',
        blank=True,
    )
    healthcare_service_expertises = models.ManyToManyField(
        'ProviderLocation',
        related_name='navigators_with_expertise',
        blank=True,
    )
    insurance_carrier_specialties = models.ManyToManyField(
        'HealthcareCarrier',
        blank=True,
    )
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(max_length=1000, blank=True, null=True)
    reported_region = models.CharField(max_length=1000, blank=True, null=True)
    video_link = models.TextField(blank=True, null=True, validators=[URLValidator()])

    def return_values_dict(self):
        valuesdict = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mpn": self.mpn,
            "email": self.email,
            "authorized_redentials": False,
            "type": self.type,
            "id": self.id,
            "county": self.county,
            "region": None,
            "picture": None,
            "base_locations": [],
            "consumers": []
        }

        # consumers = PICConsumer.objects.filter(navigator=self.id)
        consumers = self.picconsumer_set.all()
        consumer_list = []
        if len(consumers):
            for consumer in consumers:
                consumer_list.append(consumer.id)
        valuesdict['consumers'] = consumer_list

        if self.county:
            for region in self.REGIONS:
                if self.county.lower() in self.REGIONS[region]:
                    valuesdict["region"] = region
                    break

        base_locations = self.base_locations.all()
        if len(base_locations):
            base_location_values = []
            for base_location in base_locations:
                base_location_values.append(base_location.return_values_dict())
            valuesdict["base_locations"] = base_location_values

        credentials_queryset = self.credentialsmodel_set.all()
        if len(credentials_queryset):
            for credentials_instance in credentials_queryset:
                if credentials_instance.credential.invalid:
                    credentials_instance.delete()
                else:
                    valuesdict["authorized_credentials"] = True

        if self.staff_pic:
            valuesdict["picture"] = self.staff_pic.url
        else:
            valuesdict["picture"] = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_STAFF_PIC_URL)

        return valuesdict

    def save(self, *args, **kwargs):
        if self.county or self.county != "":
            for region in self.REGIONS:
                if self.county.lower() in self.REGIONS[region]:
                    self.region = region
                    break

        super(Navigators, self).save(*args, **kwargs)

    def __str__(self):
        return "Name: {} {}, id: {}".format(self.first_name, self.last_name, self.id)

    class Meta:
        unique_together = ("email",)
        # maps model to the picmodels module
        app_label = 'picmodels'


Navigators.create_row_w_validated_params = classmethod(create_row_w_validated_params)
Navigators.update_row_w_validated_params = classmethod(update_row_w_validated_params)
Navigators.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)

Navigators.retrieve_navigator_data_by_id = classmethod(retrieve_navigator_data_by_id)
Navigators.retrieve_navigator_data_by_f_and_l_name = classmethod(retrieve_navigator_data_by_f_and_l_name)
Navigators.retrieve_navigator_data_by_first_name = classmethod(retrieve_navigator_data_by_first_name)
Navigators.retrieve_navigator_data_by_last_name = classmethod(retrieve_navigator_data_by_last_name)
Navigators.retrieve_navigator_data_by_email = classmethod(retrieve_navigator_data_by_email)
Navigators.retrieve_navigator_data_by_county = classmethod(retrieve_navigator_data_by_county)
Navigators.retrieve_navigator_data_by_region = classmethod(retrieve_navigator_data_by_region)
Navigators.retrieve_navigator_data_by_mpn = classmethod(retrieve_navigator_data_by_mpn)


@receiver(models.signals.post_delete, sender=Navigators)
def remove_file_from_s3(sender, instance, using, **kwargs):
    if instance.staff_pic:
        default_pic_url = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_STAFF_PIC_URL)
        if instance.staff_pic.url != default_pic_url:
            instance.staff_pic.delete(save=False)


# Maybe add some sort of authorization to our API? OAuth? OAuth2? Some shit?
class CredentialsModel(models.Model):
    id = models.ForeignKey(Navigators, primary_key=True)
    credential = CredentialsField()

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class CredentialsAdmin(admin.ModelAdmin):
    pass


class Resume(models.Model):
    profile_description = models.TextField(blank=True, null=True)
    navigator = models.ForeignKey(Navigators)


class Education(models.Model):
    N_A = "Not Available"
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DEGREE_TYPE_CHOICES = (
        (UNDERGRADUATE, "undergraduate"),
        (GRADUATE, "graduate"),
        (BACHELORS, 'bachelors'),
        (MASTERS, 'masters'),
        (N_A, "Not Available")
    )

    school = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    degree_type = models.CharField(blank=True, null=True, max_length=100, choices=DEGREE_TYPE_CHOICES, default=N_A)
    Resume = models.ForeignKey(Resume)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    Resume = models.ForeignKey(Resume)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
