from django.db import models
from django.core.validators import MaxValueValidator
import urllib

from picmodels.models.care_advisors.healthcare_provider_coverage_network_models import HealthcareCarrier

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_healthcare_plan_objs_with_given_name_county_and_carrier

from .services.read import retrieve_plan_data_by_id
from .services.read import retrieve_plan_data_by_name
from .services.read import retrieve_plan_data_by_carrier_name
from .services.read import retrieve_plan_data_by_accepted_location_id
from .services.read import retrieve_plan_data_by_carrier_state
from .services.read import retrieve_plan_data_by_carrier_id


class HealthcarePlan(models.Model):
    HMO = "HMO"
    PPO = "PPO"
    POS = 'POS'
    EPO = 'EPO'
    N_A = "Not Available"
    PREMIUM_CHOICES = ((HMO, "HMO"),
                       (PPO, "PPO"),
                       (POS, 'POS'),
                       (EPO, 'EPO'),
                       (N_A, "Not Available")
                       )

    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = 'Platinum'
    CATASTROPHIC = "Catastrophic"
    METAL_CHOICES = ((BRONZE, "Bronze"),
                     (SILVER, "Silver"),
                     (GOLD, "Gold"),
                     (PLATINUM, 'Platinum'),
                     (CATASTROPHIC, "Catastrophic"),
                     (N_A, "Not Available"))

    name = models.CharField(max_length=10000)
    carrier = models.ForeignKey(HealthcareCarrier, on_delete=models.CASCADE, blank=True, null=True)
    premium_type = models.CharField(max_length=1000, blank=True, null=True, choices=PREMIUM_CHOICES)
    metal_level = models.CharField(max_length=1000, blank=True, null=True, choices=METAL_CHOICES)
    county = models.CharField(max_length=1000, blank=True, null=True)

    # Fields included in Summary Report
    medical_deductible_individual_standard = models.FloatField(blank=True, null=True)
    medical_out_of_pocket_max_individual_standard = models.FloatField(blank=True, null=True)
    SUMMARY_REPORT_FIELDS = [
        "medical_deductible_individual_standard",
        "medical_out_of_pocket_max_individual_standard",
        "primary_care_physician_standard_cost"
    ]

    # Fields included in Detailed Report
    DETAILED_REPORT_FIELDS = [
        "specialist_standard_cost",
        "emergency_room_standard_cost",
        "inpatient_facility_standard_cost",
        "generic_drugs_standard_cost",
        "preferred_brand_drugs_standard_cost",
        "non_preferred_brand_drugs_standard_cost",
        "specialty_drugs_standard_cost"
    ]

    # Extra benefit report fields
    medical_deductible_family_standard = models.FloatField(blank=True, null=True)
    medical_out_of_pocket_max_family_standard = models.FloatField(blank=True, null=True)
    EXTRA_REPORT_FIELDS = [
        "medical_deductible_family_standard",
        "medical_out_of_pocket_max_family_standard",
    ]

    def check_metal_choices(self,):
        if self.metal_level:
            for metal_tuple in self.METAL_CHOICES:
                if metal_tuple[1].lower() == self.metal_level.lower():
                    return True
            return False
        else:
            return True

    def check_premium_choices(self,):
        if self.premium_type:
            for premium_tuple in self.PREMIUM_CHOICES:
                if premium_tuple[1].lower() == self.premium_type.lower():
                    return True
            return False
        else:
            return True

    def return_values_dict(self, include_summary_report=False, include_detailed_report=False):
        valuesdict = {
            "name": self.name,
            "url_encoded_name": urllib.parse.quote(self.name) if self.name else None,
            "premium_type": self.premium_type,
            "metal_level": self.metal_level,
            "county": self.county,
            "carrier_info": None,
            "Database ID": self.id
        }

        def add_report_fields_to_values_dict(report_fields):
            def compose_cost_string_from_related_cost_row(healthcare_service_cost_entry_instance):
                entry_string = ""

                if healthcare_service_cost_entry_instance.coinsurance:
                    entry_string = "{}% coinsurance".format(healthcare_service_cost_entry_instance.coinsurance)
                if healthcare_service_cost_entry_instance.copay:
                    if entry_string != "":
                        entry_string += " and "
                    entry_string += "${} copay".format(healthcare_service_cost_entry_instance.copay)
                if entry_string == "" or entry_string == "0% coinsurance and $0 copay":
                    entry_string = "No charge"
                if healthcare_service_cost_entry_instance.cost_relation_to_deductible:
                    entry_string += " {} deductible".format(
                        healthcare_service_cost_entry_instance.cost_relation_to_deductible.lower())

                return entry_string

            report_fields_with_values = {}
            for report_field in report_fields:
                # try:
                    ## .order_by() adds significant overhead unless field to be ordered by has been indexed in some way
                #     report_fields_with_values[report_field] = getattr(self, report_field).all().order_by(
                #         '-cost_relation_to_deductible')
                # except AttributeError:
                #     report_fields_with_values[report_field] = getattr(self, report_field)

                report_value = getattr(self, report_field)
                if isinstance(report_value, float):
                    report_fields_with_values[report_field] = report_value
                else:
                    report_fields_with_values[report_field] = report_value.all()
                    # .order_by() adds significant overhead unless field to be ordered by has been indexed in some way
                    # report_fields_with_values[report_field] = report_value.all().order_by('-cost_relation_to_deductible')

            instance_has_all_report_fields = all(report_field_value for report_field_value in report_fields_with_values.values())
            if instance_has_all_report_fields:
                # Convert all summary report fields to values that are json serializable and add to valuesdict
                for key, healthcare_service_cost_qset in report_fields_with_values.items():
                    if isinstance(healthcare_service_cost_qset, models.QuerySet):
                        values_dict_string = ""
                        if len(healthcare_service_cost_qset):
                            for healthcare_service_cost_entry in healthcare_service_cost_qset:
                                if values_dict_string != "":
                                    values_dict_string += " and "
                                values_dict_string += compose_cost_string_from_related_cost_row(healthcare_service_cost_entry)
                        if values_dict_string == "":
                            values_dict_string = None

                        report_fields_with_values[key] = values_dict_string

                return report_fields_with_values
            else:
                return None

        def add_summary_report_fields_to_values_dict():
            valuesdict["summary_report"] = add_report_fields_to_values_dict(self.SUMMARY_REPORT_FIELDS)
        if include_summary_report:
            valuesdict["summary_report"] = None
            add_summary_report_fields_to_values_dict()

        def add_detailed_report_fields_to_values_dict():
            valuesdict["detailed_report"] = add_report_fields_to_values_dict(self.DETAILED_REPORT_FIELDS)
        if include_detailed_report:
            valuesdict["detailed_report"] = None
            add_detailed_report_fields_to_values_dict()

        def add_carrier_info_to_values_dict():
            if self.carrier:
                carrier_info = {
                    "name": self.carrier.name,
                    "state": self.carrier.state_province,
                    "Database ID": self.carrier.id
                }
                valuesdict['carrier_info'] = carrier_info
        add_carrier_info_to_values_dict()

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


