import re
import datetime
import pytz
from django import forms
from django.core.validators import validate_email
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {'db_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)}

    if validated_params['db_action'] == 'create':
        validate_params_for_create_row(rqst_body, validated_params, rqst_errors)
    elif validated_params['db_action'] == 'update':
        validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_params_for_update_row(rqst_body, validated_params, rqst_errors)
    elif validated_params['db_action'] == 'delete':
        validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
    else:
        rqst_errors.append("No valid 'db_action' provided.")

    return validated_params


def validate_params_for_create_row(rqst_body, validated_params, rqst_errors):
    validated_params['company_name'] = clean_string_value_from_dict_object(rqst_body, "root", "company_name", rqst_errors)

    if "address_line_1" in rqst_body:
        address_line_1 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_1",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["address_line_1"] = address_line_1

    if "address_line_2" in rqst_body:
        address_line_2 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_2",
            rqst_errors,
            empty_string_allowed=True
        )
        if address_line_2 is None:
            address_line_2 = ''
        validated_params["address_line_2"] = address_line_2

    if "city" in rqst_body:
        city = clean_string_value_from_dict_object(rqst_body, "root", "city", rqst_errors, empty_string_allowed=True)
        validated_params["city"] = city

    if "state_province" in rqst_body:
        state_province = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "state_province",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["state_province"] = state_province

    if "zipcode" in rqst_body:
        zipcode = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "zipcode",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["zipcode"] = zipcode

    estimated_monthly_caseload = clean_int_value_from_dict_object(
        rqst_body,
        'root',
        "estimated_monthly_caseload",
        rqst_errors
    )
    if estimated_monthly_caseload:
        validator = MinValueValidator(0)
        try:
            validator(estimated_monthly_caseload)
        except ValidationError:
            rqst_errors.append(
                "estimated_monthly_caseload must be more than 0. Value is : {}".format(estimated_monthly_caseload)
            )
    validated_params["estimated_monthly_caseload"] = estimated_monthly_caseload

    contact_first_name = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "contact_first_name",
        rqst_errors
    )
    validated_params["contact_first_name"] = contact_first_name

    contact_last_name = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "contact_last_name",
        rqst_errors
    )
    validated_params["contact_last_name"] = contact_last_name

    contact_email = clean_string_value_from_dict_object(rqst_body, "root", "contact_email", rqst_errors)
    if contact_email is not None:
        try:
            validate_email(contact_email)
        except forms.ValidationError:
            rqst_errors.append("contact_email must be a valid email address. Value is : {}".format(contact_email))
            contact_email = None
    validated_params['contact_email'] = contact_email

    contact_phone = clean_string_value_from_dict_object(
        rqst_body,
        "root",
        "contact_phone",
        rqst_errors
    )
    if contact_phone:
        validate_phone_number(contact_phone, rqst_errors)
    validated_params["contact_phone"] = contact_phone

    appointment_datetime = clean_string_value_from_dict_object(rqst_body, "root", "appointment_datetime", rqst_errors)
    validated_appointment_datetime = None
    if appointment_datetime:
        try:
            validated_appointment_datetime = datetime.datetime.strptime(appointment_datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
        except ValueError:
            rqst_errors.append(
                'appointment_datetime must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                    appointment_datetime)
            )
    validated_params['appointment_datetime'] = validated_appointment_datetime

    if "appointment_datetime_2" in rqst_body:
        appointment_datetime_2 = clean_string_value_from_dict_object(rqst_body, "root", "appointment_datetime_2", rqst_errors, none_allowed=True)
        validated_appointment_datetime_2 = None
        if appointment_datetime_2:
            try:
                validated_appointment_datetime_2 = datetime.datetime.strptime(appointment_datetime_2, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'appointment_datetime_2 must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        appointment_datetime_2)
                )
        validated_params['appointment_datetime_2'] = validated_appointment_datetime_2

    if "appointment_datetime_3" in rqst_body:
        appointment_datetime_3 = clean_string_value_from_dict_object(rqst_body, "root", "appointment_datetime_3", rqst_errors, none_allowed=True)
        validated_appointment_datetime_3 = None
        if appointment_datetime_3:
            try:
                validated_appointment_datetime_3 = datetime.datetime.strptime(appointment_datetime_3, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'appointment_datetime_3 must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        appointment_datetime_3)
                )
        validated_params['appointment_datetime_3'] = validated_appointment_datetime_3


def validate_phone_number(phone_number, rqst_errors):
    if not re.findall(r'^1?\d{10}$', phone_number):
        rqst_errors.append("{} must be a valid phone number".format(phone_number))


def validate_params_for_update_row(rqst_body, validated_params, rqst_errors):
    if 'company_name' in rqst_body:
        validated_params['company_name'] = clean_string_value_from_dict_object(rqst_body, "root", "company_name", rqst_errors)

    if "address_line_1" in rqst_body:
        address_line_1 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_1",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["address_line_1"] = address_line_1

    if "address_line_2" in rqst_body:
        address_line_2 = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "address_line_2",
            rqst_errors,
            empty_string_allowed=True
        )
        if address_line_2 is None:
            address_line_2 = ''
        validated_params["address_line_2"] = address_line_2

    if "city" in rqst_body:
        city = clean_string_value_from_dict_object(rqst_body, "root", "city", rqst_errors, empty_string_allowed=True)
        validated_params["city"] = city

    if "state_province" in rqst_body:
        state_province = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "state_province",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["state_province"] = state_province

    if "zipcode" in rqst_body:
        zipcode = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "zipcode",
            rqst_errors,
            empty_string_allowed=True
        )
        validated_params["zipcode"] = zipcode

    if "estimated_monthly_caseload" in rqst_body:
        estimated_monthly_caseload = clean_int_value_from_dict_object(
            rqst_body,
            'root',
            "estimated_monthly_caseload",
            rqst_errors
        )
        if estimated_monthly_caseload:
            validator = MinValueValidator(0)
            try:
                validator(estimated_monthly_caseload)
            except ValidationError:
                rqst_errors.append(
                    "estimated_monthly_caseload must be more than 0. Value is : {}".format(estimated_monthly_caseload)
                )
        validated_params["estimated_monthly_caseload"] = estimated_monthly_caseload

    if "contact_first_name" in rqst_body:
        contact_first_name = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "contact_first_name",
            rqst_errors
        )
        validated_params["contact_first_name"] = contact_first_name

    if "contact_last_name" in rqst_body:
        contact_last_name = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "contact_last_name",
            rqst_errors
        )
        validated_params["contact_last_name"] = contact_last_name

    if "contact_email" in rqst_body:
        contact_email = clean_string_value_from_dict_object(rqst_body, "root", "contact_email", rqst_errors)
        if contact_email is not None:
            try:
                validate_email(contact_email)
            except forms.ValidationError:
                rqst_errors.append("contact_email must be a valid email address. Value is : {}".format(contact_email))
                contact_email = None
        validated_params['contact_email'] = contact_email

    if "contact_phone" in rqst_body:
        contact_phone = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "contact_phone",
            rqst_errors
        )
        if contact_phone:
            validate_phone_number(contact_phone, rqst_errors)
        validated_params["contact_phone"] = contact_phone

    if "appointment_datetime" in rqst_body:
        appointment_datetime = clean_string_value_from_dict_object(rqst_body, "root", "appointment_datetime", rqst_errors, none_allowed=True)
        validated_appointment_datetime = None
        if appointment_datetime:
            try:
                validated_appointment_datetime = datetime.datetime.strptime(appointment_datetime, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'appointment_datetime must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        appointment_datetime)
                )
        validated_params['appointment_datetime'] = validated_appointment_datetime

    if "appointment_datetime_2" in rqst_body:
        appointment_datetime_2 = clean_string_value_from_dict_object(rqst_body, "root", "appointment_datetime_2", rqst_errors, none_allowed=True)
        validated_appointment_datetime_2 = None
        if appointment_datetime_2:
            try:
                validated_appointment_datetime_2 = datetime.datetime.strptime(appointment_datetime_2, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'appointment_datetime_2 must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        appointment_datetime_2)
                )
        validated_params['appointment_datetime_2'] = validated_appointment_datetime_2

    if "appointment_datetime_3" in rqst_body:
        appointment_datetime_3 = clean_string_value_from_dict_object(rqst_body, "root", "appointment_datetime_3", rqst_errors, none_allowed=True)
        validated_appointment_datetime_3 = None
        if appointment_datetime_3:
            try:
                validated_appointment_datetime_3 = datetime.datetime.strptime(appointment_datetime_3, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
            except ValueError:
                rqst_errors.append(
                    'appointment_datetime_3 must be a properly formatted datetime string in UTC, eg. YYYY-MM-DDTHH:MM:SS. Value is : {}'.format(
                        appointment_datetime_3)
                )
        validated_params['appointment_datetime_3'] = validated_appointment_datetime_3
