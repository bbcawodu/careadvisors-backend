"""
This module defines utility functions and classes for views that handle accepted plans for provider networks contracted
with PIC
"""

import re

from picbackend.views.utils import clean_float_value_from_dict_object
from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object

from picmodels.models import HealthcareServiceCostEntry


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {
        'rqst_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)
    }

    rqst_action = validated_params['rqst_action']

    if rqst_action == 'create':
        validate_create_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'update':
        validated_params['rqst_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_update_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'delete':
        validated_params['rqst_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)

    return validated_params


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    """
    This function parses the BODY of requests for PIC consumer management PUT requests, checks for errors, and returns
    relevant information as a dictionary

    :param rqst_body: (type: dictionary) Carrier information to be parsed
    :param rqst_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary with relevant consumer information
    """

    # Summary report fields
    validated_params["medical_deductible_individual_standard"] = clean_float_value_from_dict_object(
        rqst_body,
        "root",
        "medical_deductible_individual_standard",
        rqst_errors,
        none_allowed=True,
        no_key_allowed=True
    )

    validated_params["medical_out_of_pocket_max_individual_standard"] = clean_float_value_from_dict_object(
        rqst_body,
        "root",
        "medical_out_of_pocket_max_individual_standard",
        rqst_errors,
        none_allowed=True,
        no_key_allowed=True
    )

    rqst_primary_care_physician_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "primary_care_physician_standard_cost",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        ),
        "primary_care_physician_individual_standard_cost",
        rqst_errors
    )
    validated_params["primary_care_physician_standard_cost"] = rqst_primary_care_physician_standard_cost

    # Detailed report fields
    validated_params["rqst_plan_name"] = clean_string_value_from_dict_object(rqst_body, "root", "name", rqst_errors)

    validated_params["rqst_carrier_id"] = clean_int_value_from_dict_object(
        rqst_body,
        "root",
        "Carrier Database ID",
        rqst_errors
    )

    validated_params["rqst_plan_premium_type"] = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "premium_type",
        rqst_errors,
        none_allowed=True,
        no_key_allowed=True
    )

    validated_params["rqst_plan_metal_level"] = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "metal_level",
        rqst_errors,
        none_allowed=True,
        no_key_allowed=True
    )

    validated_params["county"] = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "county",
        rqst_errors,
        none_allowed=True,
        no_key_allowed=True
    )

    rqst_specialist_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "specialist_standard_cost",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        ),
        "specialist_standard_cost",
        rqst_errors
    )
    validated_params["specialist_standard_cost"] = rqst_specialist_standard_cost

    rqst_emergency_room_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "emergency_room_standard_cost",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        ),
        "emergency_room_standard_cost",
        rqst_errors
    )
    validated_params["emergency_room_standard_cost"] = rqst_emergency_room_standard_cost

    rqst_inpatient_facility_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "inpatient_facility_standard_cost",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        ),
        "inpatient_facility_standard_cost",
        rqst_errors
    )
    validated_params["inpatient_facility_standard_cost"] = rqst_inpatient_facility_standard_cost

    rqst_generic_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "generic_drugs_standard_cost",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        ),
        "generic_drugs_standard_cost",
        rqst_errors
    )
    validated_params["generic_drugs_standard_cost"] = rqst_generic_drugs_standard_cost

    rqst_preferred_brand_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "preferred_brand_drugs_standard_cost",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        ),
        "preferred_brand_drugs_standard_cost",
        rqst_errors
    )
    validated_params["preferred_brand_drugs_standard_cost"] = rqst_preferred_brand_drugs_standard_cost

    rqst_non_preferred_brand_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "non_preferred_brand_drugs_standard_cost",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        ),
        "non_preferred_brand_drugs_standard_cost",
        rqst_errors
    )
    validated_params["non_preferred_brand_drugs_standard_cost"] = rqst_non_preferred_brand_drugs_standard_cost

    rqst_specialty_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
        clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "specialty_drugs_standard_cost",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        ),
        "specialty_drugs_standard_cost",
        rqst_errors
    )
    validated_params["specialty_drugs_standard_cost"] = rqst_specialty_drugs_standard_cost

    # Extra benefit report fields
    validated_params["medical_deductible_family_standard"] = clean_float_value_from_dict_object(
        rqst_body,
        "root",
        "medical_deductible_family_standard",
        rqst_errors,
        none_allowed=True,
        no_key_allowed=True
    )

    validated_params["medical_out_of_pocket_max_family_standard"] = clean_float_value_from_dict_object(
        rqst_body,
        "root",
        "medical_out_of_pocket_max_family_standard",
        rqst_errors,
        none_allowed=True,
        no_key_allowed=True
    )


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    """
    This function parses the BODY of requests for PIC consumer management PUT requests, checks for errors, and returns
    relevant information as a dictionary

    :param rqst_body: (type: dictionary) Carrier information to be parsed
    :param rqst_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary with relevant consumer information
    """

    # Summary report fields
    if "medical_deductible_individual_standard" in rqst_body:
        validated_params["medical_deductible_individual_standard"] = clean_float_value_from_dict_object(
            rqst_body,
            "root",
            "medical_deductible_individual_standard",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        )

    if "medical_out_of_pocket_max_individual_standard" in rqst_body:
        validated_params["medical_out_of_pocket_max_individual_standard"] = clean_float_value_from_dict_object(
            rqst_body,
            "root",
            "medical_out_of_pocket_max_individual_standard",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        )

    if "primary_care_physician_standard_cost" in rqst_body:
        rqst_primary_care_physician_standard_cost = create_healthcare_service_cost_instances_from_string(
            clean_string_value_from_dict_object(
                rqst_body,
                "root",
                "primary_care_physician_standard_cost",
                rqst_errors,
                none_allowed=True,
                no_key_allowed=True
            ),
            "primary_care_physician_individual_standard_cost",
            rqst_errors
        )
        validated_params["primary_care_physician_standard_cost"] = rqst_primary_care_physician_standard_cost

    # Detailed report fields
    if "name" in rqst_body:
        validated_params["rqst_plan_name"] = clean_string_value_from_dict_object(rqst_body, "root", "name", rqst_errors)

    if "Carrier Database ID" in rqst_body:
        validated_params["rqst_carrier_id"] = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "Carrier Database ID",
            rqst_errors
        )

    if "premium_type" in rqst_body:
        validated_params["rqst_plan_premium_type"] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "premium_type",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        )

    if "metal_level" in rqst_body:
        validated_params["rqst_plan_metal_level"] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "metal_level",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        )

    if "county" in rqst_body:
        validated_params["county"] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "county",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        )

    if "specialist_standard_cost" in rqst_body:
        rqst_specialist_standard_cost = create_healthcare_service_cost_instances_from_string(
            clean_string_value_from_dict_object(
                rqst_body,
                "root",
                "specialist_standard_cost",
                rqst_errors,
                none_allowed=True,
                no_key_allowed=True
            ),
            "specialist_standard_cost",
            rqst_errors
        )
        validated_params["specialist_standard_cost"] = rqst_specialist_standard_cost

    if "emergency_room_standard_cost" in rqst_body:
        rqst_emergency_room_standard_cost = create_healthcare_service_cost_instances_from_string(
            clean_string_value_from_dict_object(
                rqst_body,
                "root",
                "emergency_room_standard_cost",
                rqst_errors,
                none_allowed=True,
                no_key_allowed=True
            ),
            "emergency_room_standard_cost",
            rqst_errors
        )
        validated_params["emergency_room_standard_cost"] = rqst_emergency_room_standard_cost

    if "inpatient_facility_standard_cost" in rqst_body:
        rqst_inpatient_facility_standard_cost = create_healthcare_service_cost_instances_from_string(
            clean_string_value_from_dict_object(
                rqst_body,
                "root",
                "inpatient_facility_standard_cost",
                rqst_errors,
                none_allowed=True,
                no_key_allowed=True
            ),
            "inpatient_facility_standard_cost",
            rqst_errors
        )
        validated_params["inpatient_facility_standard_cost"] = rqst_inpatient_facility_standard_cost

    if "generic_drugs_standard_cost" in rqst_body:
        rqst_generic_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
            clean_string_value_from_dict_object(
                rqst_body,
                "root",
                "generic_drugs_standard_cost",
                rqst_errors,
                none_allowed=True,
                no_key_allowed=True
            ),
            "generic_drugs_standard_cost",
            rqst_errors
        )
        validated_params["generic_drugs_standard_cost"] = rqst_generic_drugs_standard_cost

    if "preferred_brand_drugs_standard_cost" in rqst_body:
        rqst_preferred_brand_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
            clean_string_value_from_dict_object(
                rqst_body,
                "root",
                "preferred_brand_drugs_standard_cost",
                rqst_errors,
                none_allowed=True,
                no_key_allowed=True
            ),
            "preferred_brand_drugs_standard_cost",
            rqst_errors
        )
        validated_params["preferred_brand_drugs_standard_cost"] = rqst_preferred_brand_drugs_standard_cost

    if "non_preferred_brand_drugs_standard_cost" in rqst_body:
        rqst_non_preferred_brand_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
            clean_string_value_from_dict_object(
                rqst_body,
                "root",
                "non_preferred_brand_drugs_standard_cost",
                rqst_errors,
                none_allowed=True,
                no_key_allowed=True
            ),
            "non_preferred_brand_drugs_standard_cost",
            rqst_errors
        )
        validated_params["non_preferred_brand_drugs_standard_cost"] = rqst_non_preferred_brand_drugs_standard_cost

    if "specialty_drugs_standard_cost" in rqst_body:
        rqst_specialty_drugs_standard_cost = create_healthcare_service_cost_instances_from_string(
            clean_string_value_from_dict_object(
                rqst_body,
                "root",
                "specialty_drugs_standard_cost",
                rqst_errors,
                none_allowed=True,
                no_key_allowed=True
            ),
            "specialty_drugs_standard_cost",
            rqst_errors
        )
        validated_params["specialty_drugs_standard_cost"] = rqst_specialty_drugs_standard_cost

    # Extra benefit report fields
    if "medical_deductible_family_standard" in rqst_body:
        validated_params["medical_deductible_family_standard"] = clean_float_value_from_dict_object(
            rqst_body,
            "root",
            "medical_deductible_family_standard",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        )

    if "medical_out_of_pocket_max_family_standard" in rqst_body:
        validated_params["medical_out_of_pocket_max_family_standard"] = clean_float_value_from_dict_object(
            rqst_body,
            "root",
            "medical_out_of_pocket_max_family_standard",
            rqst_errors,
            none_allowed=True,
            no_key_allowed=True
        )


