from django.db import models
from picmodels.models.care_advisors import NavMetricsLocation
from oauth2client.contrib.django_util.models import CredentialsField
from django.dispatch import receiver
from django.conf import settings
import uuid
import os

from .services.create_update_delete import create_staff_row_using_validated_params
from .services.create_update_delete import modify_staff_row_using_validated_params
from .services.create_update_delete import delete_staff_row_using_validated_params

from .services.read import retrieve_staff_data_by_id
from .services.read import filter_staff_qset_by_id
from .services.read import retrieve_staff_data_by_email
from .services.read import filter_staff_qset_by_email
from .services.read import retrieve_staff_data_by_f_and_l_name
from .services.read import filter_staff_qset_by_f_and_l_name
from .services.read import retrieve_staff_data_by_first_name
from .services.read import filter_staff_qset_by_first_name
from .services.read import retrieve_staff_data_by_last_name
from .services.read import filter_staff_qset_by_last_name
from .services.read import retrieve_staff_data_by_county
from .services.read import filter_staff_qset_by_county
from .services.read import retrieve_staff_data_by_region


def get_cps_staff_pic_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('staff_pics/cps', filename)


class CPSStaff(models.Model):
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
    cps_staff_pic = models.ImageField(upload_to=get_cps_staff_pic_file_path, blank=True, null=True)
    base_locations = models.ManyToManyField(NavMetricsLocation, blank=True)

    def return_values_dict(self):
        valuesdict = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "authorized_credentials": False,
            "type": self.type,
            "id": self.id,
            "county": self.county,
            "region": None,
            "picture": None,
            "base_locations": [],
            "consumers": []
        }

        # consumers = self.picconsumer_set.all()
        # consumer_list = []
        # if len(consumers):
        #     for consumer in consumers:
        #         consumer_list.append(consumer.id)
        # valuesdict['Consumers'] = consumer_list

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

        credentials_queryset = self.cpsgooglecredential_set.all()
        if len(credentials_queryset):
            for credentials_instance in credentials_queryset:
                if credentials_instance.credential.invalid:
                    credentials_instance.delete()
                else:
                    valuesdict["authorized_credentials"] = True

        if self.cps_staff_pic:
            valuesdict["picture"] = self.cps_staff_pic.url
        else:
            valuesdict["picture"] = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_STAFF_PIC_URL)

        return valuesdict

    def save(self, *args, **kwargs):
        if self.county or self.county != "":
            for region in self.REGIONS:
                if self.county.lower() in self.REGIONS[region]:
                    self.region = region
                    break

        super(CPSStaff, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("email",)

        # maps model to the picmodels module
        app_label = 'picmodels'


CPSStaff.create_staff_row_using_validated_params = classmethod(create_staff_row_using_validated_params)
CPSStaff.modify_staff_row_using_validated_params = classmethod(modify_staff_row_using_validated_params)
CPSStaff.delete_staff_row_using_validated_params = classmethod(delete_staff_row_using_validated_params)

CPSStaff.retrieve_staff_data_by_id = classmethod(retrieve_staff_data_by_id)
CPSStaff.filter_staff_qset_by_id = classmethod(filter_staff_qset_by_id)

CPSStaff.retrieve_staff_data_by_email = classmethod(retrieve_staff_data_by_email)
CPSStaff.filter_staff_qset_by_email = classmethod(filter_staff_qset_by_email)

CPSStaff.retrieve_staff_data_by_f_and_l_name = classmethod(retrieve_staff_data_by_f_and_l_name)
CPSStaff.filter_staff_qset_by_f_and_l_name = classmethod(filter_staff_qset_by_f_and_l_name)

CPSStaff.retrieve_staff_data_by_first_name = classmethod(retrieve_staff_data_by_first_name)
CPSStaff.filter_staff_qset_by_first_name = classmethod(filter_staff_qset_by_first_name)

CPSStaff.retrieve_staff_data_by_last_name = classmethod(retrieve_staff_data_by_last_name)
CPSStaff.filter_staff_qset_by_last_name = classmethod(filter_staff_qset_by_last_name)

CPSStaff.retrieve_staff_data_by_county = classmethod(retrieve_staff_data_by_county)
CPSStaff.filter_staff_qset_by_county = classmethod(filter_staff_qset_by_county)

CPSStaff.retrieve_staff_data_by_region = classmethod(retrieve_staff_data_by_region)


@receiver(models.signals.post_delete, sender=CPSStaff)
def remove_file_from_s3(sender, instance, using, **kwargs):
    if instance.cps_staff_pic:
        default_pic_url = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_STAFF_PIC_URL)
        if instance.cps_staff_pic.url != default_pic_url:
            instance.cps_staff_pic.delete(save=False)


