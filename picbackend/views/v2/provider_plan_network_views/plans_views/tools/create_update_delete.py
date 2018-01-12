"""
This module defines utility functions and classes for views that handle accepted plans for provider networks contracted
with PIC
"""

import re

from picbackend.views.utils import clean_float_value_from_dict_object
from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picmodels.models import HealthcareServiceCostEntry
from picmodels.services.provider_plan_network_services.healthcare_plan_services import \
    add_instance_using_validated_params
from picmodels.services.provider_plan_network_services.healthcare_plan_services import \
    delete_instance_using_validated_params
from picmodels.services.provider_plan_network_services.healthcare_plan_services import \
    modify_instance_using_validated_params


def validate_rqst_params_and_add_instance(rqst_plan_info, post_errors):
    add_plan_params = get_plan_mgmt_put_params(rqst_plan_info, post_errors)

    healthcare_plan = None
    if not post_errors:
        healthcare_plan = add_instance_using_validated_params(add_plan_params, post_errors)

    return healthcare_plan


def get_plan_mgmt_put_params(rqst_plan_info, post_errors):
    """
    This function parses the BODY of requests for PIC consumer management PUT requests, checks for errors, and returns
    relevant information as a dictionary

    :param rqst_carrier_info: (type: dictionary) Carrier information to be parsed
    :param post_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary with relevant consumer information
    """

    def create_healthcare_service_cost_instances_from_string(cost_string, field_name):
        healthcare_service_cost_instances = []

        if cost_string:
            cost_string = cost_string.lower()

            cost_string_list = re.split(" and ", cost_string)

            def create_healthcare_service_cost_instance_from_cost_string_fragment(cost_string_fragment):
                def get_coinsurance_percentage_from_cost_string():
                    coinsurance_percentage_return_value = None

                    coinsurance_percentage_string_list = re.findall("\d+%", cost_string_fragment)
                    no_of_coinsurance_percentages = len(coinsurance_percentage_string_list)
                    if no_of_coinsurance_percentages == 1:
                        coinsurance_percentage_numbers = re.findall("\d+", coinsurance_percentage_string_list[0])
                        no_of_coinsurance_percentage_numbers = len(coinsurance_percentage_numbers)
                        if no_of_coinsurance_percentage_numbers == 1:
                            if coinsurance_percentage_numbers[0] != "0":
                                coinsurance_percentage_return_value = float(coinsurance_percentage_numbers[0])
                            else:
                                post_errors.append("Coinsurance percentage is improperly formatted(returned 0) for field: {}".format(field_name))
                        elif no_of_coinsurance_percentage_numbers == 0 or no_of_coinsurance_percentage_numbers > 1:
                            post_errors.append("Coinsurance percentage is improperly formatted for field: {}".format(field_name))
                    elif no_of_coinsurance_percentages > 1:
                        post_errors.append("More than one coinsurance percentage is included in field: {}".format(field_name))

                    return coinsurance_percentage_return_value
                coinsurance_percentage = get_coinsurance_percentage_from_cost_string()

                def get_copay_from_cost_string():
                    copay_return_value = None

                    copay_string_list = re.findall("\$\d+", cost_string_fragment)
                    no_of_copays = len(copay_string_list)
                    if no_of_copays == 1:
                        copay_numbers = re.findall("\d+", copay_string_list[0])
                        no_of_copay_numbers = len(copay_numbers)
                        if no_of_copay_numbers == 1:
                            if copay_numbers[0] != "0":
                                copay_return_value = float(copay_numbers[0])
                            else:
                                post_errors.append("Copay cost is improperly formatted(returned 0) for field: {}".format(field_name))
                        elif no_of_copay_numbers == 0 or no_of_copay_numbers > 1:
                            post_errors.append("Copay cost is improperly formatted for field: {}".format(field_name))
                    elif no_of_copays > 1:
                        post_errors.append("More than one copay cost is included in field: {}".format(field_name))

                    return copay_return_value
                copay = get_copay_from_cost_string()

                def check_for_no_charge_in_cost_string():
                    no_charge_in_string_return_value = False

                    if re.findall("no charge", cost_string_fragment):
                        no_charge_in_string_return_value = True

                    return no_charge_in_string_return_value
                no_charge_in_cost_string = check_for_no_charge_in_cost_string()
                if no_charge_in_cost_string:
                    coinsurance_percentage = 0.0
                    copay = 0.0

                if not post_errors:
                    if coinsurance_percentage is not None or copay is not None:
                        healthcare_service_cost_instance = HealthcareServiceCostEntry(coinsurance=coinsurance_percentage,
                                                                                      copay=copay)

                        def check_for_deductible_info_in_cost_string():
                            relation_to_deductible_return_value = None

                            if re.findall("after deductible", cost_string_fragment):
                                relation_to_deductible_return_value = "After"
                            elif re.findall("before deductible", cost_string_fragment):
                                relation_to_deductible_return_value = "Before"

                            return relation_to_deductible_return_value
                        relation_to_deductible = check_for_deductible_info_in_cost_string()

                        healthcare_service_cost_instance.cost_relation_to_deductible = relation_to_deductible
                        if not healthcare_service_cost_instance.check_relative_to_deductible_choices():
                            post_errors.append("Valid cost relation to deductible was not able to be processed for field: {}".format(field_name))

                        if not post_errors:
                            healthcare_service_cost_instances.append(healthcare_service_cost_instance)
                    else:
                        post_errors.append("Valid cost was not able to be processed for field: {}".format(field_name))
            for cost_string_piece in cost_string_list:
                create_healthcare_service_cost_instance_from_cost_string_fragment(cost_string_piece)

        return healthcare_service_cost_instances

    rqst_primary_care_physician_standard_cost = create_healthcare_service_cost_instances_from_string(clean_string_value_from_dict_object(rqst_plan_info, "root", "primary_care_physician_standard_cost", post_errors, none_allowed=True, no_key_allowed=True), "primary_care_physician_individual_standard_cost")
    rqst_specialist_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(rqst_plan_info, "root", "specialist_standard_cost",
                                            post_errors, none_allowed=True, no_key_allowed=True),
        "specialist_standard_cost")
    rqst_emergency_room_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(rqst_plan_info, "root", "emergency_room_standard_cost",
                                            post_errors, none_allowed=True, no_key_allowed=True),
        "emergency_room_standard_cost")
    rqst_inpatient_facility_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(rqst_plan_info, "root", "inpatient_facility_standard_cost",
                                            post_errors, none_allowed=True, no_key_allowed=True),
        "inpatient_facility_standard_cost")
    rqst_generic_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(rqst_plan_info, "root", "generic_drugs_standard_cost",
                                            post_errors, none_allowed=True, no_key_allowed=True),
        "generic_drugs_standard_cost")
    rqst_preferred_brand_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(rqst_plan_info, "root", "preferred_brand_drugs_standard_cost",
                                            post_errors, none_allowed=True, no_key_allowed=True),
        "preferred_brand_drugs_standard_cost")
    rqst_non_preferred_brand_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(rqst_plan_info, "root", "non_preferred_brand_drugs_standard_cost",
                                            post_errors, none_allowed=True, no_key_allowed=True),
        "non_preferred_brand_drugs_standard_cost")
    rqst_specialty_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(rqst_plan_info, "root", "specialty_drugs_standard_cost",
                                            post_errors, none_allowed=True, no_key_allowed=True),
        "specialty_drugs_standard_cost")

    return {"rqst_plan_name": clean_string_value_from_dict_object(rqst_plan_info, "root", "name", post_errors),
            "rqst_carrier_id": clean_int_value_from_dict_object(rqst_plan_info, "root", "Carrier Database ID", post_errors),
            "rqst_plan_premium_type": clean_string_value_from_dict_object(rqst_plan_info, "root", "premium_type", post_errors, none_allowed=True, no_key_allowed=True),
            "rqst_plan_metal_level": clean_string_value_from_dict_object(rqst_plan_info, "root", "metal_level", post_errors, none_allowed=True, no_key_allowed=True),
            "county": clean_string_value_from_dict_object(rqst_plan_info, "root", "county", post_errors, none_allowed=True, no_key_allowed=True),

            # Summary report fields
            "medical_deductible_individual_standard": clean_float_value_from_dict_object(rqst_plan_info, "root", "medical_deductible_individual_standard", post_errors, none_allowed=True, no_key_allowed=True),
            "medical_out_of_pocket_max_individual_standard": clean_float_value_from_dict_object(rqst_plan_info, "root", "medical_out_of_pocket_max_individual_standard", post_errors, none_allowed=True, no_key_allowed=True),
            "primary_care_physician_standard_cost": rqst_primary_care_physician_standard_cost,

            # Detailed report fields
            "specialist_standard_cost": rqst_specialist_standard_cost,
            "emergency_room_standard_cost": rqst_emergency_room_standard_cost,
            "inpatient_facility_standard_cost": rqst_inpatient_facility_standard_cost,
            "generic_drugs_standard_cost": rqst_generic_drugs_standard_cost,
            "preferred_brand_drugs_standard_cost": rqst_preferred_brand_drugs_standard_cost,
            "non_preferred_brand_drugs_standard_cost": rqst_non_preferred_brand_drugs_standard_cost,
            "specialty_drugs_standard_cost": rqst_specialty_drugs_standard_cost,

            # Extra benefit report fields
            "medical_deductible_family_standard": clean_float_value_from_dict_object(rqst_plan_info, "root", "medical_deductible_family_standard", post_errors, none_allowed=True, no_key_allowed=True),
            "medical_out_of_pocket_max_family_standard": clean_float_value_from_dict_object(rqst_plan_info, "root", "medical_out_of_pocket_max_family_standard", post_errors, none_allowed=True, no_key_allowed=True),
            }


def validate_rqst_params_and_modify_instance(rqst_plan_info, post_errors):
    modify_plan_params = get_plan_mgmt_put_params(rqst_plan_info, post_errors)
    rqst_plan_id = clean_int_value_from_dict_object(rqst_plan_info, "root", "Database ID", post_errors)

    healthcare_plan_obj = None
    if not post_errors:
        healthcare_plan_obj = modify_instance_using_validated_params(modify_plan_params, rqst_plan_id, post_errors)

    return healthcare_plan_obj


def validate_rqst_params_and_delete_instance(rqst_carrier_info, post_errors):
    rqst_plan_id = clean_int_value_from_dict_object(rqst_carrier_info, "root", "Database ID", post_errors)

    if not post_errors:
        delete_instance_using_validated_params(rqst_plan_id, post_errors)
