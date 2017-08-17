"""
This module defines utility functions and classes for views that handle locations for provider networks that are
contracted with PIC
"""

from picmodels.models import HealthcarePlan
from ....utils import clean_string_value_from_dict_object
from ....utils import clean_int_value_from_dict_object
from ....utils import clean_list_value_from_dict_object
from picmodels.services.provider_plan_network_services.provider_location_services import add_instance_using_validated_params
from picmodels.services.provider_plan_network_services.provider_location_services import modify_instance_using_validated_params
from picmodels.services.provider_plan_network_services.provider_location_services import add_accepted_plans_to_instance_using_validated_params
from picmodels.services.provider_plan_network_services.provider_location_services import remove_accepted_plans_from_instance_using_validated_params
from picmodels.services.provider_plan_network_services.provider_location_services import delete_instance_using_validated_params


def validate_rqst_params_and_add_instance(rqst_provider_location_info, post_errors):
    add_provider_location_params = get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors)

    provider_location_obj = None
    if not post_errors:
        provider_location_obj = add_instance_using_validated_params(add_provider_location_params, post_errors)

    return provider_location_obj


def get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors):
    rqst_provider_location_name = clean_string_value_from_dict_object(rqst_provider_location_info, "root", "name", post_errors)
    rqst_provider_network_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                "provider_network Database ID", post_errors)
    rqst_accepted_plans_ids = clean_list_value_from_dict_object(rqst_provider_location_info, "root", "accepted_plans",
                                                            post_errors, empty_list_allowed=True)
    for indx, plan_id in enumerate(rqst_accepted_plans_ids):
        if not isinstance(plan_id, int):
            post_errors.append("All plan ids must be integers, plan id is not an integer for 'accepted_plans' field at index: {}".format(indx))
    rqst_accepted_plans_ids = list(set(rqst_accepted_plans_ids))
    accepted_plans_objects = []
    plans_errors = []
    if rqst_accepted_plans_ids and not post_errors:
        for accepted_plan_id in rqst_accepted_plans_ids:
            try:
                accepted_plan_object = HealthcarePlan.objects.get(id=accepted_plan_id)
                accepted_plans_objects.append(accepted_plan_object)
            except HealthcarePlan.DoesNotExist:
                plans_errors.append(
                    "No HealthcarePlan database entry found for id: {}".format(accepted_plan_id))
    for plan_error in plans_errors:
        post_errors.append(plan_error)

    return {"rqst_provider_location_name": rqst_provider_location_name,
            "rqst_provider_network_id": rqst_provider_network_id,
            "accepted_plans_objects": accepted_plans_objects}


def validate_rqst_params_and_modify_instance(rqst_provider_location_info, post_errors):
    modify_provider_location_params = get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors)
    rqst_provider_location_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root", "Database ID", post_errors)

    provider_location_obj = None
    if not post_errors:
        provider_location_obj = modify_instance_using_validated_params(modify_provider_location_params, rqst_provider_location_id, post_errors)

    return provider_location_obj


def validate_rqst_params_and_add_accepted_plans_to_instance(rqst_provider_location_info, post_errors):
    modify_provider_location_params = get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors)
    rqst_provider_location_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                 "Database ID", post_errors)

    provider_location_obj = None
    if not post_errors:
        provider_location_obj = add_accepted_plans_to_instance_using_validated_params(modify_provider_location_params, rqst_provider_location_id, post_errors)

    return provider_location_obj


def validate_rqst_params_and_remove_accepted_plans_from_instance(rqst_provider_location_info, post_errors):
    modify_provider_location_params = get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors)
    rqst_provider_location_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                 "Database ID", post_errors)

    provider_location_obj = None
    if not post_errors:
        provider_location_obj = remove_accepted_plans_from_instance_using_validated_params(modify_provider_location_params, rqst_provider_location_id, post_errors)

    return provider_location_obj


def validate_rqst_params_and_delete_instance(rqst_provider_location_info, post_errors):
    rqst_provider_location_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root", "Database ID", post_errors)

    if not post_errors:
        delete_instance_using_validated_params(rqst_provider_location_id, post_errors)