def create_healthcare_service_cost_instances_from_string(cost_string, field_name, rqst_errors):
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
                            rqst_errors.append("Coinsurance percentage is improperly formatted(returned 0) for field: {}".format(field_name))
                    elif no_of_coinsurance_percentage_numbers == 0 or no_of_coinsurance_percentage_numbers > 1:
                        rqst_errors.append("Coinsurance percentage is improperly formatted for field: {}".format(field_name))
                elif no_of_coinsurance_percentages > 1:
                    rqst_errors.append("More than one coinsurance percentage is included in field: {}".format(field_name))

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
                            rqst_errors.append("Copay cost is improperly formatted(returned 0) for field: {}".format(field_name))
                    elif no_of_copay_numbers == 0 or no_of_copay_numbers > 1:
                        rqst_errors.append("Copay cost is improperly formatted for field: {}".format(field_name))
                elif no_of_copays > 1:
                    rqst_errors.append("More than one copay cost is included in field: {}".format(field_name))

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

            if not rqst_errors:
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
                        rqst_errors.append("Valid cost relation to deductible was not able to be processed for field: {}".format(field_name))

                    if not rqst_errors:
                        healthcare_service_cost_instances.append(healthcare_service_cost_instance)
                else:
                    rqst_errors.append("Valid cost was not able to be processed for field: {}".format(field_name))
        for cost_string_piece in cost_string_list:
            create_healthcare_service_cost_instance_from_cost_string_fragment(cost_string_piece)

    return healthcare_service_cost_instances
