"""
Defines utility functions and classes for staff views
"""

from django import forms
from django.core.validators import validate_email
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

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

    validate_nav_signup_params(rqst_body, validated_params, rqst_errors)


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

    validate_nav_signup_params(rqst_body, validated_params, rqst_errors)


def validate_nav_signup_params(rqst_body, validated_params, rqst_errors):
    if 'add_healthcare_locations_worked' in rqst_body:
        add_healthcare_locations_worked = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_healthcare_locations_worked",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_location_info = []
        for location_dict in add_healthcare_locations_worked:
            if not isinstance(location_dict, dict):
                rqst_errors.append('Error: A location object in \'add_healthcare_locations_worked\' is not a object.')
            else:
                location_info = {
                    "name": clean_string_value_from_dict_object(
                        location_dict,
                        "add_location_object",
                        'name',
                        rqst_errors
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        location_dict,
                        "add_location_object",
                        'state_province',
                        rqst_errors,
                        none_allowed=True
                    )
                }
                if not location_info['state_province']:
                    location_info['state_province'] = 'not available'

                validated_location_info.append(location_info)

        validated_params['add_healthcare_locations_worked'] = validated_location_info
    elif 'remove_healthcare_locations_worked' in rqst_body:
        remove_healthcare_locations_worked = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_healthcare_locations_worked",
            rqst_errors
        )

        validated_location_info = []
        for location_dict in remove_healthcare_locations_worked:
            if not isinstance(location_dict, dict):
                rqst_errors.append('Error: A location object in \'remove_healthcare_locations_worked\' is not a object.')
            else:
                location_info = {
                    "name": clean_string_value_from_dict_object(
                        location_dict,
                        "remove_location_object",
                        'name',
                        rqst_errors
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        location_dict,
                        "remove_location_object",
                        'state_province',
                        rqst_errors,
                        none_allowed=True
                    )
                }
                if not location_info['state_province']:
                    location_info['state_province'] = 'not available'

                validated_location_info.append(location_info)

        validated_params['remove_healthcare_locations_worked'] = validated_location_info

    if 'add_healthcare_service_expertises' in rqst_body:
        add_healthcare_service_expertises = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_healthcare_service_expertises",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_service_expertise_info = []
        for service_expertise in add_healthcare_service_expertises:
            if not isinstance(service_expertise, str):
                rqst_errors.append('Error: A service_expertise in \'add_healthcare_service_expertises\' is not a string.')
                continue

            validated_service_expertise_info.append(service_expertise)

        validated_params['add_healthcare_service_expertises'] = validated_service_expertise_info
    elif 'remove_healthcare_service_expertises' in rqst_body:
        remove_healthcare_service_expertises = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_healthcare_service_expertises",
            rqst_errors
        )

        validated_service_expertise_info = []
        for service_expertise in remove_healthcare_service_expertises:
            if not isinstance(service_expertise, str):
                rqst_errors.append('Error: A service_expertise in \'remove_healthcare_service_expertises\' is not a string.')
                continue

            validated_service_expertise_info.append(service_expertise)

        validated_params['remove_healthcare_service_expertises'] = validated_service_expertise_info

    if 'add_insurance_carrier_specialties' in rqst_body:
        add_insurance_carrier_specialties = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_insurance_carrier_specialties",
            rqst_errors,
            empty_list_allowed=True
        )

        validated_insurance_carrier_info = []
        for carrier_dict in add_insurance_carrier_specialties:
            if not isinstance(carrier_dict, dict):
                rqst_errors.append('Error: An insurance_carrier object in \'add_insurance_carrier_specialties\' is not a object.')
            else:
                validated_carrier_info = {
                    "name": clean_string_value_from_dict_object(
                        carrier_dict,
                        "insurance_carrier_object",
                        'name',
                        rqst_errors,
                        empty_string_allowed=True
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        carrier_dict,
                        "insurance_carrier_object",
                        'state_province',
                        rqst_errors,
                        empty_string_allowed=True
                    )
                }
                if not validated_carrier_info['state_province']:
                    validated_carrier_info['state_province'] = 'not available'

                validated_insurance_carrier_info.append(validated_carrier_info)

        validated_params['add_insurance_carrier_specialties'] = validated_insurance_carrier_info
    elif 'remove_insurance_carrier_specialties' in rqst_body:
        remove_insurance_carrier_specialties = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_insurance_carrier_specialties",
            rqst_errors
        )

        validated_insurance_carrier_info = []
        for carrier_dict in remove_insurance_carrier_specialties:
            if not isinstance(carrier_dict, dict):
                rqst_errors.append('Error: An insurance_carrier object in \'remove_insurance_carrier_specialties\' is not a object.')
            else:
                validated_carrier_info = {
                    "name": clean_string_value_from_dict_object(
                        carrier_dict,
                        "insurance_carrier_object",
                        'name',
                        rqst_errors,
                        empty_string_allowed=True
                    ),
                    "state_province": clean_string_value_from_dict_object(
                        carrier_dict,
                        "insurance_carrier_object",
                        'state_province',
                        rqst_errors,
                        empty_string_allowed=True
                    )
                }
                if not validated_carrier_info['state_province']:
                    validated_carrier_info['state_province'] = 'not available'

                validated_insurance_carrier_info.append(validated_carrier_info)

        validated_params['remove_insurance_carrier_specialties'] = validated_insurance_carrier_info

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

    if "phone" in rqst_body:
        phone = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "phone",
            rqst_errors,
            none_allowed=True
        )

        validated_params["phone"] = phone

    if "reported_region" in rqst_body:
        reported_region = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "reported_region",
            rqst_errors,
            none_allowed=True
        )

        validated_params["reported_region"] = reported_region

    if "video_link" in rqst_body:
        video_link = clean_string_value_from_dict_object(
            rqst_body,
            "root",
            "video_link",
            rqst_errors,
            none_allowed=True
        )
        if video_link:
            validate = URLValidator()
            try:
                validate(video_link)
            except ValidationError:
                rqst_errors.append("'video_link' is not a valid url. value is: {}".format(video_link))

        validated_params["video_link"] = video_link
