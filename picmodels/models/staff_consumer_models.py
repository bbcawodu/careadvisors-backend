"""
This file defines the data models for the picproject app
"""

from django.db import models
from picmodels.models import NavMetricsLocation, Address
from django.contrib import admin
from oauth2client.contrib.django_util.models import CredentialsField
from django.dispatch import receiver
from django.conf import settings
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


class PICConsumerBaseQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            if obj.cps_info:
                obj.cps_info.delete()
        super(PICConsumerBaseQuerySet, self).delete(*args, **kwargs)


class PICConsumerBase(models.Model):
    objects = PICConsumerBaseQuerySet.as_manager()

    # fields for PICConsumer model
    first_name = models.CharField(max_length=1000)
    middle_name = models.CharField(max_length=1000, blank=True, null=True)
    last_name = models.CharField(default="", max_length=1000)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=1000, blank=True, null=True)
    preferred_language = models.CharField(max_length=1000, blank=True, null=True)
    best_contact_time = models.CharField(max_length=1000, blank=True, null=True)
    navigator = models.ForeignKey(PICStaff, on_delete=models.SET_NULL, blank=True, null=True)
    # navigators = models.ManyToManyField(PICStaff, blank=True)

    address = models.ForeignKey(Address, blank=True, null=True)
    household_size = models.IntegerField()
    plan = models.CharField(max_length=1000, blank=True, null=True)
    met_nav_at = models.CharField(max_length=1000)
    date_met_nav = models.DateField(blank=True, null=True)

    cps_consumer = models.BooleanField(default=False)
    cps_info = models.ForeignKey('ConsumerCPSInfoEntry', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
        abstract = True

    def get_primary_guardian_qset(self):
        primary_guardian_qset = None

        cps_info_qset = self.primary_guardian.all()
        if len(cps_info_qset):
            for cps_info_instance in cps_info_qset:
                primary_guardian_qset_for_this_cps_info = cps_info_instance.picconsumer_set.all()

                if primary_guardian_qset is not None:
                    primary_guardian_qset = primary_guardian_qset | primary_guardian_qset_for_this_cps_info
                else:
                    primary_guardian_qset = primary_guardian_qset_for_this_cps_info

        return primary_guardian_qset

    def get_secondary_guardian_qset(self):
        secondary_guardian_qset = None

        cps_info_qset = self.secondary_guardians.all()
        if len(cps_info_qset):
            for cps_info_instance in cps_info_qset:
                secondary_guardian_qset_for_this_cps_info = cps_info_instance.picconsumer_set.all()

                if secondary_guardian_qset is not None:
                    secondary_guardian_qset = secondary_guardian_qset | secondary_guardian_qset_for_this_cps_info
                else:
                    secondary_guardian_qset = secondary_guardian_qset_for_this_cps_info

        return secondary_guardian_qset

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
                      "Navigator": None,
                      "Navigator Notes": None,
                      "date_met_nav": None,
                      "cps_consumer": self.cps_consumer,
                      "cps_info": None,
                      "primary_guardians": None,
                      "secondary_guardians": None,
                      "Database ID": self.id}

        if self.date_met_nav:
            valuesdict["date_met_nav"] = self.date_met_nav.isoformat()

        if self.consumernote_set:
            navigator_note_objects = self.consumernote_set.all()
            navigator_note_list = []

            if len(navigator_note_objects):
                for navigator_note in navigator_note_objects:
                    navigator_note_list.append(navigator_note.navigator_notes)

            valuesdict["Navigator Notes"] = navigator_note_list

        if self.address:
            valuesdict["address"] = {}
            address_values = self.address.return_values_dict()
            for key in address_values:
                valuesdict["address"][key] = address_values[key]

        if self.navigator:
            valuesdict['Navigator'] = "{!s} {!s}".format(self.navigator.first_name, self.navigator.last_name)

        if self.cps_info:
            valuesdict['cps_info'] = self.cps_info.return_values_dict()

        # if self.primary_guardian:
        #     primary_guardian_info = []
        #
        #     primary_guardian_qset = self.get_primary_guardian_qset()
        #     if primary_guardian_qset is not None:
        #         if len(primary_guardian_qset):
        #             for primary_guardian_instance in primary_guardian_qset:
        #                 primary_guardian_info.append(primary_guardian_instance.id)
        #
        #     if primary_guardian_info:
        #         valuesdict["primary_guardians"] = primary_guardian_info
        #
        # if self.secondary_guardians:
        #     secondary_guardian_info = []
        #
        #     secondary_guardian_qset = self.get_secondary_guardian_qset()
        #     if secondary_guardian_qset is not None:
        #         if len(secondary_guardian_qset):
        #             for secondary_guardian_instance in secondary_guardian_qset:
        #                 secondary_guardian_info.append(secondary_guardian_instance.id)
        #
        #     if secondary_guardian_info:
        #         valuesdict["secondary_guardians"] = secondary_guardian_info

        return valuesdict

    def delete(self, *args, **kwargs):
        if self.cps_info:
            self.cps_info.delete()
        super(PICConsumerBase, self).delete(*args, **kwargs)


class PICConsumer(PICConsumerBase):

    class Meta(PICConsumerBase.Meta):
        unique_together = ()


class PICConsumerBackup(PICConsumerBase):
    pass


