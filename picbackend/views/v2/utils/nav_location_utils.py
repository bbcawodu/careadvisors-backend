"""
Defines utility functions and classes for navigator location views
"""


from django.db import IntegrityError
from .base import clean_string_value_from_dict_object
from .base import clean_int_value_from_dict_object
from .base import clean_bool_value_from_dict_object
from picmodels.models import NavMetricsLocation
from picmodels.models import Address
from picmodels.models import Country
import json


def add_nav_hub_location(response_raw_data, post_data, post_errors):
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

    if len(post_errors) == 0:
        address_instance, address_instance_created = Address.objects.get_or_create(address_line_1=rqst_address_line_1,
                                                                                   address_line_2=rqst_address_line_2,
                                                                                   city=rqst_city,
                                                                                   state_province=rqst_state,
                                                                                   zipcode=rqst_zipcode,
                                                                                   country=Country.objects.get(name=rqst_country))

        try:
            location_instance = NavMetricsLocation.objects.get(name=rqst_location_name, address=address_instance)
            post_errors.append('Nav Hub Location database entry already exists for the name: {!s}'.format(rqst_location_name))
        except NavMetricsLocation.DoesNotExist:
            try:
                location_instance = NavMetricsLocation(name=rqst_location_name, address=address_instance, cps_location=rqst_cps_location)
                location_instance.save()
            except IntegrityError:
                location_instance = NavMetricsLocation.objects.get(address=address_instance)
                post_errors.append('Nav Hub Location database entry already exists for the address: {!s}'.format(json.dumps(location_instance.return_values_dict())))

        response_raw_data['Data'] = {"Database ID": location_instance.id}

    return response_raw_data


def modify_nav_hub_location(response_raw_data, post_data, post_errors):
    # rqst_location_id = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)
    rqst_location_name = clean_string_value_from_dict_object(post_data, "root", "Location Name", post_errors)
    rqst_address_line_1 = clean_string_value_from_dict_object(post_data, "root", "Address Line 1", post_errors)
    rqst_address_line_2 = clean_string_value_from_dict_object(post_data, "root", "Address Line 2", post_errors, empty_string_allowed=True)
    if rqst_address_line_2 is None:
        rqst_address_line_2 = ''
    rqst_city = clean_string_value_from_dict_object(post_data, "root", "City", post_errors)
    rqst_state = clean_string_value_from_dict_object(post_data, "root", "State", post_errors)
    rqst_zipcode = clean_string_value_from_dict_object(post_data, "root", "Zipcode", post_errors)
    rqst_country = clean_string_value_from_dict_object(post_data, "root", "Country", post_errors)
    rqst_location_id = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)

    rqst_cps_location = clean_bool_value_from_dict_object(post_data, "root", "cps_location", post_errors,
                                                          no_key_allowed=True)
    if not rqst_cps_location:
        rqst_cps_location = False

    if len(post_errors) == 0:
        address_instance, address_instance_created = Address.objects.get_or_create(address_line_1=rqst_address_line_1,
                                                                                   address_line_2=rqst_address_line_2,
                                                                                   city=rqst_city,
                                                                                   state_province=rqst_state,
                                                                                   zipcode=rqst_zipcode,
                                                                                   country=Country.objects.get(name=rqst_country))
        try:
            location_instance = NavMetricsLocation.objects.get(id=rqst_location_id)
            location_instance.name = rqst_location_name
            location_instance.cps_location = rqst_cps_location
            location_instance.address = address_instance
            location_instance.save()
            response_raw_data['Data'] = {"Database ID": location_instance.id}
        except NavMetricsLocation.DoesNotExist:
            post_errors.append('Nav Hub Location database entry does not exist for the name: {!s}'.format(str(rqst_location_name)))
        except NavMetricsLocation.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the name: {!s}'.format(str(rqst_location_name)))
        except IntegrityError:
            post_errors.append('Database entry already exists for the name: {!s}'.format(rqst_location_name))

    return response_raw_data


def delete_nav_hub_location(response_raw_data, post_data, post_errors):
    rqst_location_id = clean_int_value_from_dict_object(post_data, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            location_instance = NavMetricsLocation.objects.get(id=rqst_location_id)
            location_instance.delete()
            response_raw_data['Data'] = {"Database ID": "Deleted"}
        except NavMetricsLocation.DoesNotExist:
            post_errors.append('Location database entry does not exist for the id: {!s}'.format(str(rqst_location_id)))
        except NavMetricsLocation.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_location_id)))

    return response_raw_data
