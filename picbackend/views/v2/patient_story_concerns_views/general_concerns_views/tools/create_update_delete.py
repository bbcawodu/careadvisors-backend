"""
This module defines utility functions and classes for views that handle carriers for provider networks contracted with
PIC
"""

from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picmodels.services.patient_story_models_services.consumer_general_concern_services import \
    add_instance_using_validated_params
from picmodels.services.patient_story_models_services.consumer_general_concern_services import \
    delete_instance_using_validated_params
from picmodels.services.patient_story_models_services.consumer_general_concern_services import \
    modify_instance_using_validated_params


def validate_rqst_params_and_add_instance(rqst_gen_concern_info, rqst_errors):
    add_general_concern_params = get_general_concern_mgmt_put_params(rqst_gen_concern_info, rqst_errors)

    general_concern_obj = None
    if not rqst_errors:
        general_concern_obj = add_instance_using_validated_params(add_general_concern_params, rqst_errors)

    return general_concern_obj


def get_general_concern_mgmt_put_params(rqst_carrier_info, rqst_errors):

    return {
        "rqst_general_concern_name": clean_string_value_from_dict_object(rqst_carrier_info, "root", "name", rqst_errors),
            }


def validate_rqst_params_and_modify_instance(rqst_general_concern_info, rqst_errors):
    modify_general_concern_params = get_general_concern_mgmt_put_params(rqst_general_concern_info, rqst_errors)
    rqst_general_concern_id = clean_int_value_from_dict_object(rqst_general_concern_info, "root", "Database ID", rqst_errors)

    general_concern_obj = None
    if not rqst_errors:
        general_concern_obj = modify_instance_using_validated_params(modify_general_concern_params, rqst_general_concern_id, rqst_errors)

    return general_concern_obj


def validate_rqst_params_and_delete_instance(rqst_general_concern_info, rqst_errors):
    rqst_general_concern_id = clean_int_value_from_dict_object(rqst_general_concern_info, "root", "Database ID", rqst_errors)

    if not rqst_errors:
        delete_instance_using_validated_params(rqst_general_concern_id, rqst_errors)
