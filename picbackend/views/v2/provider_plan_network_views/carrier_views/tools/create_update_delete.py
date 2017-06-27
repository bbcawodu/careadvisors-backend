"""
This module defines utility functions and classes for views that handle carriers for provider networks contracted with
PIC
"""

from ....utils import clean_string_value_from_dict_object
from ....utils import clean_int_value_from_dict_object
from picmodels.services.provider_plan_network_services.healthcare_carrier_services import add_instance_using_validated_params
from picmodels.services.provider_plan_network_services.healthcare_carrier_services import modify_instance_using_validated_params
from picmodels.services.provider_plan_network_services.healthcare_carrier_services import delete_instance_using_validated_params


def validate_rqst_params_and_add_instance(rqst_carrier_info, post_errors):
    add_carrier_params = get_carrier_mgmt_put_params(rqst_carrier_info, post_errors)

    healthcare_carrier_obj = None
    if not post_errors:
        healthcare_carrier_obj = add_instance_using_validated_params(add_carrier_params, post_errors)

    return healthcare_carrier_obj


def get_carrier_mgmt_put_params(rqst_carrier_info, post_errors):
    rqst_carrier_name = clean_string_value_from_dict_object(rqst_carrier_info, "root", "name", post_errors)
    rqst_carrier_state = clean_string_value_from_dict_object(rqst_carrier_info, "root", "state_province", post_errors)

    return {"rqst_carrier_name": rqst_carrier_name,
            "rqst_carrier_state": rqst_carrier_state}


def validate_rqst_params_and_modify_instance(rqst_carrier_info, post_errors):
    modify_carrier_params = get_carrier_mgmt_put_params(rqst_carrier_info, post_errors)
    rqst_carrier_id = clean_int_value_from_dict_object(rqst_carrier_info, "root", "Database ID", post_errors)

    healthcare_carrier_obj = None
    if not post_errors:
        healthcare_carrier_obj = modify_instance_using_validated_params(modify_carrier_params, rqst_carrier_id, post_errors)

    return healthcare_carrier_obj


def validate_rqst_params_and_delete_instance(rqst_carrier_info, post_errors):
    rqst_carrier_id = clean_int_value_from_dict_object(rqst_carrier_info, "root", "Database ID", post_errors)

    if not post_errors:
        delete_instance_using_validated_params(rqst_carrier_id, post_errors)
