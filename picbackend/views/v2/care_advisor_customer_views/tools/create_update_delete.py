"""
Defines utility functions and classes for staff views
"""

import re
from django import forms
from django.core.validators import validate_email

from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {}

    rqst_db_action = clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)
    validated_params['db_action'] = rqst_db_action

    if not rqst_errors:
        if rqst_db_action == 'create':
            validate_params_for_create_row(rqst_body, validated_params, rqst_errors)
        elif rqst_db_action == 'update':
            validate_params_for_update_row(rqst_body, validated_params, rqst_errors)
        elif rqst_db_action == 'delete':
            validate_params_for_delete_row(rqst_body, validated_params, rqst_errors)
        else:
            rqst_errors.append("No valid 'db_action' provided.")

    return validated_params


def validate_params_for_create_row(rqst_body, validated_params, rqst_errors):
    validated_params['full_name'] = clean_string_value_from_dict_object(rqst_body, "root", "full_name", rqst_errors)

    rqst_email = clean_string_value_from_dict_object(rqst_body, "root", "email", rqst_errors)
    if rqst_email is not None:
        try:
            validate_email(rqst_email)
        except forms.ValidationError:
            rqst_errors.append("{} must be a valid email address".format(rqst_email))
            rqst_email = None
    validated_params['email'] = rqst_email

    validated_params['company_name'] = clean_string_value_from_dict_object(rqst_body, "root", "company_name", rqst_errors)

    rqst_phone_number = clean_string_value_from_dict_object(rqst_body, "root", "phone_number", rqst_errors)
    if rqst_phone_number is not None:
        validate_phone_number(rqst_phone_number, rqst_errors)
    validated_params['phone_number'] = rqst_phone_number


def validate_phone_number(phone_number, rqst_errors):
    if not re.findall(r'^1?\d{10}$', phone_number):
        rqst_errors.append("{} must be a valid phone number".format(phone_number))


def validate_params_for_update_row(rqst_body, validated_params, rqst_errors):
    validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
    if 'full_name' in rqst_body:
        validated_params['full_name'] = clean_string_value_from_dict_object(rqst_body, "root", "full_name", rqst_errors)
    if 'email' in rqst_body:
        rqst_email = clean_string_value_from_dict_object(rqst_body, "root", "email", rqst_errors)
        if rqst_email is not None:
            try:
                validate_email(rqst_email)
            except forms.ValidationError:
                rqst_errors.append("{} must be a valid email address".format(rqst_email))
                rqst_email = None
        validated_params['email'] = rqst_email
    if 'company_name' in rqst_body:
        validated_params['company_name'] = clean_string_value_from_dict_object(rqst_body, "root", "company_name", rqst_errors)
    if 'phone_number' in rqst_body:
        rqst_phone_number = clean_string_value_from_dict_object(rqst_body, "root", "phone_number", rqst_errors)
        if rqst_phone_number is not None:
            validate_phone_number(rqst_phone_number, rqst_errors)
        validated_params['phone_number'] = rqst_phone_number


def validate_params_for_delete_row(rqst_body, validated_params, rqst_errors):
    validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
