"""
This module defines utility functions and classes for views that handle carriers for provider networks contracted with
PIC
"""

import json
from picmodels.models import HealthcareCarrier
from picbackend.views.v2.utils import clean_string_value_from_dict_object
from picbackend.views.v2.utils import clean_int_value_from_dict_object


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
        found_healthcare_carrier_objs = check_for_healthcare_carrier_objs_with_given_name(
            add_carrier_params['rqst_carrier_name'], post_errors)

        if not found_healthcare_carrier_objs and len(post_errors) == 0:
            healthcare_carrier_obj = HealthcareCarrier()
            healthcare_carrier_obj.name = add_carrier_params['rqst_carrier_name']
            healthcare_carrier_obj.save()

            response_raw_data['Data']["Database ID"] = healthcare_carrier_obj.id

    return response_raw_data


def modify_carrier(response_raw_data, rqst_carrier_info, post_errors):
    modify_carrier_params = get_carrier_mgmt_put_params(rqst_carrier_info, post_errors)
    rqst_carrier_id = clean_int_value_from_dict_object(rqst_carrier_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        found_healthcare_carrier_objs = check_for_healthcare_carrier_objs_with_given_name(
            modify_carrier_params['rqst_carrier_name'], post_errors)

        if not found_healthcare_carrier_objs and len(post_errors) == 0:
            try:
                healthcare_carrier_obj = HealthcareCarrier.objects.get(id=rqst_carrier_id)
                healthcare_carrier_obj.name = modify_carrier_params['rqst_carrier_name']
                healthcare_carrier_obj.save()

                response_raw_data['Data']["Database ID"] = healthcare_carrier_obj.id
            except HealthcareCarrier.DoesNotExist:
                post_errors.append("Healthcare carrier does not exist for database id: {}".format(rqst_carrier_id))

    return response_raw_data


def check_for_healthcare_carrier_objs_with_given_name(carrier_name, post_errors):
    found_healthcare_carrier_obj = False

    healthcare_carrier_objs = HealthcareCarrier.objects.filter(name=carrier_name)

    if healthcare_carrier_objs:
        found_healthcare_carrier_obj = True

        carrier_ids = []
        for carrier_obj in healthcare_carrier_objs:
            carrier_ids.append(carrier_obj.id)

        if len(healthcare_carrier_objs) > 1:
            post_errors.append(
                "Multiple healthcare carriers with name {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    carrier_name, json.dumps(carrier_ids)))
        else:
            post_errors.append(
                "Healthcare carrier with name {} already exists in db. (Hint - Modify that entry) id: {}".format(
                    carrier_name, carrier_ids[0]))

    return found_healthcare_carrier_obj


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


def retrieve_id_carriers(response_raw_data, rqst_errors, carriers, rqst_carrier_id, list_of_ids):
    """
    This function takes a list of ids and a QueryList of HealthcareCarrier instances as parameters,
    filters the database with the parameters, and adds the carrier info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param carriers: (type: QueryList) QueryList of carriers
    :param rqst_carrier_id: (type: integer) carrier id
    :param list_of_ids: (type: list) list of carrier ids
    :return: (type: dictionary and list) response data and list of error messages
    """

    if rqst_carrier_id == "all":
        all_carriers = carriers
        carrier_dict = {}
        for carrier in all_carriers:
            carrier_dict[carrier.id] = carrier.return_values_dict()
        carrier_list = []
        for carrier_key, carrier_entry in carrier_dict.items():
            carrier_list.append(carrier_entry)

        response_raw_data["Data"] = carrier_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            carriers = carriers.filter(id__in=list_of_ids)
            if len(carriers) > 0:

                carrier_dict = {}
                for carrier in carriers:
                    carrier_dict[carrier.id] = carrier.return_values_dict()
                carrier_list = []
                for carrier_key, carrier_entry in carrier_dict.items():
                    carrier_list.append(carrier_entry)
                response_raw_data["Data"] = carrier_list

                for carrier_id in list_of_ids:
                    if carrier_id not in carrier_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Carrier with id: {!s} not found in database'.format(str(carrier_id)))
            else:
                rqst_errors.append('No carriers found for database ID(s): ' + rqst_carrier_id)
        else:
            rqst_errors.append('No valid carrier IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_name_carriers(response_raw_data, rqst_errors, carriers, rqst_name):
    """
    This function takes a carrier name and a QueryList of HealthcareCarrier instances as parameters,
    filters the database with the parameters, and adds the carrier info the given dictionary of response data

    :param response_raw_data: (type: dictionary) response data
    :param rqst_errors: (type: list) list of error messages
    :param carriers: (type: QueryList) QueryList of consumers
    :param rqst_name: (type: string) consumer last name
    :return: (type: dictionary and list) response data and list of error messages
    """

    carrier_list = []
    carriers = carriers.filter(name__iexact=rqst_name)

    if carriers:
        if len(carriers) > 1:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Multiple carriers found in db for name: {!s}'.format(rqst_name))

        for carrier in carriers:
            carrier_list.append(carrier.return_values_dict())
        response_raw_data["Data"] = carrier_list
    else:
        rqst_errors.append('Carrier with name: {!s} not found in database'.format(rqst_name))

    return response_raw_data, rqst_errors


# def retrieve_name_carriers(response_raw_data, rqst_errors, carriers, rqst_name, list_of_names):
#     """
#     This function takes a carrier name and a QueryList of HealthcareCarrier instances as parameters,
#     filters the database with the parameters, and adds the carrier info the given dictionary of response data
#
#     :param response_raw_data: (type: dictionary) response data
#     :param rqst_errors: (type: list) list of error messages
#     :param carriers: (type: QueryList) QueryList of consumers
#     :param rqst_name: (type: string) consumer last name
#     :return: (type: dictionary and list) response data and list of error messages
#     """
#
#     carrier_list = []
#     carriers = carriers.filter(name__iexact=rqst_name)
#
#     if carriers:
#         if len(carriers) > 1:
#             if response_raw_data['Status']['Error Code'] != 2:
#                 response_raw_data['Status']['Error Code'] = 2
#             rqst_errors.append('Multiple carriers found in db for name: {!s}'.format(rqst_name))
#
#         for carrier in carriers:
#             carrier_list.append(carrier.return_values_dict())
#         response_raw_data["Data"] = carrier_list
#     else:
#         rqst_errors.append('Carrier with name: {!s} not found in database'.format(rqst_name))
#
#     return response_raw_data, rqst_errors
