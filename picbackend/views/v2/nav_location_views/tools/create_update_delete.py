"""
Defines utility functions and classes for navigator location views
"""


from picbackend.views.utils import clean_bool_value_from_dict_object
from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object
from picmodels.models import Country


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
    rqst_location_name = clean_string_value_from_dict_object(rqst_body, "root", "Location Name", rqst_errors)
    rqst_address_line_1 = clean_string_value_from_dict_object(rqst_body, "root", "Address Line 1", rqst_errors)
    rqst_address_line_2 = clean_string_value_from_dict_object(rqst_body, "root", "Address Line 2", rqst_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_string_value_from_dict_object(rqst_body, "root", "City", rqst_errors)
    rqst_state = clean_string_value_from_dict_object(rqst_body, "root", "State", rqst_errors)
    rqst_zipcode = clean_string_value_from_dict_object(rqst_body, "root", "Zipcode", rqst_errors)
    rqst_cps_location = clean_bool_value_from_dict_object(rqst_body, "root", "cps_location", rqst_errors, no_key_allowed=True)
    if not rqst_cps_location:
        rqst_cps_location = False

    rqst_country = clean_string_value_from_dict_object(rqst_body, "root", "Country", rqst_errors)

    country_row = None
    if rqst_country:
        try:
            country_row = Country.objects.get(name__iexact=rqst_country)
        except Country.DoesNotExist:
            rqst_errors.append('Row does not exist in database for the country name: {!s}'.format(str(rqst_country)))

    validated_params["rqst_location_name"] = rqst_location_name
    validated_params["rqst_address_line_1"] = rqst_address_line_1
    validated_params["rqst_address_line_2"] = rqst_address_line_2
    validated_params["rqst_city"] = rqst_city
    validated_params["rqst_state"] = rqst_state
    validated_params["rqst_zipcode"] = rqst_zipcode
    validated_params["country_row"] = country_row
    validated_params["rqst_cps_location"] = rqst_cps_location


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "Location Name" in rqst_body:
        rqst_location_name = clean_string_value_from_dict_object(rqst_body, "root", "Location Name", rqst_errors)
        validated_params["rqst_location_name"] = rqst_location_name

    if "cps_location" in rqst_body:
        rqst_cps_location = clean_bool_value_from_dict_object(rqst_body, "root", "cps_location", rqst_errors, no_key_allowed=True)
        if not rqst_cps_location:
            rqst_cps_location = False
        validated_params["rqst_cps_location"] = rqst_cps_location

    rqst_address_line_1 = clean_string_value_from_dict_object(rqst_body, "root", "Address Line 1", rqst_errors)
    validated_params["rqst_address_line_1"] = rqst_address_line_1

    rqst_address_line_2 = clean_string_value_from_dict_object(rqst_body, "root", "Address Line 2", rqst_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    validated_params["rqst_address_line_2"] = rqst_address_line_2

    rqst_city = clean_string_value_from_dict_object(rqst_body, "root", "City", rqst_errors)
    validated_params["rqst_city"] = rqst_city

    rqst_state = clean_string_value_from_dict_object(rqst_body, "root", "State", rqst_errors)
    validated_params["rqst_state"] = rqst_state

    rqst_zipcode = clean_string_value_from_dict_object(rqst_body, "root", "Zipcode", rqst_errors)
    validated_params["rqst_zipcode"] = rqst_zipcode

    rqst_country = clean_string_value_from_dict_object(rqst_body, "root", "Country", rqst_errors)
    country_row = None
    if rqst_country:
        try:
            country_row = Country.objects.get(name__iexact=rqst_country)
        except Country.DoesNotExist:
            rqst_errors.append('Row does not exist in database for the country name: {!s}'.format(str(rqst_country)))
    validated_params["country_row"] = country_row
