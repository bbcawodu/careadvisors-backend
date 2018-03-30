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

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_f_and_l_name
from .services.read import get_serialized_rows_by_first_name
from .services.read import get_serialized_rows_by_last_name
from .services.read import get_serialized_rows_by_email
from .services.read import get_serialized_rows_by_county
from .services.read import get_serialized_rows_by_region
from .services.read import get_serialized_rows_by_mpn


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
        'HealthcareServiceExpertise',
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
            "consumers": [],

            "healthcare_locations_worked": None,
            "healthcare_service_expertises": None,
            "insurance_carrier_specialties": None,
            "resume_info": None,
            "phone": self.phone,
            "reported_region": self.reported_region,
            "video_link": self.video_link,
            "address": None,
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

        if self.address:
            valuesdict["address"] = {}
            address_values = self.address.return_values_dict()
            for key in address_values:
                valuesdict["address"][key] = address_values[key]

        healthcare_locations_worked = self.healthcare_locations_worked.all()
        if len(healthcare_locations_worked):
            healthcare_locations_worked_values = []
            for location_worked in healthcare_locations_worked:
                location_info = {
                    "name": location_worked.name,
                    "state_province": location_worked.state_province,
                    "id": location_worked.id
                }
                healthcare_locations_worked_values.append(location_info)
            valuesdict["healthcare_locations_worked"] = healthcare_locations_worked_values

        healthcare_service_expertises = self.healthcare_service_expertises.all()
        if len(healthcare_service_expertises):
            healthcare_service_expertises_values = []
            for service_expertise in healthcare_service_expertises:
                healthcare_service_expertises_values.append(service_expertise.name)
            valuesdict["healthcare_service_expertises"] = healthcare_service_expertises_values

        insurance_carrier_specialties = self.insurance_carrier_specialties.all()
        if len(insurance_carrier_specialties):
            insurance_carrier_specialties_values = []
            for insurance_carrier_specialty in insurance_carrier_specialties:
                insurance_carrier_specialty_info = {
                    "name": insurance_carrier_specialty.name,
                    "state_province": insurance_carrier_specialty.state_province,
                    "id": insurance_carrier_specialty.id
                }
                insurance_carrier_specialties_values.append(insurance_carrier_specialty_info)
            valuesdict["insurance_carrier_specialties"] = insurance_carrier_specialties_values

        resume_qset = self.resume_set.all()
        if len(resume_qset):
            resume_values = []
            for resume in resume_qset:
                resume_values.append(resume.return_values_dict())
            valuesdict["resume_info"] = resume_values

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

Navigators.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
Navigators.get_serialized_rows_by_f_and_l_name = classmethod(get_serialized_rows_by_f_and_l_name)
Navigators.get_serialized_rows_by_first_name = classmethod(get_serialized_rows_by_first_name)
Navigators.get_serialized_rows_by_last_name = classmethod(get_serialized_rows_by_last_name)
Navigators.get_serialized_rows_by_email = classmethod(get_serialized_rows_by_email)
Navigators.get_serialized_rows_by_county = classmethod(get_serialized_rows_by_county)
Navigators.get_serialized_rows_by_region = classmethod(get_serialized_rows_by_region)
Navigators.get_serialized_rows_by_mpn = classmethod(get_serialized_rows_by_mpn)


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
    navigator = models.ForeignKey(Navigators, on_delete=models.CASCADE)

    def return_values_dict(self):
        values_dict = {
            "profile_description": self.profile_description,
            "id": self.id,
            "education_info": None,
            "job_info": None
        }

        education_qset = self.education_set.all()
        if len(education_qset):
            education_values = []
            for education in education_qset:
                education_values.append(education.return_values_dict())
            values_dict["education_info"] = education_values

        job_qset = self.job_set.all()
        if len(job_qset):
            job_values = []
            for job in job_qset:
                job_values.append(job.return_values_dict())
            values_dict["job_info"] = job_values

        return values_dict


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

    school = models.CharField(max_length=1000, blank=True, null=True)
    major = models.CharField(max_length=1000, blank=True, null=True)
    degree_type = models.CharField(blank=True, null=True, max_length=100, choices=DEGREE_TYPE_CHOICES, default=N_A)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def return_values_dict(self):
        values_dict = {
            "school": self.school,
            "major": self.major,
            "degree_type": self.degree_type,
            "id": self.id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }

        return values_dict

    def check_degree_type_choices(self,):
        for degree_type_tuple in self.DEGREE_TYPE_CHOICES:
            if degree_type_tuple[1].lower() == self.degree_type.lower():
                return True
        return False


class Job(models.Model):
    title = models.CharField(max_length=2000, blank=True, null=True)
    company = models.CharField(max_length=2000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def return_values_dict(self):
        values_dict = {
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "id": self.id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }

        return values_dict