class ConsumerNote(models.Model):
    consumer = models.ForeignKey(PICConsumer, on_delete=models.CASCADE, blank=True, null=True)
    consumer_backup = models.ForeignKey(PICConsumerBackup, on_delete=models.CASCADE, blank=True, null=True)
    navigator_notes = models.TextField(blank=True, default="")

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class ConsumerCPSInfoEntry(models.Model):
    """
    Need to validate ALL form data before creating PICConsumer entries and by extention, ConsumerCPSInfoEntry
    """

    N_A = "Not Available"
    OPEN = "Open"
    RESOLVED = "Resloved"
    CASE_MGMT_STATUS_CHOICES = ((OPEN, "Open"),
                                (RESOLVED, "Resolved"),
                                (N_A, "Not Available"))

    MEDICAID = "Medicaid"
    SNAP = "SNAP"
    MEDICAID_SNAP = "Medicaid/SNAP"
    REDETERMINATION = "Redetermination"
    PLAN_SELECTION = "Plan Selection"
    FAX_FCRC = "Fax FCRC"
    EDUCATION = "Education"
    MMCO = "MMCO"
    APP_TYPE_CHOICES = ((MEDICAID, "Medicaid"),
                        (SNAP, "SNAP"),
                        (MEDICAID_SNAP, "Medicaid/SNAP"),
                        (REDETERMINATION, "Redetermination"),
                        (PLAN_SELECTION, "Plan Selection"),
                        (FAX_FCRC, "Fax FCRC"),
                        (EDUCATION, "Education"),
                        (MMCO, "MMCO"),
                        (N_A, "Not Available"))

    SUBMITTED = "Submitted"
    PENDING = "Pending"
    APPROVED = "Approved"
    DENIED = "Denied"
    APP_STATUS_CHOICES = ((SUBMITTED, "Submitted"),
                          (PENDING, "Pending"),
                          (APPROVED, "Approved"),
                          (DENIED, "Denied"),
                          (N_A, "Not Available"))

    WALK_IN = "Walk-in"
    APPOINTMENT = "Appointment"
    REFERRAL_FROM_CALL = "Referral from call"
    REFERRAL_FROM_SCHOOL_LETTER = "Referral from school letter"
    ENROLLMENT_EVENT = "Enrollment event"
    POINT_OF_ORIGIN_CHOICES = (
        (WALK_IN, "Walk-in"),
        (APPOINTMENT, "Appointment"),
        (REFERRAL_FROM_CALL, "Referral from call"),
        (REFERRAL_FROM_SCHOOL_LETTER, "Referral from school letter"),
        (ENROLLMENT_EVENT, "Enrollment event"),
        (N_A, "Not Available")
    )

    primary_dependent = models.ForeignKey(PICConsumer, on_delete=models.SET_NULL, blank=True, null=True, related_name='primary_guardian')
    secondary_dependents = models.ManyToManyField(PICConsumer, blank=True, related_name='secondary_guardians')

    cps_location = models.ForeignKey(NavMetricsLocation, blank=True, null=True)

    apt_date = models.DateField(blank=True, null=True)
    target_list = models.BooleanField(default=False)
    phone_apt = models.BooleanField(default=False)
    case_mgmt_type = models.CharField(max_length=1000, blank=True, null=True)
    case_mgmt_status = models.CharField(max_length=1000, blank=True, null=True, choices=CASE_MGMT_STATUS_CHOICES, default=N_A)
    app_type = models.CharField(max_length=1000, blank=True, null=True, choices=APP_TYPE_CHOICES, default=N_A)
    app_status = models.CharField(max_length=1000, blank=True, null=True, choices=APP_STATUS_CHOICES, default=N_A)
    point_of_origin = models.CharField(max_length=1000, blank=True, null=True, choices=POINT_OF_ORIGIN_CHOICES, default=N_A)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

    def check_case_mgmt_status_choices(self,):
        for plan_tuple in self.CASE_MGMT_STATUS_CHOICES:
            if plan_tuple[1].lower() == self.case_mgmt_status.lower():
                return True
        return False

    def check_app_type_choices(self,):
        for plan_tuple in self.APP_TYPE_CHOICES:
            if plan_tuple[1].lower() == self.app_type.lower():
                return True
        return False

    def check_app_status_choices(self,):
        for plan_tuple in self.APP_STATUS_CHOICES:
            if plan_tuple[1].lower() == self.app_status.lower():
                return True
        return False

    def check_point_of_origin_choices(self,):
        for point_of_origin_tuple in self.POINT_OF_ORIGIN_CHOICES:
            if point_of_origin_tuple[1].lower() == self.point_of_origin.lower():
                return True
        return False

    def return_values_dict(self):
        valuesdict = {"apt_date": None,
                      "target_list": self.target_list,
                      "phone_apt": self.phone_apt,
                      "case_mgmt_type": self.case_mgmt_type,
                      "case_mgmt_status": self.case_mgmt_status,
                      "app_type": self.app_type,
                      "app_status": self.app_status,
                      "point_of_origin": self.point_of_origin,
                      "cps_location": None,
                      "primary_dependent": None,
                      "secondary_dependents": None,
                      "Database ID": self.id}

        if self.apt_date:
            valuesdict["apt_date"] = self.apt_date.isoformat()

        if self.cps_location:
            valuesdict["cps_location"] = self.cps_location.name

        if self.primary_dependent:
            primary_dependent_entry = {"first_name": self.primary_dependent.first_name,
                                       "last_name": self.primary_dependent.last_name,
                                       "Database ID": self.primary_dependent.id}
            valuesdict["primary_dependent"] = primary_dependent_entry

        if self.secondary_dependents:
            secondary_dependent_queryset = self.secondary_dependents.all()
            if len(secondary_dependent_queryset):
                secondary_dependent_list = []
                for secondary_dependent in secondary_dependent_queryset:
                    dependent_entry = {"first_name": secondary_dependent.first_name,
                                       "last_name": secondary_dependent.last_name,
                                       "Database ID": secondary_dependent.id}
                    secondary_dependent_list.append(dependent_entry)
                valuesdict["secondary_dependents"] = secondary_dependent_list

        return valuesdict
