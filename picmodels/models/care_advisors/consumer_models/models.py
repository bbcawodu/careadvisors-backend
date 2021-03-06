from django.db import models
from django.core.validators import MinValueValidator

from decimal import Decimal

from picmodels.models.care_advisors.navigator_models import Navigators
from picmodels.models.care_advisors import NavMetricsLocation, Address

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import create_c_m_rows_w_validated_params
from .services.create_update_delete import update_c_m_rows_w_validated_params
from .services.create_update_delete import delete_c_m_rows_w_validated_params

from .services.read import get_serialized_rows_by_id
from .services.read import get_serialized_rows_by_f_and_l_name
from .services.read import get_serialized_rows_by_email
from .services.read import get_serialized_rows_by_first_name
from .services.read import get_serialized_rows_by_last_name


class PICConsumerBaseQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            if obj.cps_info:
                obj.cps_info.delete()
            if obj.consumerhospitaldata_set:
                hospital_data_objs = obj.consumerhospitaldata_set.all()
                if len(hospital_data_objs):
                    for hospital_obj in hospital_data_objs:
                        hospital_obj.delete()
        super(PICConsumerBaseQuerySet, self).delete(*args, **kwargs)


class PICConsumerBase(models.Model):
    N_A = "Not Available"
    CHOOSE_A_DOC = "choose a doctor"
    BILLING_ISSUES = "billing issues"
    CONSUMER_NEED_CHOICES = (
        (CHOOSE_A_DOC, "choose a doctor"),
        (BILLING_ISSUES, "billing issues"),
        (N_A, "Not Available")
    )

    MALE = "Male"
    FEMALE = "Female"
    TRANSGENDER = "Transgender"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (TRANSGENDER, "Transgender"),
        (N_A, "Not Available")
    )

    PHONE = "Phone"
    EMAIL = "Email"
    DATA = "Data"
    REFERRAL_CHANNEL_CHOICES = (
        (PHONE, "Phone"),
        (EMAIL, "Email"),
        (DATA, "Data"),
        (N_A, "Not Available")
    )

    objects = PICConsumerBaseQuerySet.as_manager()

    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    datetime_received_by_client = models.DateTimeField(blank=True, null=True)

    # fields for PICConsumer model
    first_name = models.CharField(max_length=1000)
    middle_name = models.CharField(max_length=1000, blank=True, null=True)
    last_name = models.CharField(default="", max_length=1000)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=1000, blank=True, null=True)
    preferred_language = models.CharField(max_length=1000, blank=True, null=True)
    best_contact_time = models.CharField(max_length=1000, blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=1000, choices=GENDER_CHOICES, default=N_A)
    dob = models.DateField(blank=True, null=True)
    referral_channel = models.CharField(blank=True, null=True, max_length=1000, choices=REFERRAL_CHANNEL_CHOICES, default=N_A)
    navigator = models.ForeignKey(Navigators, on_delete=models.SET_NULL, blank=True, null=True)
    # navigators = models.ManyToManyField(Navigators, blank=True)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    household_size = models.IntegerField()
    plan = models.CharField(max_length=1000, blank=True, null=True)
    met_nav_at = models.CharField(max_length=1000)
    date_met_nav = models.DateField(blank=True, null=True)

    cps_info = models.ForeignKey('ConsumerCPSInfoEntry', on_delete=models.SET_NULL, blank=True, null=True)

    # Individual Seeking Navigator fields/columns
    consumer_need = models.CharField(blank=True, null=True, max_length=1000, choices=CONSUMER_NEED_CHOICES, default=N_A)
    billing_amount = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=14,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    service_expertise_need = models.ForeignKey(
        'HealthcareServiceExpertise',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    insurance_carrier = models.ForeignKey(
        'HealthcareCarrier',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    healthcare_locations_used = models.ManyToManyField(
        'ProviderLocation',
        blank=True,
    )

    def delete(self, *args, **kwargs):
        if self.cps_info:
            self.cps_info.delete()
        super(PICConsumerBase, self).delete(*args, **kwargs)

    def __str__(self):
        return "Name: {} {}, id: {}".format(self.first_name, self.last_name, self.id)

    def check_consumer_need_choices(self,):
        for consumer_need_tuple in self.CONSUMER_NEED_CHOICES:
            if consumer_need_tuple[1].lower() == self.consumer_need.lower():
                return True
        return False

    def check_gender_choices(self,):
        for gender_tuple in self.GENDER_CHOICES:
            if gender_tuple[1].lower() == self.gender.lower():
                return True
        return False

    def check_referral_channel_choices(self,):
        for referral_channel_tuple in self.REFERRAL_CHANNEL_CHOICES:
            if referral_channel_tuple[1].lower() == self.referral_channel.lower():
                return True
        return False

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
        abstract = True


PICConsumerBase.get_serialized_rows_by_id = classmethod(get_serialized_rows_by_id)
PICConsumerBase.get_serialized_rows_by_f_and_l_name = classmethod(get_serialized_rows_by_f_and_l_name)
PICConsumerBase.get_serialized_rows_by_email = classmethod(get_serialized_rows_by_email)
PICConsumerBase.get_serialized_rows_by_first_name = classmethod(get_serialized_rows_by_first_name)
PICConsumerBase.get_serialized_rows_by_last_name = classmethod(get_serialized_rows_by_last_name)


class PICConsumer(PICConsumerBase):
    cm_client_for_routing = models.ForeignKey('CaseManagementClient', related_name='consumers_for_routing',
                                              on_delete=models.SET_NULL, blank=True, null=True)
    referring_cm_clients = models.ManyToManyField(
        'CaseManagementClient',
        related_name='referred_consumers_for_cm',
        blank=True,
    )
    referral_type = models.ForeignKey(
        'HealthcareServiceExpertise',
        related_name='consumers_referred_by_this_type',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta(PICConsumerBase.Meta):
        unique_together = ()

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
        valuesdict = {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "preferred_language": self.preferred_language,
            "gender": self.gender,
            "dob": self.dob.isoformat() if self.dob else None,
            "address": None,
            "household_size": self.household_size,
            "plan": self.plan,
            "met_nav_at": self.met_nav_at,
            "best_contact_time": self.best_contact_time,
            "referral_channel": self.referral_channel,
            "referral_type": None,
            "navigator": None,
            "cm_client_for_routing": None,
            "referring_cm_clients": None,
            "consumer_notes": None,
            "date_met_nav": None,
            "cps_info": None,
            "primary_guardians": None,
            "secondary_guardians": None,
            "consumer_hospital_data": None,
            "consumer_payer_data": None,

            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,
            "datetime_received_by_client": self.datetime_received_by_client.isoformat() if self.datetime_received_by_client else None,

            "case_management_rows": None,

            "consumer_need": self.consumer_need,
            "billing_amount": float(self.billing_amount) if self.billing_amount else self.billing_amount,
            "service_expertise_need": None,
            "insurance_carrier": None,
            "healthcare_locations_used": None,

            "id": self.id
        }

        if self.date_met_nav:
            valuesdict["date_met_nav"] = self.date_met_nav.isoformat()

        if self.consumernote_set:
            navigator_note_objects = self.consumernote_set.all()
            navigator_note_list = []

            if len(navigator_note_objects):
                for navigator_note in navigator_note_objects:
                    navigator_note_list.append(navigator_note.navigator_notes)

            valuesdict["consumer_notes"] = navigator_note_list

        if self.casemanagementstatus_set:
            case_objects = self.casemanagementstatus_set.all()
            # .order_by() adds significant overhead unless field to be ordered by has been indexed in some way
            # case_objects = self.casemanagementstatus_set.all().order_by("-date_modified")
            # case_objects = self.casemanagementstatus_set.all().order_by("management_step")

            case_list = []

            if len(case_objects):
                for case_note in case_objects:
                    case_list.append(case_note.return_values_dict())

            valuesdict["case_management_rows"] = case_list

        if self.address:
            valuesdict["address"] = {}
            address_values = self.address.return_values_dict()
            for key in address_values:
                valuesdict["address"][key] = address_values[key]

        if self.navigator:
            valuesdict['navigator'] = self.navigator.id

        if self.referral_type:
            valuesdict['referral_type'] = self.referral_type.name

        if self.cm_client_for_routing:
            valuesdict['cm_client_for_routing'] = self.cm_client_for_routing.id

        referring_cm_clients = self.referring_cm_clients.all()
        if len(referring_cm_clients):
            cm_client_values = []
            for cm_client in referring_cm_clients:
                cm_client_values.append(cm_client.id)
            valuesdict["referring_cm_clients"] = cm_client_values

        if self.cps_info:
            valuesdict['cps_info'] = self.cps_info.return_values_dict()

        if self.consumerhospitaldata_set:
            consumer_hospital_data_objects = self.consumerhospitaldata_set.all()
            consumer_hospital_data_list = []

            if len(consumer_hospital_data_objects):
                for consumer_hospital_data in consumer_hospital_data_objects:
                    consumer_hospital_data_list.append(consumer_hospital_data.return_values_dict())

            valuesdict["consumer_hospital_data"] = consumer_hospital_data_list

        if self.consumerpayerdata_set:
            consumer_payer_data_objects = self.consumerpayerdata_set.all()
            consumer_payer_data_list = []

            if len(consumer_payer_data_objects):
                for consumer_payer_data in consumer_payer_data_objects:
                    consumer_payer_data_list.append(consumer_payer_data.return_values_dict())

            valuesdict["consumer_payer_data"] = consumer_payer_data_list

        if self.service_expertise_need:
            valuesdict['service_expertise_need'] = self.service_expertise_need.return_values_dict()

        if self.insurance_carrier:
            valuesdict['insurance_carrier'] = self.insurance_carrier.return_values_dict()

        if self.healthcare_locations_used:
            healthcare_locations_used_objects = self.healthcare_locations_used.all()
            healthcare_locations_used_list = []

            if len(healthcare_locations_used_objects):
                for healthcare_location_used in healthcare_locations_used_objects:
                    healthcare_locations_used_list.append(healthcare_location_used.return_values_dict())

            valuesdict["healthcare_locations_used"] = healthcare_locations_used_list

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


PICConsumer.create_row_w_validated_params = classmethod(create_row_w_validated_params)
PICConsumer.update_row_w_validated_params = classmethod(update_row_w_validated_params)
PICConsumer.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)


class PICConsumerBackup(PICConsumerBase):
    cm_client_for_routing = models.ForeignKey('CaseManagementClient', related_name='consumer_backups_for_routing',
                                              on_delete=models.SET_NULL, blank=True, null=True)
    referring_cm_clients = models.ManyToManyField(
        'CaseManagementClient',
        related_name='referred_consumer_backups_for_cm',
        blank=True,
    )
    referral_type = models.ForeignKey(
        'HealthcareServiceExpertise',
        related_name='backup_consumers_referred_by_this_type',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

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
        valuesdict = {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "preferred_language": self.preferred_language,
            "gender": self.gender,
            "dob": self.dob.isoformat() if self.dob else None,
            "address": None,
            "household_size": self.household_size,
            "plan": self.plan,
            "met_nav_at": self.met_nav_at,
            "best_contact_time": self.best_contact_time,
            "referral_channel": self.referral_channel,
            'referral_type': None,
            "navigator": None,
            "consumer_notes": None,
            "date_met_nav": None,
            "cps_info": None,
            "primary_guardians": None,
            "secondary_guardians": None,
            "consumer_hospital_data": None,
            "consumer_payer_data": None,

            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,
            "datetime_received_by_client": self.datetime_received_by_client.isoformat() if self.datetime_received_by_client else None,

            "case_management_rows": None,

            "consumer_need": self.consumer_need,
            "billing_amount": float(self.billing_amount) if self.billing_amount else self.billing_amount,
            "service_expertise_need": None,
            "insurance_carrier": None,
            "healthcare_locations_used": None,

            "id": self.id
        }

        if self.date_met_nav:
            valuesdict["date_met_nav"] = self.date_met_nav.isoformat()

        if self.consumernote_set:
            navigator_note_objects = self.consumernote_set.all()
            navigator_note_list = []

            if len(navigator_note_objects):
                for navigator_note in navigator_note_objects:
                    navigator_note_list.append(navigator_note.navigator_notes)

            valuesdict["consumer_notes"] = navigator_note_list

        if self.casemanagementstatus_set:
            case_objects = self.casemanagementstatus_set.all()
            # .order_by() adds significant overhead unless field to be ordered by has been indexed in some way
            # case_objects = self.casemanagementstatus_set.all().order_by("-date_modified")
            # case_objects = self.casemanagementstatus_set.all().order_by("management_step")

            case_list = []

            if len(case_objects):
                for case_note in case_objects:
                    case_list.append(case_note.return_values_dict())

            valuesdict["case_management_rows"] = case_list

        if self.address:
            valuesdict["address"] = {}
            address_values = self.address.return_values_dict()
            for key in address_values:
                valuesdict["address"][key] = address_values[key]

        if self.navigator:
            valuesdict['navigator'] = self.navigator.id

        if self.referral_type:
            valuesdict['referral_type'] = self.referral_type.name

        if self.cps_info:
            valuesdict['cps_info'] = self.cps_info.return_values_dict()

        if self.consumerhospitaldata_set:
            consumer_hospital_data_objects = self.consumerhospitaldata_set.all()
            consumer_hospital_data_list = []

            if len(consumer_hospital_data_objects):
                for consumer_hospital_data in consumer_hospital_data_objects:
                    consumer_hospital_data_list.append(consumer_hospital_data.return_values_dict())

            valuesdict["consumer_hospital_data"] = consumer_hospital_data_list

        if self.consumerpayerdata_set:
            consumer_payer_data_objects = self.consumerpayerdata_set.all()
            consumer_payer_data_list = []

            if len(consumer_payer_data_objects):
                for consumer_payer_data in consumer_payer_data_objects:
                    consumer_payer_data_list.append(consumer_payer_data.return_values_dict())

            valuesdict["consumer_payer_data"] = consumer_payer_data_list

        if self.service_expertise_need:
            valuesdict['service_expertise_need'] = self.service_expertise_need.return_values_dict()

        if self.insurance_carrier:
            valuesdict['insurance_carrier'] = self.insurance_carrier.return_values_dict()

        if self.healthcare_locations_used:
            healthcare_locations_used_objects = self.healthcare_locations_used.all()
            healthcare_locations_used_list = []

            if len(healthcare_locations_used_objects):
                for healthcare_location_used in healthcare_locations_used_objects:
                    healthcare_locations_used_list.append(healthcare_location_used.return_values_dict())

            valuesdict["healthcare_locations_used"] = healthcare_locations_used_list

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


class ConsumerNote(models.Model):
    consumer = models.ForeignKey(PICConsumer, on_delete=models.CASCADE, blank=True, null=True)
    consumer_backup = models.ForeignKey(PICConsumerBackup, on_delete=models.CASCADE, blank=True, null=True)
    navigator_notes = models.TextField(blank=True, default="")

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class ConsumerHospitalData(models.Model):
    medical_record_number = models.CharField(max_length=5000, blank=True, null=True)
    discharge_date = models.DateField(blank=True, null=True)
    billing_amount = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=14,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    hospital_name = models.CharField(max_length=5000, blank=True, null=True)

    consumer = models.ForeignKey(
        'PICConsumer',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    consumer_backup = models.ForeignKey(
        'PICConsumerBackup',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

    def return_values_dict(self):
        valuesdict = {
            "medical_record_number": self.medical_record_number,
            "discharge_date": self.discharge_date.isoformat() if self.discharge_date else None,
            "billing_amount": float(self.billing_amount) if self.billing_amount else self.billing_amount,

            'hospital_name': self.hospital_name,

            "id": self.id
        }

        return valuesdict


class ConsumerPayerData(models.Model):
    N_A = "Not Available"
    PRIVATE = "Private"
    ACA = "ACA"
    FHP = "FHP"
    MEDICARE = "Medicare"
    DUAL_ELIGIBLE = "Dual Eligible"
    COVERAGE_TYPE_CHOICES = (
        (PRIVATE, "Private"),
        (ACA, "ACA"),
        (FHP, "FHP"),
        (MEDICARE, "Medicare"),
        (DUAL_ELIGIBLE, "Dual Eligible"),
        (N_A, "Not Available")
    )

    member_id_number = models.CharField(max_length=5000, blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    risk = models.CharField(max_length=5000, blank=True, null=True)
    coverage_type = models.CharField(
        blank=True,
        null=True,
        max_length=1000,
        choices=COVERAGE_TYPE_CHOICES,
        default=N_A
    )
    case_type = models.ForeignKey(
        'CMSequences',
        related_name='payer_data_for_cases_of_this_type',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    consumer = models.ForeignKey(
        'PICConsumer',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    consumer_backup = models.ForeignKey(
        'PICConsumerBackup',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def check_coverage_type_choices(self,):
        for coverage_type_tuple in self.COVERAGE_TYPE_CHOICES:
            if coverage_type_tuple[1].lower() == self.coverage_type.lower():
                return True
        return False

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

    def return_values_dict(self):
        valuesdict = {
            "member_id_number": self.member_id_number,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "risk": self.risk,
            "coverage_type": self.coverage_type,
            'case_type': self.case_type.name if self.case_type else None,

            "id": self.id
        }

        return valuesdict


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


class CaseManagementStatus(models.Model):
    """
    Need to validate ALL field/column data before creating PICConsumerBase entries/rows and by extention,
    CaseManagementStatus entries/rows
    """

    contact = models.ForeignKey('PICConsumer', on_delete=models.CASCADE, blank=True, null=True)
    contact_backup = models.ForeignKey('PICConsumerBackup', on_delete=models.CASCADE, blank=True, null=True)

    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)

    management_step = models.IntegerField()
    management_notes = models.TextField(blank=True, null=True)

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'

    def return_values_dict(self):
        valuesdict = {
            "management_step": self.management_step,
            "management_notes": self.management_notes,
            "date_created": self.date_created.isoformat() if self.date_created else None,
            "date_modified": self.date_modified.isoformat() if self.date_modified else None,

            "id": self.id
        }

        return valuesdict


CaseManagementStatus.create_c_m_rows_w_validated_params = classmethod(create_c_m_rows_w_validated_params)
CaseManagementStatus.update_c_m_rows_w_validated_params = classmethod(update_c_m_rows_w_validated_params)
CaseManagementStatus.delete_c_m_rows_w_validated_params = classmethod(delete_c_m_rows_w_validated_params)