# Maybe add some sort of authorization to our API? OAuth? OAuth2? Some shit?
class CPSGoogleCredential(models.Model):
    id = models.ForeignKey(CPSStaff, primary_key=True)
    credential = CredentialsField()

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
#
#
# class PICConsumerBaseQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for obj in self:
#             if obj.cps_info:
#                 obj.cps_info.delete()
#             if obj.consumer_hospital_info:
#                 obj.consumer_hospital_info.delete()
#         super(PICConsumerBaseQuerySet, self).delete(*args, **kwargs)
#
#
# class PICConsumerBase(models.Model):
#     objects = PICConsumerBaseQuerySet.as_manager()
#
#     # fields for PICConsumer model
#     first_name = models.CharField(max_length=1000)
#     middle_name = models.CharField(max_length=1000, blank=True, null=True)
#     last_name = models.CharField(default="", max_length=1000)
#     email = models.EmailField(blank=True)
#     phone = models.CharField(max_length=1000, blank=True, null=True)
#     preferred_language = models.CharField(max_length=1000, blank=True, null=True)
#     best_contact_time = models.CharField(max_length=1000, blank=True, null=True)
#     navigator = models.ForeignKey(PICStaff, on_delete=models.SET_NULL, blank=True, null=True)
#     # navigators = models.ManyToManyField(PICStaff, blank=True)
#
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
#     household_size = models.IntegerField()
#     plan = models.CharField(max_length=1000, blank=True, null=True)
#     met_nav_at = models.CharField(max_length=1000)
#     date_met_nav = models.DateField(blank=True, null=True)
#
#     cps_consumer = models.BooleanField(default=False)
#     cps_info = models.ForeignKey('ConsumerCPSInfoEntry', on_delete=models.SET_NULL, blank=True, null=True)
#     consumer_hospital_info = models.ForeignKey('ConsumerHospitalInfo', on_delete=models.SET_NULL, blank=True, null=True)
#
#     class Meta:
#         # maps model to the picmodels module
#         app_label = 'picmodels'
#         abstract = True
#
#     def get_primary_guardian_qset(self):
#         primary_guardian_qset = None
#
#         cps_info_qset = self.primary_guardian.all()
#         if len(cps_info_qset):
#             for cps_info_instance in cps_info_qset:
#                 primary_guardian_qset_for_this_cps_info = cps_info_instance.picconsumer_set.all()
#
#                 if primary_guardian_qset is not None:
#                     primary_guardian_qset = primary_guardian_qset | primary_guardian_qset_for_this_cps_info
#                 else:
#                     primary_guardian_qset = primary_guardian_qset_for_this_cps_info
#
#         return primary_guardian_qset
#
#     def get_secondary_guardian_qset(self):
#         secondary_guardian_qset = None
#
#         cps_info_qset = self.secondary_guardians.all()
#         if len(cps_info_qset):
#             for cps_info_instance in cps_info_qset:
#                 secondary_guardian_qset_for_this_cps_info = cps_info_instance.picconsumer_set.all()
#
#                 if secondary_guardian_qset is not None:
#                     secondary_guardian_qset = secondary_guardian_qset | secondary_guardian_qset_for_this_cps_info
#                 else:
#                     secondary_guardian_qset = secondary_guardian_qset_for_this_cps_info
#
#         return secondary_guardian_qset
#
#     def return_values_dict(self):
#         valuesdict = {"First Name": self.first_name,
#                       "Middle Name": self.middle_name,
#                       "Last Name": self.last_name,
#                       "Email": self.email,
#                       "Phone Number": self.phone,
#                       "Preferred Language": self.preferred_language,
#                       "address": None,
#                       "Household Size": self.household_size,
#                       "Plan": self.plan,
#                       "Met Navigator At": self.met_nav_at,
#                       "Best Contact Time": self.best_contact_time,
#                       "Navigator": None,
#                       "Navigator Notes": None,
#                       "date_met_nav": None,
#                       "cps_consumer": self.cps_consumer,
#                       "cps_info": None,
#                       "primary_guardians": None,
#                       "secondary_guardians": None,
#                       "consumer_hospital_info": None,
#
#                       "Database ID": self.id}
#
#         if self.date_met_nav:
#             valuesdict["date_met_nav"] = self.date_met_nav.isoformat()
#
#         if self.consumernote_set:
#             navigator_note_objects = self.consumernote_set.all()
#             navigator_note_list = []
#
#             if len(navigator_note_objects):
#                 for navigator_note in navigator_note_objects:
#                     navigator_note_list.append(navigator_note.navigator_notes)
#
#             valuesdict["Navigator Notes"] = navigator_note_list
#
#         if self.address:
#             valuesdict["address"] = {}
#             address_values = self.address.return_values_dict()
#             for key in address_values:
#                 valuesdict["address"][key] = address_values[key]
#
#         if self.navigator:
#             valuesdict['Navigator'] = "{!s} {!s}".format(self.navigator.first_name, self.navigator.last_name)
#
#         if self.cps_info:
#             valuesdict['cps_info'] = self.cps_info.return_values_dict()
#
#         if self.consumer_hospital_info:
#             valuesdict['consumer_hospital_info'] = self.consumer_hospital_info.return_values_dict()
#
#         # if self.primary_guardian:
#         #     primary_guardian_info = []
#         #
#         #     primary_guardian_qset = self.get_primary_guardian_qset()
#         #     if primary_guardian_qset is not None:
#         #         if len(primary_guardian_qset):
#         #             for primary_guardian_instance in primary_guardian_qset:
#         #                 primary_guardian_info.append(primary_guardian_instance.id)
#         #
#         #     if primary_guardian_info:
#         #         valuesdict["primary_guardians"] = primary_guardian_info
#         #
#         # if self.secondary_guardians:
#         #     secondary_guardian_info = []
#         #
#         #     secondary_guardian_qset = self.get_secondary_guardian_qset()
#         #     if secondary_guardian_qset is not None:
#         #         if len(secondary_guardian_qset):
#         #             for secondary_guardian_instance in secondary_guardian_qset:
#         #                 secondary_guardian_info.append(secondary_guardian_instance.id)
#         #
#         #     if secondary_guardian_info:
#         #         valuesdict["secondary_guardians"] = secondary_guardian_info
#
#         return valuesdict
#
#     def delete(self, *args, **kwargs):
#         if self.cps_info:
#             self.cps_info.delete()
#         super(PICConsumerBase, self).delete(*args, **kwargs)
#
#
# class PICConsumer(PICConsumerBase):
#
#     class Meta(PICConsumerBase.Meta):
#         unique_together = ()
#
#
# class PICConsumerBackup(PICConsumerBase):
#     pass
#
#
# class ConsumerNote(models.Model):
#     consumer = models.ForeignKey(PICConsumer, on_delete=models.CASCADE, blank=True, null=True)
#     consumer_backup = models.ForeignKey(PICConsumerBackup, on_delete=models.CASCADE, blank=True, null=True)
#     navigator_notes = models.TextField(blank=True, default="")
#
#     class Meta:
#         # maps model to the picmodels module
#         app_label = 'picmodels'
#
#
# class ConsumerCPSInfoEntry(models.Model):
#     """
#     Need to validate ALL form data before creating PICConsumer entries and by extention, ConsumerCPSInfoEntry
#     """
#
#     N_A = "Not Available"
#     OPEN = "Open"
#     RESOLVED = "Resloved"
#     CASE_MGMT_STATUS_CHOICES = ((OPEN, "Open"),
#                                 (RESOLVED, "Resolved"),
#                                 (N_A, "Not Available"))
#
#     MEDICAID = "Medicaid"
#     SNAP = "SNAP"
#     MEDICAID_SNAP = "Medicaid/SNAP"
#     REDETERMINATION = "Redetermination"
#     PLAN_SELECTION = "Plan Selection"
#     FAX_FCRC = "Fax FCRC"
#     EDUCATION = "Education"
#     MMCO = "MMCO"
#     APP_TYPE_CHOICES = ((MEDICAID, "Medicaid"),
#                         (SNAP, "SNAP"),
#                         (MEDICAID_SNAP, "Medicaid/SNAP"),
#                         (REDETERMINATION, "Redetermination"),
#                         (PLAN_SELECTION, "Plan Selection"),
#                         (FAX_FCRC, "Fax FCRC"),
#                         (EDUCATION, "Education"),
#                         (MMCO, "MMCO"),
#                         (N_A, "Not Available"))
#
#     SUBMITTED = "Submitted"
#     PENDING = "Pending"
#     APPROVED = "Approved"
#     DENIED = "Denied"
#     APP_STATUS_CHOICES = ((SUBMITTED, "Submitted"),
#                           (PENDING, "Pending"),
#                           (APPROVED, "Approved"),
#                           (DENIED, "Denied"),
#                           (N_A, "Not Available"))
#
#     WALK_IN = "Walk-in"
#     APPOINTMENT = "Appointment"
#     REFERRAL_FROM_CALL = "Referral from call"
#     REFERRAL_FROM_SCHOOL_LETTER = "Referral from school letter"
#     ENROLLMENT_EVENT = "Enrollment event"
#     POINT_OF_ORIGIN_CHOICES = (
#         (WALK_IN, "Walk-in"),
#         (APPOINTMENT, "Appointment"),
#         (REFERRAL_FROM_CALL, "Referral from call"),
#         (REFERRAL_FROM_SCHOOL_LETTER, "Referral from school letter"),
#         (ENROLLMENT_EVENT, "Enrollment event"),
#         (N_A, "Not Available")
#     )
#
#     primary_dependent = models.ForeignKey(PICConsumer, on_delete=models.SET_NULL, blank=True, null=True, related_name='primary_guardian')
#     secondary_dependents = models.ManyToManyField(PICConsumer, blank=True, related_name='secondary_guardians')
#
#     cps_location = models.ForeignKey(NavMetricsLocation, blank=True, null=True)
#
#     apt_date = models.DateField(blank=True, null=True)
#     target_list = models.BooleanField(default=False)
#     phone_apt = models.BooleanField(default=False)
#     case_mgmt_type = models.CharField(max_length=1000, blank=True, null=True)
#     case_mgmt_status = models.CharField(max_length=1000, blank=True, null=True, choices=CASE_MGMT_STATUS_CHOICES, default=N_A)
#     app_type = models.CharField(max_length=1000, blank=True, null=True, choices=APP_TYPE_CHOICES, default=N_A)
#     app_status = models.CharField(max_length=1000, blank=True, null=True, choices=APP_STATUS_CHOICES, default=N_A)
#     point_of_origin = models.CharField(max_length=1000, blank=True, null=True, choices=POINT_OF_ORIGIN_CHOICES, default=N_A)
#
#     class Meta:
#         # maps model to the picmodels module
#         app_label = 'picmodels'
#
#     def check_case_mgmt_status_choices(self,):
#         for plan_tuple in self.CASE_MGMT_STATUS_CHOICES:
#             if plan_tuple[1].lower() == self.case_mgmt_status.lower():
#                 return True
#         return False
#
#     def check_app_type_choices(self,):
#         for plan_tuple in self.APP_TYPE_CHOICES:
#             if plan_tuple[1].lower() == self.app_type.lower():
#                 return True
#         return False
#
#     def check_app_status_choices(self,):
#         for plan_tuple in self.APP_STATUS_CHOICES:
#             if plan_tuple[1].lower() == self.app_status.lower():
#                 return True
#         return False
#
#     def check_point_of_origin_choices(self,):
#         for point_of_origin_tuple in self.POINT_OF_ORIGIN_CHOICES:
#             if point_of_origin_tuple[1].lower() == self.point_of_origin.lower():
#                 return True
#         return False
#
#     def return_values_dict(self):
#         valuesdict = {"apt_date": None,
#                       "target_list": self.target_list,
#                       "phone_apt": self.phone_apt,
#                       "case_mgmt_type": self.case_mgmt_type,
#                       "case_mgmt_status": self.case_mgmt_status,
#                       "app_type": self.app_type,
#                       "app_status": self.app_status,
#                       "point_of_origin": self.point_of_origin,
#                       "cps_location": None,
#                       "primary_dependent": None,
#                       "secondary_dependents": None,
#                       "Database ID": self.id}
#
#         if self.apt_date:
#             valuesdict["apt_date"] = self.apt_date.isoformat()
#
#         if self.cps_location:
#             valuesdict["cps_location"] = self.cps_location.name
#
#         if self.primary_dependent:
#             primary_dependent_entry = {"first_name": self.primary_dependent.first_name,
#                                        "last_name": self.primary_dependent.last_name,
#                                        "Database ID": self.primary_dependent.id}
#             valuesdict["primary_dependent"] = primary_dependent_entry
#
#         if self.secondary_dependents:
#             secondary_dependent_queryset = self.secondary_dependents.all()
#             if len(secondary_dependent_queryset):
#                 secondary_dependent_list = []
#                 for secondary_dependent in secondary_dependent_queryset:
#                     dependent_entry = {"first_name": secondary_dependent.first_name,
#                                        "last_name": secondary_dependent.last_name,
#                                        "Database ID": secondary_dependent.id}
#                     secondary_dependent_list.append(dependent_entry)
#                 valuesdict["secondary_dependents"] = secondary_dependent_list
#
#         return valuesdict
#
#
# class ConsumerHospitalInfo(models.Model):
#     """
#     Need to validate ALL field/column data before creating PICConsumerBase entries/rows and by extention,
#     ConsumerHospitalInfo entries/rows
#     """
#
#     N_A = "Not Available"
#     OPEN = "Open"
#     CLOSED = "Closed"
#     CASE_STATUS_CHOICES = ((OPEN, "Open"),
#                            (CLOSED, "Closed"),
#                            (N_A, "Not Available"))
#
#     treatment_site = models.CharField(max_length=1000, blank=True, null=True)
#     account_number = models.CharField(max_length=1000, blank=True, null=True)
#     mrn = models.CharField(max_length=1000, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     ssn = models.CharField(max_length=10, blank=True, null=True)
#     state = models.CharField(max_length=5, blank=True, null=True)
#     p_class = models.CharField(max_length=100, blank=True, null=True)
#     admit_date = models.DateField(blank=True, null=True)
#     discharge_date = models.DateField(blank=True, null=True)
#     medical_charges = models.FloatField(blank=True, null=True)
#     referred_date = models.DateField(blank=True, null=True)
#     no_date = models.DateField(blank=True, null=True)
#     type = models.CharField(max_length=1000, blank=True, null=True)
#     no_reason = models.CharField(max_length=1000, blank=True, null=True)
#
#     case_status = models.CharField(max_length=1000, blank=True, null=True, choices=CASE_STATUS_CHOICES, default=N_A)
#
#     class Meta:
#         # maps model to the picmodels module
#         app_label = 'picmodels'
#
#     def check_case_status_choices(self,):
#         for case_status_tuple in self.CASE_STATUS_CHOICES:
#             if case_status_tuple[1].lower() == self.case_status.lower():
#                 return True
#         return False
#
#     def return_values_dict(self):
#         valuesdict = {
#             "treatment_site": self.treatment_site,
#             "account_number": self.account_number,
#             "mrn": self.mrn,
#             "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
#             "ssn": self.ssn,
#             "state": self.state,
#             "p_class": self.p_class,
#             "admit_date": self.admit_date.isoformat() if self.admit_date else None,
#             "discharge_date": self.discharge_date.isoformat() if self.discharge_date else None,
#             "medical_charges": self.medical_charges,
#             "referred_date": self.referred_date.isoformat() if self.referred_date else None,
#             "no_date": self.no_date.isoformat() if self.no_date else None,
#             "type": self.type,
#             "no_reason": self.no_reason,
#             "case_status": self.case_status,
#
#             "id": self.id
#         }
#
#         return valuesdict
