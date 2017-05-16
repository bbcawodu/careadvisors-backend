"""
This module defines utility functions and classes for views that handle carriers for provider networks contracted with
PIC
"""

import json
from picmodels.models import HealthcareCarrier
from ..base import clean_string_value_from_dict_object
from ..base import clean_int_value_from_dict_object


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
        found_healthcare_carrier_objs = check_for_healthcare_carrier_objs_with_given_name_and_state(
            add_carrier_params['rqst_carrier_name'], add_carrier_params['rqst_carrier_state'],  post_errors)

        if not found_healthcare_carrier_objs and len(post_errors) == 0:
            healthcare_carrier_obj = create_new_carrier_obj(add_carrier_params, post_errors)

            if len(post_errors) == 0:
                healthcare_carrier_obj.save()
                response_raw_data['Data']["Database ID"] = healthcare_carrier_obj.id

    return response_raw_data


def create_new_carrier_obj(carrier_params, post_errors):
    healthcare_carrier_obj = HealthcareCarrier()
    healthcare_carrier_obj.name = carrier_params['rqst_carrier_name']
    healthcare_carrier_obj.state_province = carrier_params['rqst_carrier_state']
    if not healthcare_carrier_obj.check_state_choices():
        post_errors.append(
            "State: {!s} is not a valid state abbreviation".format(healthcare_carrier_obj.state_province))

    return healthcare_carrier_obj


def modify_carrier(response_raw_data, rqst_carrier_info, post_errors):
    modify_carrier_params = get_carrier_mgmt_put_params(rqst_carrier_info, post_errors)
    rqst_carrier_id = clean_int_value_from_dict_object(rqst_carrier_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        found_healthcare_carrier_objs = check_for_healthcare_carrier_objs_with_given_name_and_state(
            modify_carrier_params['rqst_carrier_name'], modify_carrier_params['rqst_carrier_state'], post_errors, rqst_carrier_id)

        if not found_healthcare_carrier_objs and len(post_errors) == 0:
            healthcare_carrier_obj = modify_carrier_obj(modify_carrier_params, rqst_carrier_id, post_errors)

            if len(post_errors) == 0:
                healthcare_carrier_obj.save()
                response_raw_data['Data']["Database ID"] = healthcare_carrier_obj.id

    return response_raw_data


def modify_carrier_obj(carrier_params, rqst_carrier_id, post_errors):
    healthcare_carrier_obj = None
    try:
        healthcare_carrier_obj = HealthcareCarrier.objects.get(id=rqst_carrier_id)
        healthcare_carrier_obj.name = carrier_params['rqst_carrier_name']
        healthcare_carrier_obj.state_province = carrier_params['rqst_carrier_state']
        if not healthcare_carrier_obj.check_state_choices():
            post_errors.append(
                "State: {!s} is not a valid state abbreviation".format(healthcare_carrier_obj.state_province))
    except HealthcareCarrier.DoesNotExist:
        post_errors.append("Healthcare carrier does not exist for database id: {}".format(rqst_carrier_id))

    return healthcare_carrier_obj


def check_for_healthcare_carrier_objs_with_given_name_and_state(carrier_name, carrier_state,  post_errors, current_carrier_id=None):
    found_healthcare_carrier_obj = False

    healthcare_carrier_objs = HealthcareCarrier.objects.filter(name__iexact=carrier_name,
                                                               state_province__iexact=carrier_state)

    if healthcare_carrier_objs:
        found_healthcare_carrier_obj = True

        carrier_ids = []
        for carrier_obj in healthcare_carrier_objs:
            carrier_ids.append(carrier_obj.id)

        if healthcare_carrier_objs.count() > 1:
            post_errors.append(
                "Multiple healthcare carriers with name: {} and state: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    carrier_name, carrier_state, json.dumps(carrier_ids)))
        else:
            if not current_carrier_id or current_carrier_id not in carrier_ids:
                post_errors.append(
                    "Healthcare carrier with name: {} and state: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        carrier_name, carrier_state, carrier_ids[0]))
            else:
                found_healthcare_carrier_obj = False

    return found_healthcare_carrier_obj


def get_carrier_mgmt_put_params(rqst_carrier_info, post_errors):
    rqst_carrier_name = clean_string_value_from_dict_object(rqst_carrier_info, "root", "name", post_errors)
    rqst_carrier_state = clean_string_value_from_dict_object(rqst_carrier_info, "root", "state_province", post_errors)

    return {"rqst_carrier_name": rqst_carrier_name,
            "rqst_carrier_state": rqst_carrier_state}


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


def retrieve_state_carriers(response_raw_data, rqst_errors, carriers, rqst_state, list_of_states):
    carrier_dict = {}
    for state in list_of_states:
        name_carriers = carriers.filter(state_province__iexact=state)
        for carrier in name_carriers:
            if state not in carrier_dict:
                carrier_dict[state] = [carrier.return_values_dict()]
            else:
                carrier_dict[state].append(carrier.return_values_dict())
    if len(carrier_dict) > 0:
        carrier_list = []
        for carrier_key, carrier_entry in carrier_dict.items():
            carrier_list.append(carrier_entry)
        response_raw_data["Data"] = carrier_list
        for state in list_of_states:
            if state not in carrier_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Carriers in the state: {!s} not found in database'.format(state))
    else:
        rqst_errors.append('Carriers in the state(s): {!s} not found in database'.format(rqst_state))

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
