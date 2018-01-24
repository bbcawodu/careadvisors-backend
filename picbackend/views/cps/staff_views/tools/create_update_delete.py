"""
Defines utility functions and classes for staff views
"""

from picbackend.views.utils import clean_string_value_from_dict_object
from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_list_value_from_dict_object
from picmodels.models import NavMetricsLocation
from django.core.validators import validate_email
from django import forms


def validate_staff_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {
        'rqst_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)
    }

    rqst_action = validated_params['rqst_action']

    if rqst_action == 'create':
        validate_add_staff_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'update':
        validated_params['rqst_usr_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_modify_staff_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'delete':
        validated_params['rqst_usr_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)

    return validated_params


def validate_add_staff_params(rqst_body, validated_params, rqst_errors):
    rqst_usr_email = clean_string_value_from_dict_object(rqst_body, "root", "email", rqst_errors)
    if rqst_usr_email and not rqst_errors:
        try:
            validate_email(rqst_usr_email)
        except forms.ValidationError:
            rqst_errors.append("{!s} must be a valid email address".format(rqst_usr_email))

    rqst_usr_f_name = clean_string_value_from_dict_object(rqst_body, "root", "first_name", rqst_errors)
    rqst_usr_l_name = clean_string_value_from_dict_object(rqst_body, "root", "last_name", rqst_errors)
    rqst_county = clean_string_value_from_dict_object(rqst_body, "root", "county", rqst_errors)
    rqst_usr_type = clean_string_value_from_dict_object(rqst_body, "root", "type", rqst_errors)
    rqst_base_locations = clean_list_value_from_dict_object(rqst_body, "root", "base_locations", rqst_errors,
                                                            empty_list_allowed=True)

    base_location_objects = []
    location_errors = []
    if rqst_base_locations:
        rqst_base_locations = list(set(rqst_base_locations))
        for base_location_name in rqst_base_locations:
            try:
                base_location_object = NavMetricsLocation.objects.get(name=base_location_name)
                base_location_objects.append(base_location_object)
            except NavMetricsLocation.DoesNotExist:
                location_errors.append(
                    "No Nav Hub Location Database entry found for name: {!s}".format(base_location_name))
    for location_error in location_errors:
        rqst_errors.append(location_error)

    validated_params["rqst_usr_email"] = rqst_usr_email
    validated_params["rqst_usr_f_name"] = rqst_usr_f_name
    validated_params["rqst_usr_l_name"] = rqst_usr_l_name
    validated_params["rqst_county"] = rqst_county
    validated_params["rqst_usr_type"] = rqst_usr_type
    validated_params["base_location_objects"] = base_location_objects


def validate_modify_staff_params(rqst_body, validated_params, rqst_errors):
    if "email" in rqst_body:
        rqst_usr_email = clean_string_value_from_dict_object(rqst_body, "root", "email", rqst_errors)
        if rqst_usr_email and not rqst_errors:
            try:
                validate_email(rqst_usr_email)
                validated_params["rqst_usr_email"] = rqst_usr_email
            except forms.ValidationError:
                rqst_errors.append("{!s} must be a valid email address".format(rqst_usr_email))

    if "first_name" in rqst_body:
        rqst_usr_f_name = clean_string_value_from_dict_object(rqst_body, "root", "first_name", rqst_errors)
        validated_params["rqst_usr_f_name"] = rqst_usr_f_name

    if "last_name" in rqst_body:
        rqst_usr_l_name = clean_string_value_from_dict_object(rqst_body, "root", "last_name", rqst_errors)
        validated_params["rqst_usr_l_name"] = rqst_usr_l_name

    if "county" in rqst_body:
        rqst_county = clean_string_value_from_dict_object(rqst_body, "root", "county", rqst_errors)
        validated_params["rqst_county"] = rqst_county

    if "type" in rqst_body:
        rqst_usr_type = clean_string_value_from_dict_object(rqst_body, "root", "type", rqst_errors)
        validated_params["rqst_usr_type"] = rqst_usr_type

    if "base_locations" in rqst_body:
        rqst_base_locations = clean_list_value_from_dict_object(rqst_body, "root", "base_locations", rqst_errors,
                                                                empty_list_allowed=True)

        rqst_base_locations = list(set(rqst_base_locations))
        base_location_objects = []
        location_errors = []
        if rqst_base_locations:
            for base_location_name in rqst_base_locations:
                try:
                    base_location_object = NavMetricsLocation.objects.get(name=base_location_name)
                    base_location_objects.append(base_location_object)
                except NavMetricsLocation.DoesNotExist:
                    location_errors.append(
                        "No Nav Hub Location Database entry found for name: {!s}".format(base_location_name))
        for location_error in location_errors:
            rqst_errors.append(location_error)

        validated_params["base_location_objects"] = base_location_objects

    if len(validated_params.keys()) < 2:
        rqst_errors.append('Not enough given parameters to modify staff instance.')
