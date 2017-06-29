"""
Defines utility functions and classes for navigator location views
"""


from ...utils import clean_string_value_from_dict_object
from ...utils import clean_int_value_from_dict_object
from ...utils import clean_bool_value_from_dict_object
from picmodels.services.nav_metrics_location_services import add_instance_using_validated_params
from picmodels.services.nav_metrics_location_services import modify_instance_using_validated_params
from picmodels.services.nav_metrics_location_services import delete_instance_using_validated_params


def validate_rqst_params_and_add_instance(post_data, post_errors):
    validated_rqst_params = validate_rqst_params(post_data, post_errors)

    location_instance = None
    if not post_errors:
        location_instance = add_instance_using_validated_params(validated_rqst_params, post_errors)

    return location_instance


def validate_rqst_params(post_data, post_errors):
    rqst_location_name = clean_string_value_from_dict_object(post_data, "root", "Location Name", post_errors)
    rqst_address_line_1 = clean_string_value_from_dict_object(post_data, "root", "Address Line 1", post_errors)
    rqst_address_line_2 = clean_string_value_from_dict_object(post_data, "root", "Address Line 2", post_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_string_value_from_dict_object(post_data, "root", "City", post_errors)
    rqst_state = clean_string_value_from_dict_object(post_data, "root", "State", post_errors)
    rqst_zipcode = clean_string_value_from_dict_object(post_data, "root", "Zipcode", post_errors)
    rqst_country = clean_string_value_from_dict_object(post_data, "root", "Country", post_errors)
    rqst_cps_location = clean_bool_value_from_dict_object(post_data, "root", "cps_location", post_errors, no_key_allowed=True)
    if not rqst_cps_location:
        rqst_cps_location = False

    return {
        "rqst_location_name": rqst_location_name,
        "rqst_address_line_1": rqst_address_line_1,
        "rqst_address_line_2": rqst_address_line_2,
        "rqst_city": rqst_city,
        "rqst_state": rqst_state,
        "rqst_zipcode": rqst_zipcode,
        "rqst_country": rqst_country,
        "rqst_cps_location": rqst_cps_location
    }


def validate_rqst_params_and_modify_instance(post_data, post_errors):
    validated_rqst_params = validate_rqst_params(post_data, post_errors)
    rqst_location_id = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)

    location_instance = None
    if not post_errors:
        location_instance = modify_instance_using_validated_params(rqst_location_id, validated_rqst_params, post_errors)

    return location_instance


def validate_rqst_params_and_delete_instance(post_data, post_errors):
    rqst_location_id = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)

    if not post_errors:
        delete_instance_using_validated_params(rqst_location_id, post_errors)
