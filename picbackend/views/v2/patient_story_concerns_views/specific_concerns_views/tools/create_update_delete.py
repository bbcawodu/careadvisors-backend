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


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    validated_params["rqst_specific_concern_question"] = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "question",
        rqst_errors
    )

    rqst_specific_concern_research_weight = clean_int_value_from_dict_object(
        rqst_body,
        "root",
        "research_weight",
        rqst_errors,
        no_key_allowed=True
    )
    if not rqst_specific_concern_research_weight:
        rqst_specific_concern_research_weight = ConsumerSpecificConcern.RESEARCH_WEIGHT_DEFAULT
    elif rqst_specific_concern_research_weight > 100:
        rqst_errors.append("Value for 'research_weight' must be less than 100. Given value is: {}".format(rqst_specific_concern_research_weight))
    validated_params["rqst_specific_concern_research_weight"] = rqst_specific_concern_research_weight

    if "add_related_general_concerns" in rqst_body:
        rqst_add_related_general_concerns_names = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_related_general_concerns",
            rqst_errors,
            empty_list_allowed=True
        )
        add_related_general_concerns_objects = []
        if rqst_add_related_general_concerns_names:
            validate_related_gen_concern_names(rqst_add_related_general_concerns_names, rqst_errors)

            if not rqst_errors:
                add_related_general_concerns_objects = ConsumerGeneralConcern.retrieve_related_gen_concern_rows_by_name(
                    rqst_add_related_general_concerns_names,
                    rqst_errors
                )
        validated_params["add_related_general_concerns_objects"] = add_related_general_concerns_objects


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "question" in rqst_body:
        validated_params["rqst_specific_concern_question"] = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "question",
            rqst_errors
        )

    if "research_weight" in rqst_body:
        rqst_specific_concern_research_weight = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "research_weight",
            rqst_errors,
            no_key_allowed=True
        )
        if not rqst_specific_concern_research_weight:
            rqst_specific_concern_research_weight = ConsumerSpecificConcern.RESEARCH_WEIGHT_DEFAULT
        elif rqst_specific_concern_research_weight > 100:
            rqst_errors.append("Value for 'research_weight' must be less than 100. Given value is: {}".format(rqst_specific_concern_research_weight))
        validated_params["rqst_specific_concern_research_weight"] = rqst_specific_concern_research_weight

    if "add_related_general_concerns" in rqst_body:
        rqst_add_related_general_concerns_names = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_related_general_concerns",
            rqst_errors,
        )
        add_related_general_concerns_objects = []
        if rqst_add_related_general_concerns_names:
            validate_related_gen_concern_names(rqst_add_related_general_concerns_names, rqst_errors)

            if not rqst_errors:
                add_related_general_concerns_objects = ConsumerGeneralConcern.retrieve_related_gen_concern_rows_by_name(
                    rqst_add_related_general_concerns_names,
                    rqst_errors
                )
        validated_params["add_related_general_concerns_objects"] = add_related_general_concerns_objects
    elif "remove_related_general_concerns" in rqst_body:
        rqst_remove_related_general_concerns_names = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_related_general_concerns",
            rqst_errors,
        )
        remove_related_general_concerns_objects = []
        if rqst_remove_related_general_concerns_names:
            validate_related_gen_concern_names(rqst_remove_related_general_concerns_names, rqst_errors)

            if not rqst_errors:
                remove_related_general_concerns_objects = ConsumerGeneralConcern.retrieve_related_gen_concern_rows_by_name(
                    rqst_remove_related_general_concerns_names,
                    rqst_errors
                )
        validated_params["remove_related_general_concerns_objects"] = remove_related_general_concerns_objects


def validate_related_gen_concern_names(gen_concern_names, rqst_errors):
    for indx, general_concern_name in enumerate(gen_concern_names):
        if not isinstance(general_concern_name, str):
            rqst_errors.append(
                "All related general concerns must be strings, related general concern is not an string for 'related_general_concerns' field at index: {}".format(
                    indx
                )
            )
