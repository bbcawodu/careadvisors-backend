"""
This module defines utility functions that are used throughout the project
"""

import sys
import urllib
import re
import datetime


def clean_string_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, empty_string_allowed=False,
                                        none_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the string value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get string from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param empty_string_allowed: (type: boolean) whether an empty string allowed for given key, default is False
    :param none_allowed: (type: boolean) whether Null values are allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: string or None) String type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] == "" and empty_string_allowed is False:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty string".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and none_allowed is False:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not none_allowed and not isinstance(dict_object[dict_key], str):
        post_errors.append("Value for {!r} in {!r} dictionary is not a string".format(dict_key, dict_name))
    else:
        if dict_object[dict_key] or dict_object[dict_key] == "":
            return str(dict_object[dict_key])
        else:
            return None


def clean_int_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the integer value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get integer from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: integer or None) Integer type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], int):
        post_errors.append("Value for {!r} in {!r} dictionary is not an integer".format(dict_key, dict_name))
    else:
        return int(dict_object[dict_key])


def clean_dict_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, none_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the dictionary value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get dictionary from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param none_allowed: (type: boolean) whether Null values are allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: dictionary or None) dictionary type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and none_allowed == False:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not none_allowed and not isinstance(dict_object[dict_key], dict):
        post_errors.append("Value for {!r} in {!r} dictionary is not a dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] == {}:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty dictionary".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]
    return None


def clean_list_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, empty_list_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the list value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get list from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param empty_list_allowed: (type: boolean) whether an empty list is allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: list or None) list type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], list):
        post_errors.append("Value for {!r} in {!r} dictionary is not a list".format(dict_key, dict_name))
    elif dict_object[dict_key] == []:
        if empty_list_allowed:
            return []
        else:
            post_errors.append("Value for {!r} in {!r} dictionary is an empty list".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]
    return None


def clean_bool_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the boolean value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get boolean from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: boolean or None) boolean type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], bool):
        post_errors.append("Value for {!r} in {!r} dictionary is not type boolean".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]


