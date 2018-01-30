"""
Defines utility functions and classes for staff views
"""

from django import forms
from django.core.validators import validate_email

from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_list_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picmodels.models import NavMetricsLocation


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {
        'rqst_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)
    }

    rqst_action = validated_params['rqst_action']

    if rqst_action == 'create':
        validate_create_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'update':
        validated_params['rqst_usr_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_update_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'delete':
        validated_params['rqst_usr_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)

    return validated_params


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    rqst_usr_email = clean_string_value_from_dict_object(rqst_body, "root", "Email", rqst_errors)
    if rqst_usr_email and not rqst_errors:
        try:
            validate_email(rqst_usr_email)
        except forms.ValidationError:
            rqst_errors.append("{!s} must be a valid email address".format(rqst_usr_email))

    rqst_usr_mpn = clean_string_value_from_dict_object(rqst_body, "root", "MPN", rqst_errors, empty_string_allowed=True,
                                                       none_allowed=True)
    if rqst_usr_mpn is None:
        rqst_usr_mpn = ''
    rqst_usr_f_name = clean_string_value_from_dict_object(rqst_body, "root", "First Name", rqst_errors)
    rqst_usr_l_name = clean_string_value_from_dict_object(rqst_body, "root", "Last Name", rqst_errors)
    rqst_county = clean_string_value_from_dict_object(rqst_body, "root", "User County", rqst_errors)
    rqst_usr_type = clean_string_value_from_dict_object(rqst_body, "root", "User Type", rqst_errors)
    rqst_base_locations = clean_list_value_from_dict_object(rqst_body, "root", "Base Locations", rqst_errors,
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
    validated_params["rqst_usr_mpn"] = rqst_usr_mpn
    validated_params["rqst_usr_f_name"] = rqst_usr_f_name
    validated_params["rqst_usr_l_name"] = rqst_usr_l_name
    validated_params["rqst_county"] = rqst_county
    validated_params["rqst_usr_type"] = rqst_usr_type
    validated_params["base_location_objects"] = base_location_objects

    return validated_params


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "Email" in rqst_body:
        rqst_usr_email = clean_string_value_from_dict_object(rqst_body, "root", "Email", rqst_errors)
        if rqst_usr_email and not rqst_errors:
            try:
                validate_email(rqst_usr_email)
            except forms.ValidationError:
                rqst_errors.append("{!s} must be a valid email address".format(rqst_usr_email))
        validated_params["rqst_usr_email"] = rqst_usr_email

    if "MPN" in rqst_body:
        rqst_usr_mpn = clean_string_value_from_dict_object(rqst_body, "root", "MPN", rqst_errors, empty_string_allowed=True,
                                                           none_allowed=True)
        if rqst_usr_mpn is None:
            rqst_usr_mpn = ''
        validated_params["rqst_usr_mpn"] = rqst_usr_mpn

    if "First Name" in rqst_body:
        rqst_usr_f_name = clean_string_value_from_dict_object(rqst_body, "root", "First Name", rqst_errors)
        validated_params["rqst_usr_f_name"] = rqst_usr_f_name

    if "Last Name" in rqst_body:
        rqst_usr_l_name = clean_string_value_from_dict_object(rqst_body, "root", "Last Name", rqst_errors)
        validated_params["rqst_usr_l_name"] = rqst_usr_l_name

    if "User County" in rqst_body:
        rqst_county = clean_string_value_from_dict_object(rqst_body, "root", "User County", rqst_errors)
        validated_params["rqst_county"] = rqst_county

    if "User Type" in rqst_body:
        rqst_usr_type = clean_string_value_from_dict_object(rqst_body, "root", "User Type", rqst_errors)
        validated_params["rqst_usr_type"] = rqst_usr_type

    if "Base Locations" in rqst_body:
        rqst_base_locations = clean_list_value_from_dict_object(rqst_body, "root", "Base Locations", rqst_errors,
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
        validated_params["base_location_objects"] = base_location_objects

    return validated_params
