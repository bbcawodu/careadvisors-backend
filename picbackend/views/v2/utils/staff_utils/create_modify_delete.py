"""
Defines utility functions and classes for staff views
"""

from ..base import clean_string_value_from_dict_object
from ..base import clean_int_value_from_dict_object
from ..base import clean_list_value_from_dict_object
from picmodels.models import NavMetricsLocation
from picmodels.models import PICStaff
from django.db import IntegrityError
from django.core.validators import validate_email
from django import forms


def add_staff(response_raw_data, post_data, post_errors):
    rqst_usr_email = clean_string_value_from_dict_object(post_data, "root", "Email", post_errors)
    if rqst_usr_email and not post_errors:
        try:
            validate_email(rqst_usr_email)
        except forms.ValidationError:
            post_errors.append("{!s} must be a valid email address".format(rqst_usr_email))
    rqst_usr_mpn = clean_string_value_from_dict_object(post_data, "root", "MPN", post_errors, empty_string_allowed=True, none_allowed=True)
    if rqst_usr_mpn is None:
        rqst_usr_mpn = ''
    rqst_usr_f_name = clean_string_value_from_dict_object(post_data, "root", "First Name", post_errors)
    rqst_usr_l_name = clean_string_value_from_dict_object(post_data, "root", "Last Name", post_errors)
    rqst_county = clean_string_value_from_dict_object(post_data, "root", "User County", post_errors)
    rqst_usr_type = clean_string_value_from_dict_object(post_data, "root", "User Type", post_errors)
    rqst_base_locations = clean_list_value_from_dict_object(post_data, "root", "Base Locations", post_errors, empty_list_allowed=True)
    rqst_base_locations = list(set(rqst_base_locations))
    base_location_objects = []
    location_errors = []
    if rqst_base_locations:
        for base_location_name in rqst_base_locations:
            try:
                base_location_object = NavMetricsLocation.objects.get(name=base_location_name)
                base_location_objects.append(base_location_object)
            except NavMetricsLocation.DoesNotExist:
                location_errors.append("No Nav Hub Location Database entry found for name: {!s}".format(base_location_name))
    for location_error in location_errors:
        post_errors.append(location_error)

    if len(post_errors) == 0:
        usr_rqst_values = {"first_name": rqst_usr_f_name,
                           "last_name": rqst_usr_l_name,
                           "type": rqst_usr_type,
                           "county": rqst_county,
                           "mpn": rqst_usr_mpn}
        user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
                                                                              defaults=usr_rqst_values)
        if not user_instance_created:
            post_errors.append('Staff database entry already exists for the email: {!s}'.format(rqst_usr_email))
        else:
            user_instance.base_locations = base_location_objects
            user_instance.save()
            response_raw_data['Data'] = {"Database ID": user_instance.id}

    return response_raw_data


def modify_staff(response_raw_data, post_data, post_errors):
    rqst_usr_id = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)
    rqst_usr_email = clean_string_value_from_dict_object(post_data, "root", "Email", post_errors)
    rqst_usr_mpn = clean_string_value_from_dict_object(post_data, "root", "MPN", post_errors, empty_string_allowed=True, none_allowed=True)
    if rqst_usr_mpn is None:
        rqst_usr_mpn = ''
    rqst_usr_f_name = clean_string_value_from_dict_object(post_data, "root", "First Name", post_errors)
    rqst_usr_l_name = clean_string_value_from_dict_object(post_data, "root", "Last Name", post_errors)
    rqst_county = clean_string_value_from_dict_object(post_data, "root", "User County", post_errors)
    rqst_usr_type = clean_string_value_from_dict_object(post_data, "root", "User Type", post_errors)
    rqst_base_locations = clean_list_value_from_dict_object(post_data, "root", "Base Locations", post_errors, empty_list_allowed=True)
    rqst_base_locations = list(set(rqst_base_locations))
    base_location_objects = []
    location_errors = []
    if rqst_base_locations:
        for base_location_name in rqst_base_locations:
            try:
                base_location_object = NavMetricsLocation.objects.get(name=base_location_name)
                base_location_objects.append(base_location_object)
            except NavMetricsLocation.DoesNotExist:
                location_errors.append("No Nav Hub Location Database entry found for name: {!s}".format(base_location_name))
    for location_error in location_errors:
        post_errors.append(location_error)

    if len(post_errors) == 0:
        try:
            staff_instance = PICStaff.objects.get(id=rqst_usr_id)
            staff_instance.first_name = rqst_usr_f_name
            staff_instance.last_name = rqst_usr_l_name
            staff_instance.type = rqst_usr_type
            staff_instance.county = rqst_county
            staff_instance.email = rqst_usr_email
            staff_instance.mpn = rqst_usr_mpn

            staff_instance.base_locations.clear()
            staff_instance.base_locations = base_location_objects

            staff_instance.save()
            response_raw_data['Data'] = {"Database ID": staff_instance.id}
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        except PICStaff.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
        except IntegrityError:
            post_errors.append('Database entry already exists for the email: {!s}'.format(rqst_usr_email))

    return response_raw_data


def delete_staff(response_raw_data, post_data, post_errors):
    rqst_usr_id = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            staff_instance = PICStaff.objects.get(id=rqst_usr_id)
            staff_instance.delete()
            response_raw_data['Data'] = {"Database ID": "Deleted"}
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        except PICStaff.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))

    return response_raw_data