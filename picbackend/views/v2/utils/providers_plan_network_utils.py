"""
This module defines utility functions and classes for views that handle carriers, accepted plans, and hospital/provider
locations for provider networks contracted with PIC
"""

import json
from picmodels.models import HealthcareCarrier
from .base import clean_string_value_from_dict_object
from .base import clean_int_value_from_dict_object


def add_carrier(response_raw_data, rqst_carrier_info, post_errors):
    """
    This function takes dictionary populated with Healthcare carrier info, parses for errors, adds the carrier
    to the database if there are none, and adds the carrier info to given response data.

    :param response_raw_data: (type: dictionary) dictionary that contains response data
    :param rqst_carrier_info: (type: dictionary) dictionary that contains carrier info
    :param post_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary that contains response data
    """

    add_carrier_params = get_carrier_mgmt_put_params(rqst_carrier_info, post_errors)

    if len(post_errors) == 0:
        found_healthcare_carrier_objs = HealthcareCarrier.objects.filter(
            name=add_carrier_params['rqst_carrier_name'])

        if found_healthcare_carrier_objs:
            carrier_ids = []
            for healthcare_carrier_obj in found_healthcare_carrier_objs:
                carrier_ids.append(healthcare_carrier_obj.id)

            if len(found_healthcare_carrier_objs) > 1:
                post_errors.append("Multiple healthcare carriers with name {} already exist in db. (Hint - Delete one) id's: {}".format(
                    add_carrier_params['rqst_carrier_name'], json.dumps(carrier_ids)))
            else:
                post_errors.append("Healthcare carrier with name {} already exists in db. id: {}".format(
                    add_carrier_params['rqst_carrier_name'], carrier_ids[0]))
        else:
            healthcare_carrier_obj = HealthcareCarrier()
            healthcare_carrier_obj.name = add_carrier_params['rqst_carrier_name']
            healthcare_carrier_obj.save()

            response_raw_data['Data']["Database ID"] = healthcare_carrier_obj.id

    return response_raw_data


def modify_carrier(response_raw_data, rqst_carrier_info, post_errors):
    modify_carrier_params = get_carrier_mgmt_put_params(rqst_carrier_info, post_errors)
    rqst_carrier_id = clean_int_value_from_dict_object(rqst_carrier_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            healthcare_carrier_obj = HealthcareCarrier.objects.get(id=rqst_carrier_id)
        except HealthcareCarrier.DoesNotExist:
            post_errors.append("Healthcare carrier does not exist for database id: {}".format(rqst_carrier_id))

    return response_raw_data


def delete_carrier(response_raw_data, rqst_carrier_info, post_errors):
    rqst_carrier_id = clean_int_value_from_dict_object(rqst_carrier_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            healthcare_carrier_obj = HealthcareCarrier.objects.get(id=rqst_carrier_id)
            healthcare_carrier_obj.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except HealthcareCarrier.DoesNotExist:
            post_errors.append("Healthcare carrier does not exist for database id: {}".format(rqst_carrier_id))

    return response_raw_data


def get_carrier_mgmt_put_params(rqst_carrier_info, post_errors):
    """
    This function parses the BODY of requests for PIC consumer management PUT requests, checks for errors, and returns
    relevant information as a dictionary

    :param rqst_carrier_info: (type: dictionary) Carrier information to be parsed
    :param post_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary with relevant consumer information
    """

    rqst_carrier_name = clean_string_value_from_dict_object(rqst_carrier_info, "root", "name", post_errors)

    return {"rqst_carrier_name": rqst_carrier_name,}