HealthcarePlan.create_row_w_validated_params = classmethod(create_row_w_validated_params)
HealthcarePlan.update_row_w_validated_params = classmethod(update_row_w_validated_params)
HealthcarePlan.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)
HealthcarePlan.check_for_healthcare_plan_objs_with_given_name_county_and_carrier = classmethod(check_for_healthcare_plan_objs_with_given_name_county_and_carrier)


HealthcarePlan.retrieve_plan_data_by_id = classmethod(retrieve_plan_data_by_id)
HealthcarePlan.retrieve_plan_data_by_name = classmethod(retrieve_plan_data_by_name)
HealthcarePlan.retrieve_plan_data_by_carrier_name = classmethod(retrieve_plan_data_by_carrier_name)
HealthcarePlan.retrieve_plan_data_by_accepted_location_id = classmethod(retrieve_plan_data_by_accepted_location_id)
HealthcarePlan.retrieve_plan_data_by_carrier_state = classmethod(retrieve_plan_data_by_carrier_state)
HealthcarePlan.retrieve_plan_data_by_carrier_id = classmethod(retrieve_plan_data_by_carrier_id)


class HealthcareServiceCostEntry(models.Model):
    BEFORE = "Before"
    AFTER = "After"
    RELATIVE_TO_DEDUCTIBLE_CHOICES = ((BEFORE, "Before"),
                                      (AFTER, "After"),
                                      )

    cost_relation_to_deductible = models.CharField(max_length=100, blank=True, null=True, choices=RELATIVE_TO_DEDUCTIBLE_CHOICES)
    coinsurance = models.FloatField(blank=True, null=True, validators=[MaxValueValidator(100), ])
    copay = models.FloatField(blank=True, null=True)

    # Fields included in Summary Report
    plan_obj_for_primary_care_physician_standard_cost = models.ForeignKey(HealthcarePlan, on_delete=models.CASCADE, blank=True, null=True, related_name='primary_care_physician_standard_cost')

    # Fields included in Detailed Report
    plan_obj_for_specialist_standard_cost = models.ForeignKey(HealthcarePlan, on_delete=models.CASCADE, blank=True, null=True, related_name='specialist_standard_cost')
    plan_obj_for_emergency_room_standard_cost = models.ForeignKey(HealthcarePlan, on_delete=models.CASCADE, blank=True, null=True, related_name='emergency_room_standard_cost')
    plan_obj_for_inpatient_facility_standard_cost = models.ForeignKey(HealthcarePlan, on_delete=models.CASCADE, blank=True, null=True, related_name='inpatient_facility_standard_cost')
    plan_obj_for_generic_drugs_standard_cost = models.ForeignKey(HealthcarePlan, on_delete=models.CASCADE, blank=True, null=True, related_name='generic_drugs_standard_cost')
    plan_obj_for_preferred_brand_drugs_standard_cost = models.ForeignKey(HealthcarePlan, on_delete=models.CASCADE, blank=True, null=True, related_name='preferred_brand_drugs_standard_cost')
    plan_obj_for_non_preferred_brand_drugs_standard_cost = models.ForeignKey(HealthcarePlan, on_delete=models.CASCADE, blank=True, null=True, related_name='non_preferred_brand_drugs_standard_cost')
    plan_obj_for_specialty_drugs_standard_cost = models.ForeignKey(HealthcarePlan, on_delete=models.CASCADE, blank=True, null=True, related_name='specialty_drugs_standard_cost')

    def check_relative_to_deductible_choices(self,):
        if self.cost_relation_to_deductible:
            for relative_to_deductible_tuple in self.RELATIVE_TO_DEDUCTIBLE_CHOICES:
                if relative_to_deductible_tuple[1].lower() == self.cost_relation_to_deductible.lower():
                    return True
            return False
        else:
            return True

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
