from django.db import models
from picmodels.models.care_advisors import NavMetricsLocation
from django.contrib import admin
from oauth2client.contrib.django_util.models import CredentialsField
from django.dispatch import receiver
from django.conf import settings

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params

from .services.read import retrieve_staff_data_by_id
from .services.read import retrieve_staff_data_by_f_and_l_name
from .services.read import retrieve_staff_data_by_first_name
from .services.read import retrieve_staff_data_by_last_name
from .services.read import retrieve_staff_data_by_email
from .services.read import retrieve_staff_data_by_county
from .services.read import retrieve_staff_data_by_region
from .services.read import retrieve_staff_data_by_mpn


import uuid
import os


def get_staff_pic_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('staff_pics', filename)


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
    staff_pic = models.ImageField(upload_to=get_staff_pic_file_path, blank=True, null=True)
    base_locations = models.ManyToManyField(NavMetricsLocation, blank=True)

    def return_values_dict(self):
        valuesdict = {"First Name": self.first_name,
                      "Last Name": self.last_name,
                      "MPN": self.mpn,
                      "Email": self.email,
                      "Authorized Credentials": False,
                      "Type": self.type,
                      "Database ID": self.id,
                      "County": self.county,
                      "Region": None,
                      "Picture": None,
                      "Base Locations": [],
                      "Consumers": []}

        # consumers = PICConsumer.objects.filter(navigator=self.id)
        consumers = self.picconsumer_set.all()
        consumer_list = []
        if len(consumers):
            for consumer in consumers:
                consumer_list.append(consumer.id)
        valuesdict['Consumers'] = consumer_list

        if self.county:
            for region in self.REGIONS:
                if self.county.lower() in self.REGIONS[region]:
                    valuesdict["Region"] = region
                    break

        base_locations = self.base_locations.all()
        if len(base_locations):
            base_location_values = []
            for base_location in base_locations:
                base_location_values.append(base_location.return_values_dict())
            valuesdict["Base Locations"] = base_location_values

        credentials_queryset = self.credentialsmodel_set.all()
        if len(credentials_queryset):
            for credentials_instance in credentials_queryset:
                if credentials_instance.credential.invalid:
                    credentials_instance.delete()
                else:
                    valuesdict["Authorized Credentials"] = True

        if self.staff_pic:
            valuesdict["Picture"] = self.staff_pic.url
        else:
            valuesdict["Picture"] = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_STAFF_PIC_URL)

        return valuesdict

    def save(self, *args, **kwargs):
        if self.county or self.county != "":
            for region in self.REGIONS:
                if self.county.lower() in self.REGIONS[region]:
                    self.region = region
                    break

        super(PICStaff, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("email",)
        # maps model to the picmodels module
        app_label = 'picmodels'


PICStaff.create_row_w_validated_params = classmethod(create_row_w_validated_params)
PICStaff.update_row_w_validated_params = classmethod(update_row_w_validated_params)
PICStaff.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)

PICStaff.retrieve_staff_data_by_id = classmethod(retrieve_staff_data_by_id)
PICStaff.retrieve_staff_data_by_f_and_l_name = classmethod(retrieve_staff_data_by_f_and_l_name)
PICStaff.retrieve_staff_data_by_first_name = classmethod(retrieve_staff_data_by_first_name)
PICStaff.retrieve_staff_data_by_last_name = classmethod(retrieve_staff_data_by_last_name)
PICStaff.retrieve_staff_data_by_email = classmethod(retrieve_staff_data_by_email)
PICStaff.retrieve_staff_data_by_county = classmethod(retrieve_staff_data_by_county)
PICStaff.retrieve_staff_data_by_region = classmethod(retrieve_staff_data_by_region)
PICStaff.retrieve_staff_data_by_mpn = classmethod(retrieve_staff_data_by_mpn)


@receiver(models.signals.post_delete, sender=PICStaff)
def remove_file_from_s3(sender, instance, using, **kwargs):
    if instance.staff_pic:
        default_pic_url = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_STAFF_PIC_URL)
        if instance.staff_pic.url != default_pic_url:
            instance.staff_pic.delete(save=False)


# Maybe add some sort of authorization to our API? OAuth? OAuth2? Some shit?
class CredentialsModel(models.Model):
    id = models.ForeignKey(PICStaff, primary_key=True)
    credential = CredentialsField()

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class CredentialsAdmin(admin.ModelAdmin):
    pass
