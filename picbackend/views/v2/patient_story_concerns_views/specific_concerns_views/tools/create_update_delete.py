"""
This module defines utility functions and classes for views that handle locations for provider networks that are
contracted with PIC
"""

from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_list_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picmodels.models import ConsumerGeneralConcern
from picmodels.models import ConsumerSpecificConcern


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


def validate_rqst_params_and_add_instance(rqst_specific_concern_info, rqst_errors):
    add_specific_concern_params = get_specific_concern_mgmt_put_params(rqst_specific_concern_info, rqst_errors)

    specific_concern_obj = None
    if not rqst_errors:
        specific_concern_obj = add_instance_using_validated_params(add_specific_concern_params, rqst_errors)

    return specific_concern_obj


def get_specific_concern_mgmt_put_params(rqst_provider_location_info, post_errors):
    rqst_specific_concern_research_weight = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                             "research_weight", post_errors,
                                                                             no_key_allowed=True)
    if not rqst_specific_concern_research_weight:
        rqst_specific_concern_research_weight = ConsumerSpecificConcern.RESEARCH_WEIGHT_DEFAULT
    elif rqst_specific_concern_research_weight > 100:
        post_errors.append("Value for 'research_weight' must be less than 100. Given value is: {}".format(rqst_specific_concern_research_weight))

    rqst_related_general_concerns_names = clean_list_value_from_dict_object(rqst_provider_location_info, "root",
                                                                            "related_general_concerns", post_errors,
                                                                            empty_list_allowed=True)
    for indx, general_concern_name in enumerate(rqst_related_general_concerns_names):
        if not isinstance(general_concern_name, str):
            post_errors.append("All related general concerns must be strings, related general concern is not an string for 'related_general_concerns' field at index: {}".format(indx))
    rqst_related_general_concerns_names = list(set(rqst_related_general_concerns_names))
    related_general_concerns_objects = []
    related_general_concerns_errors = []
    if rqst_related_general_concerns_names and not post_errors:
        for related_general_concerns_name in rqst_related_general_concerns_names:
            try:
                related_general_concerns_object = ConsumerGeneralConcern.objects.get(name__iexact=related_general_concerns_name)
                related_general_concerns_objects.append(related_general_concerns_object)
            except ConsumerGeneralConcern.DoesNotExist:
                related_general_concerns_errors.append(
                    "No related ConsumerGeneralConcern database entry found for name: {}".format(related_general_concerns_name))
    for related_general_concerns_error in related_general_concerns_errors:
        post_errors.append(related_general_concerns_error)

    return {"rqst_specific_concern_question": clean_string_value_from_dict_object(rqst_provider_location_info, "root", "question", post_errors),
            "rqst_specific_concern_research_weight": rqst_specific_concern_research_weight,
            "related_general_concerns_objects": related_general_concerns_objects}


def validate_rqst_params_and_modify_instance(rqst_specific_concern_info, rqst_errors):
    modify_specific_concern_params = get_specific_concern_mgmt_put_params(rqst_specific_concern_info, rqst_errors)
    rqst_specific_concern_id = clean_int_value_from_dict_object(rqst_specific_concern_info, "root", "Database ID", rqst_errors)

    specific_concern_obj = None
    if not rqst_errors:
        specific_concern_obj = modify_instance_using_validated_params(modify_specific_concern_params, rqst_specific_concern_id, rqst_errors)

    return specific_concern_obj


def validate_rqst_params_and_add_general_concern_to_instance(rqst_specific_concern_info, rqst_errors):
    modify_specific_concern_params = get_specific_concern_mgmt_put_params(rqst_specific_concern_info, rqst_errors)
    rqst_specific_concern_id = clean_int_value_from_dict_object(rqst_specific_concern_info, "root",
                                                                 "Database ID", rqst_errors)

    specific_concern_obj = None
    if not rqst_errors:
        specific_concern_obj = add_general_concern_to_instance_using_validated_params(modify_specific_concern_params, rqst_specific_concern_id, rqst_errors)

    return specific_concern_obj


def validate_rqst_params_and_remove_general_concern_from_instance(rqst_specific_concern_info, rqst_errors):
    modify_specific_concern_params = get_specific_concern_mgmt_put_params(rqst_specific_concern_info, rqst_errors)
    rqst_specific_concern_id = clean_int_value_from_dict_object(rqst_specific_concern_info, "root",
                                                                "Database ID", rqst_errors)

    specific_concern_obj = None
    if not rqst_errors:
        specific_concern_obj = remove_general_concern_from_instance_using_validated_params(modify_specific_concern_params,
                                                                                           rqst_specific_concern_id,
                                                                                           rqst_errors)

    return specific_concern_obj


def validate_rqst_params_and_delete_instance(rqst_specific_concern_info, rqst_errors):
    rqst_specific_concern_id = clean_int_value_from_dict_object(rqst_specific_concern_info, "root", "Database ID", rqst_errors)

    if not rqst_errors:
        delete_instance_using_validated_params(rqst_specific_concern_id, rqst_errors)
