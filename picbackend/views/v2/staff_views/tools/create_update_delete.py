"""
Defines utility functions and classes for staff views
"""

from ...utils import clean_string_value_from_dict_object
from ...utils import clean_int_value_from_dict_object
from ...utils import clean_list_value_from_dict_object
from picmodels.models import NavMetricsLocation
from django.core.validators import validate_email
from django import forms
from picmodels.services.staff_consumer_models_services.pic_staff_services import add_instance_using_validated_params
from picmodels.services.staff_consumer_models_services.pic_staff_services import modify_instance_using_validated_params
from picmodels.services.staff_consumer_models_services.pic_staff_services import delete_instance_using_validated_params


def validate_rqst_params_and_add_instance(post_data, post_errors):
    add_staff_params = get_staff_mgmt_put_params(post_data, post_errors)

    staff_instance = None
    if not post_errors:
        staff_instance = add_instance_using_validated_params(add_staff_params, post_errors)

    return staff_instance


def get_staff_mgmt_put_params(put_data, rqst_errors):
    rqst_usr_email = clean_string_value_from_dict_object(put_data, "root", "Email", rqst_errors)
    if rqst_usr_email and not rqst_errors:
        try:
            validate_email(rqst_usr_email)
        except forms.ValidationError:
            rqst_errors.append("{!s} must be a valid email address".format(rqst_usr_email))
    rqst_usr_mpn = clean_string_value_from_dict_object(put_data, "root", "MPN", rqst_errors, empty_string_allowed=True,
                                                       none_allowed=True)
    if rqst_usr_mpn is None:
        rqst_usr_mpn = ''
    rqst_usr_f_name = clean_string_value_from_dict_object(put_data, "root", "First Name", rqst_errors)
    rqst_usr_l_name = clean_string_value_from_dict_object(put_data, "root", "Last Name", rqst_errors)
    rqst_county = clean_string_value_from_dict_object(put_data, "root", "User County", rqst_errors)
    rqst_usr_type = clean_string_value_from_dict_object(put_data, "root", "User Type", rqst_errors)
    rqst_base_locations = clean_list_value_from_dict_object(put_data, "root", "Base Locations", rqst_errors,
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

    return {
        "rqst_usr_email": rqst_usr_email,
        "rqst_usr_mpn": rqst_usr_mpn,
        "rqst_usr_f_name": rqst_usr_f_name,
        "rqst_usr_l_name": rqst_usr_l_name,
        "rqst_county": rqst_county,
        "rqst_usr_type": rqst_usr_type,
        "base_location_objects": base_location_objects
    }


def validate_rqst_params_and_modify_instance(post_data, post_errors):
    modify_staff_params = get_staff_mgmt_put_params(post_data, post_errors)
    modify_staff_params['rqst_usr_id'] = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)

    staff_instance = None
    if not post_errors:
        staff_instance = modify_instance_using_validated_params(modify_staff_params, post_errors)

    return staff_instance


def validate_rqst_params_and_delete_instance(post_data, post_errors):
    rqst_usr_id = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)

    if not post_errors:
        delete_instance_using_validated_params(rqst_usr_id, post_errors)
