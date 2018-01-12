"""
This module defines utility functions and classes for views that handle provider networks contracted with PIC
"""

from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picmodels.services.provider_plan_network_services.provider_network_services import \
    add_instance_using_validated_params
from picmodels.services.provider_plan_network_services.provider_network_services import \
    delete_instance_using_validated_params
from picmodels.services.provider_plan_network_services.provider_network_services import \
    modify_instance_using_validated_params


def validate_rqst_params_and_add_instance(rqst_provider_network_info, post_errors):
    add_provider_network_params = get_provider_network_mgmt_put_params(rqst_provider_network_info, post_errors)

    provider_network_obj = None
    if not post_errors:
        provider_network_obj = add_instance_using_validated_params(add_provider_network_params, post_errors)

    return provider_network_obj


def get_provider_network_mgmt_put_params(rqst_provider_network_info, post_errors):
    rqst_provider_network_name = clean_string_value_from_dict_object(rqst_provider_network_info, "root", "name", post_errors)

    return {"rqst_provider_network_name": rqst_provider_network_name,}


def validate_rqst_params_and_modify_instance(rqst_provider_network_info, post_errors):
    modify_provider_network_params = get_provider_network_mgmt_put_params(rqst_provider_network_info, post_errors)
    rqst_provider_network_id = clean_int_value_from_dict_object(rqst_provider_network_info, "root", "Database ID", post_errors)

    provider_network_obj = None
    if not post_errors:
        provider_network_obj = modify_instance_using_validated_params(modify_provider_network_params, rqst_provider_network_id, post_errors)

    return provider_network_obj


def validate_rqst_params_and_delete_instance(rqst_provider_network_info, post_errors):
    rqst_provider_network_id = clean_int_value_from_dict_object(rqst_provider_network_info, "root", "Database ID", post_errors)

    if not post_errors:
        delete_instance_using_validated_params(rqst_provider_network_id, post_errors)