def build_search_params(rqst_params, rqst_errors):
    """
    This function takes a Django request.Get object, and parses it for any paramaters relevant to the PIC
    API

    :param rqst_params: (type: Django QueryDict object) dictionary like object that represents request GET parameters
    :param rqst_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary populated with key value paramaters from GET request
    """

    search_params = {}
    if 'location' in rqst_params:
        search_params['location'] = urllib.parse.unquote(rqst_params['location'])
    if 'fields' in rqst_params:
        search_params['fields'] = urllib.parse.unquote(rqst_params['fields'])
        search_params['fields list'] = re.findall(r"[@\w. '-]+", search_params['fields'])
    if 'fname' in rqst_params:
        search_params['first name'] = rqst_params['fname']
        search_params['first name list'] = re.findall(r"[\w. '-]+", search_params['first name'])
    if 'lname' in rqst_params:
        search_params['last name'] = rqst_params['lname']
        search_params['last name list'] = re.findall(r"[\w. '-]+", search_params['last name'])
    if 'email' in rqst_params:
        search_params['email'] = rqst_params['email']
        search_params['email list'] = re.findall(r"[@\w. '-]+", search_params['email'])
    if 'mpn' in rqst_params:
        search_params['mpn'] = rqst_params['mpn']
        search_params['mpn list'] = re.findall(r"[@\w. '-]+", search_params['mpn'])
    if 'region' in rqst_params:
        search_params['region'] = rqst_params['region']
        search_params['region list'] = re.findall(r"[@\w. '-]+", search_params['region'])
    if 'id' in rqst_params:
        search_params['id'] = rqst_params['id']
        if search_params['id'] != "all":
            list_of_ids = re.findall("\d+", search_params['id'])
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            search_params['id list'] = list_of_ids

            if not search_params['id list']:
                rqst_errors.append('Invalid id, ids must be base 10 integers')
    if 'partnerid' in rqst_params:
        search_params['partnerid'] = rqst_params['partnerid']
        list_of_ids = re.findall("[@\w. '-_]+", search_params['partnerid'])
        search_params['partnerid list'] = list_of_ids
    if 'navid' in rqst_params:
        search_params['navigator id'] = rqst_params['navid']

        list_of_nav_ids = re.findall("\d+", search_params['navigator id'])
        for indx, element in enumerate(list_of_nav_ids):
            list_of_nav_ids[indx] = int(element)
        search_params['navigator id list'] = list_of_nav_ids

        if not search_params['navigator id list']:
            rqst_errors.append('Invalid navigator id, navigator ids must be base 10 integers')
    if 'location_id' in rqst_params:
        search_params['location_id'] = rqst_params['location_id']

        list_of_ids = re.findall("\d+", search_params['location_id'])
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        search_params['location_id list'] = list_of_ids

        if not search_params['location_id list']:
            rqst_errors.append('Invalid location_id, ids must be base 10 integers')
    if 'is_cps_consumer' in rqst_params:
        search_params['is_cps_consumer'] = rqst_params['is_cps_consumer'].lower()
        if search_params['is_cps_consumer'] not in ('true', 'false'):
            rqst_errors.append("Value for is_cps_consumer is not type boolean")
        else:
            search_params['is_cps_consumer'] = search_params['is_cps_consumer'] in ('true')
    if 'page' in rqst_params:
        search_params['page number'] = int(rqst_params['page'])
    if "county" in rqst_params:
        search_params['county'] = rqst_params['county']
        search_params['county list'] = re.findall(r"[\w. '-]+", search_params['county'])
    if "zipcode" in rqst_params:
        search_params['zipcode'] = rqst_params['zipcode']
        search_params['zipcode list'] = re.findall(r"\d+", search_params['zipcode'])

        if not search_params['zipcode list']:
            rqst_errors.append('Invalid zipcode, zipcodes must be integers')
    if "time" in rqst_params:
        try:
            search_params['look up date'] = datetime.date.today() - datetime.timedelta(days=int(rqst_params['time']))
            search_params['time'] = rqst_params['time']
        except ValueError:
            rqst_errors.append('time parameter must be a valid integer. Metrics returned without time parameter.')
    if "startdate" in rqst_params:
        try:
            datetime.datetime.strptime(rqst_params["startdate"], '%Y-%m-%d')
            search_params['start date'] = rqst_params["startdate"]
        except ValueError:
            rqst_errors.append('startdate parameter must be a valid date. Metrics returned without startdate parameter.')
    if "enddate" in rqst_params:
        try:
            datetime.datetime.strptime(rqst_params["enddate"], '%Y-%m-%d')
            search_params['end date'] = rqst_params["enddate"]
        except ValueError:
            rqst_errors.append('enddate parameter must be a valid integer. Metrics returned without enddate parameter.')
    if "groupby" in rqst_params:
        search_params['group by'] = rqst_params['groupby']
    if 'nav_location_tags' in rqst_params:
        search_params['nav_location_tags'] = rqst_params['nav_location_tags']
        search_params['nav_location_tags list'] = re.findall(r"[@\w. '-]+", search_params['region'])
    if 'intent' in rqst_params:
        search_params['intent'] = urllib.parse.unquote(rqst_params['intent'])
    if 'name' in rqst_params:
        search_params['name'] = urllib.parse.unquote(rqst_params['name'])
    if "state" in rqst_params:
        search_params['state'] = rqst_params['state']
        search_params['state list'] = re.findall(r"[\w. '-]+", search_params['state'])
    if 'carrier_id' in rqst_params:
        search_params['carrier id'] = rqst_params['carrier_id']

        list_of_carrier_ids = re.findall("\d+", search_params['carrier id'])
        for indx, element in enumerate(list_of_carrier_ids):
            list_of_carrier_ids[indx] = int(element)
        search_params['carrier id list'] = list_of_carrier_ids

        if not search_params['carrier id list']:
            rqst_errors.append('Invalid carrier id, carrier ids must be base 10 integers')
    if "carrier_state" in rqst_params:
        search_params['carrier state'] = rqst_params['carrier_state']
        search_params['carrier state list'] = re.findall(r"[\w. '-]+", search_params['carrier state'])
    if 'carrier_name' in rqst_params:
        search_params['carrier name'] = urllib.parse.unquote(rqst_params['carrier_name'])
    if 'accepted_location_id' in rqst_params:
        search_params['accepted_location_id'] = rqst_params['accepted_location_id']

        list_of_accepted_location_ids = re.findall("\d+", search_params['accepted_location_id'])
        for indx, element in enumerate(list_of_accepted_location_ids):
            list_of_accepted_location_ids[indx] = int(element)
        search_params['accepted_location_id_list'] = list_of_accepted_location_ids

        if not search_params['accepted_location_id_list']:
            rqst_errors.append('Invalid accepted_location id, accepted_location ids must be base 10 integers')
    if 'network_name' in rqst_params:
        search_params['network_name'] = urllib.parse.unquote(rqst_params['network_name'])
    if 'network_id' in rqst_params:
        search_params['network_id'] = rqst_params['network_id']

        list_of_network_ids = re.findall("\d+", search_params['network_id'])
        for indx, element in enumerate(list_of_network_ids):
            list_of_network_ids[indx] = int(element)
        search_params['network_id_list'] = list_of_network_ids

        if not search_params['network_id_list']:
            rqst_errors.append('Invalid network id, network ids must be base 10 integers')
    if 'is_cps_location' in rqst_params:
        search_params['is_cps_location'] = rqst_params['is_cps_location'].lower()
        if search_params['is_cps_location'] not in ('true', 'false'):
            rqst_errors.append("Value for is_cps_location is not type boolean")
        else:
            search_params['is_cps_location'] = search_params['is_cps_location'] in ('true')
    if 'question' in rqst_params:
        search_params['question'] = urllib.parse.unquote(rqst_params['question'])
    if 'gen_concern_name' in rqst_params:
        search_params['gen_concern_name'] = urllib.parse.unquote(rqst_params['gen_concern_name'])
    if 'gen_concern_id_subset' in rqst_params:
        search_params['gen_concern_id_subset'] = rqst_params['gen_concern_id_subset']

        list_of_gen_concern_ids = re.findall("\d+", search_params['gen_concern_id_subset'])
        for indx, element in enumerate(list_of_gen_concern_ids):
            list_of_gen_concern_ids[indx] = int(element)
        search_params['gen_concern_id_subset_list'] = list_of_gen_concern_ids

        if not search_params['gen_concern_id_subset_list']:
            rqst_errors.append('Invalid gen_concern id, gen_concern ids must be base 10 integers')
    if 'gen_concern_id' in rqst_params:
        search_params['gen_concern_id'] = rqst_params['gen_concern_id']

        list_of_gen_concern_ids = re.findall("\d+", search_params['gen_concern_id'])
        for indx, element in enumerate(list_of_gen_concern_ids):
            list_of_gen_concern_ids[indx] = int(element)
        search_params['gen_concern_id_list'] = list_of_gen_concern_ids

        if not search_params['gen_concern_id_list']:
            rqst_errors.append('Invalid gen_concern id, gen_concern ids must be base 10 integers')

    return search_params


def init_v2_response_data():
    """
    This function returns a skelleton dictionary that can be used for PIC JSON responses

    :return: (type: dictionary) dictionary that can be used in PIC JSON responses
    """
    return {'Status': {"Error Code": 0, "Warnings": [], "Version": 2.0, "Missing Parameters": []},
            'Data': {}}, []


def parse_and_log_errors(response_raw_data, errors_list):
    """
    This function takes a list of error messages, adds them to a PIC API response dictionary, and adds the
    correct error code

    :param response_raw_data: (type: dictionary) dictionary that can be used in PIC JSON responses
    :param errors_list: (type: list) list of error messages
    :return: (type: dictionary) dictionary that can be used in PIC JSON responses with errors logged
    """
    if len(errors_list) > 0:
        if response_raw_data["Status"]["Error Code"] == 0:
            response_raw_data["Status"]["Error Code"] = 1
        response_raw_data["Status"]["Errors"] = errors_list

        for message in errors_list:
            print(message)
            sys.stdout.flush()

    return response_raw_data
