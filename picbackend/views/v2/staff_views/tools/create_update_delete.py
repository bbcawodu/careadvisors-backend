"""
Defines utility functions and classes for staff views
"""

from ...utils import clean_string_value_from_dict_object
from ...utils import clean_int_value_from_dict_object
from ...utils import clean_list_value_from_dict_object
from picmodels.models import NavMetricsLocation
from picmodels.models import PICStaff
from django.db import IntegrityError
from django.core.validators import validate_email
from django import forms


def add_staff_using_api_rqst_params(response_raw_data, post_data, post_errors):
    add_staff_params = get_staff_mgmt_put_params(post_data, post_errors)

    if len(post_errors) == 0:
        user_instance = create_staff_obj(add_staff_params, post_errors)

        if len(post_errors) == 0:
            if user_instance:
                response_raw_data['Data'] = {"Database ID": user_instance.id}

    return response_raw_data


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


def create_staff_obj(staff_params, rqst_errors):
    user_instance = None

    rqst_usr_email = staff_params['rqst_usr_email']
    usr_rqst_values = {"first_name": staff_params['rqst_usr_f_name'],
                       "last_name": staff_params['rqst_usr_l_name'],
                       "type": staff_params['rqst_usr_type'],
                       "county": staff_params['rqst_county'],
                       "mpn": staff_params['rqst_usr_mpn']}
    user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
                                                                          defaults=usr_rqst_values)
    if not user_instance_created:
        rqst_errors.append('Staff database entry already exists for the email: {!s}'.format(rqst_usr_email))
    else:
        user_instance.base_locations = staff_params['base_location_objects']
        user_instance.save()

    return user_instance


def modify_staff_using_api_rqst_params(response_raw_data, post_data, post_errors):
    modify_staff_params = get_staff_mgmt_put_params(post_data, post_errors)
    modify_staff_params['rqst_usr_id'] = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        staff_instance = modify_staff_obj(modify_staff_params, post_errors)

        if len(post_errors) == 0 and staff_instance:
            response_raw_data['Data'] = {"Database ID": staff_instance.id}

    return response_raw_data


def modify_staff_obj(staff_params, rqst_errors):
    staff_instance = None

    rqst_usr_email = staff_params['rqst_usr_email']
    rqst_usr_id = staff_params['rqst_usr_id']
    try:
        staff_instance = PICStaff.objects.get(id=rqst_usr_id)
        staff_instance.first_name = staff_params['rqst_usr_f_name']
        staff_instance.last_name = staff_params['rqst_usr_l_name']
        staff_instance.type = staff_params['rqst_usr_type']
        staff_instance.county = staff_params['rqst_county']
        staff_instance.email = rqst_usr_email
        staff_instance.mpn = staff_params['rqst_usr_mpn']

        staff_instance.base_locations.clear()
        staff_instance.base_locations = staff_params['base_location_objects']

        staff_instance.save()
    except PICStaff.DoesNotExist:
        rqst_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
    except PICStaff.MultipleObjectsReturned:
        rqst_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
    except IntegrityError:
        rqst_errors.append('Database entry already exists for the email: {!s}'.format(rqst_usr_email))

    return staff_instance


def delete_staff_using_api_rqst_params(response_raw_data, post_data, post_errors):
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