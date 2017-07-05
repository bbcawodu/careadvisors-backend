"""
This module defines utility functions that are used throughout the project
"""

import sys
import urllib
import re
import datetime
from picmodels.models import HealthcarePlan


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
        return dict_object[dict_key]


def clean_int_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, none_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the integer value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get integer from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param none_allowed: (type: boolean) whether Null values are allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: integer or None) Integer type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and not none_allowed:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], int):
        post_errors.append("Value for {!r} in {!r} dictionary is not an integer".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]


def clean_float_value_from_dict_object(dict_object, dict_name, dict_key, post_errors, none_allowed=False, no_key_allowed=False):
    """
    This function takes a target dictionary and returns the float value given by the given key.
    Returns None if key if not found and appends any error messages to the post_errors list

    :param dict_object: (type: dictionary) target object to get integer from
    :param dict_name: (type: string) name of target dictionary
    :param dict_key: (type: string) target dictionary key
    :param post_errors: (type: list) list of error messages
    :param none_allowed: (type: boolean) whether Null values are allowed for given key, default is False
    :param no_key_allowed: (type: boolean) whether the or not to allow for absence of target key in target dictionary,
                           default is False
    :return: (type: float or None) Integer type value for given target key, or None
    """
    if dict_key not in dict_object:
        if no_key_allowed:
            return None
        else:
            post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and not none_allowed:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], float):
        post_errors.append("Value for {!r} in {!r} dictionary is not an float".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]


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


def validate_get_rqst_parameter_id(get_rqst_params, validated_params, rqst_errors):
    if 'id' in get_rqst_params:
        validated_params['id'] = get_rqst_params['id']
        if validated_params['id'] != "all":
            list_of_ids = re.findall("\d+", validated_params['id'])
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            validated_params['id list'] = list_of_ids

            if not validated_params['id list']:
                rqst_errors.append('Invalid id, ids must be base 10 integers')


def validate_get_rqst_parameter_fname(get_rqst_params, validated_params, rqst_errors):
    if 'fname' in get_rqst_params:
        validated_params['first name'] = get_rqst_params['fname']
        validated_params['first name list'] = re.findall(r"[\w. '-]+", validated_params['first name'])

        if not validated_params['first name list']:
            rqst_errors.append('Invalid first name, first names must be ascii strings.')


def validate_get_rqst_parameter_lname(get_rqst_params, validated_params, rqst_errors):
    if 'lname' in get_rqst_params:
        validated_params['last name'] = get_rqst_params['lname']
        validated_params['last name list'] = re.findall(r"[\w. '-]+", validated_params['last name'])

        if not validated_params['last name list']:
            rqst_errors.append('Invalid last name, last names must be ascii strings.')


def validate_get_rqst_parameter_email(get_rqst_params, validated_params, rqst_errors):
    if 'email' in get_rqst_params:
        validated_params['email'] = get_rqst_params['email']
        validated_params['email list'] = re.findall(r"[@\w. '-]+", validated_params['email'])

        if not validated_params['email list']:
            rqst_errors.append('Invalid email parameter.')


def validate_get_rqst_parameter_mpn(get_rqst_params, validated_params, rqst_errors):
    if 'mpn' in get_rqst_params:
        validated_params['mpn'] = get_rqst_params['mpn']
        validated_params['mpn list'] = re.findall(r"[@\w. '-]+", validated_params['mpn'])

        if not validated_params['mpn list']:
            rqst_errors.append('Invalid mpn parameter.')


def validate_get_rqst_parameter_region(get_rqst_params, validated_params, rqst_errors):
    if 'region' in get_rqst_params:
        validated_params['region'] = get_rqst_params['region']
        validated_params['region list'] = re.findall(r"[@\w. '-]+", validated_params['region'])

        if not validated_params['region list']:
            rqst_errors.append('Invalid region, regions must be ascii strings.')


def validate_get_rqst_parameter_location(get_rqst_params, validated_params, rqst_errors):
    if 'location' in get_rqst_params:
        validated_params['location'] = urllib.parse.unquote(get_rqst_params['location'])


def validate_get_rqst_parameter_fields(get_rqst_params, validated_params, rqst_errors):
    if 'fields' in get_rqst_params:
        validated_params['fields'] = urllib.parse.unquote(get_rqst_params['fields'])
        validated_params['fields list'] = re.findall(r"[@\w. '-]+", validated_params['fields'])

        if not validated_params['fields list']:
            rqst_errors.append('Invalid fields parameter, field parameters must be ascii strings.')


GET_PARAMETER_VALIDATION_FUNCTIONS = {
    "id": validate_get_rqst_parameter_id,
    "fname": validate_get_rqst_parameter_fname,
    "lname": validate_get_rqst_parameter_lname,
    "email": validate_get_rqst_parameter_email,
    "mpn": validate_get_rqst_parameter_mpn,
    "region": validate_get_rqst_parameter_region,
    "location": validate_get_rqst_parameter_location,
    'fields': validate_get_rqst_parameter_fields,
}


def validate_get_request_parameters(get_rqst_params, rqst_errors, params_to_validate=None):
    validated_params = {}

    def run_validation_functions():
        for parameter_to_validate in params_to_validate:
            if parameter_to_validate in GET_PARAMETER_VALIDATION_FUNCTIONS:
                validation_fucntion = GET_PARAMETER_VALIDATION_FUNCTIONS[parameter_to_validate]
                validation_fucntion(get_rqst_params, validated_params, rqst_errors)
            else:
                raise NotImplementedError("GET parameter :{} does not have a validation function implemented.")

    if params_to_validate:
        run_validation_functions()
    else:
        validate_get_rqst_parameter_fname(get_rqst_params, validated_params, rqst_errors)
        validate_get_rqst_parameter_lname(get_rqst_params, validated_params, rqst_errors)
        validate_get_rqst_parameter_id(get_rqst_params, validated_params, rqst_errors)
        validate_get_rqst_parameter_location(get_rqst_params, validated_params, rqst_errors)
        validate_get_rqst_parameter_fields(get_rqst_params, validated_params, rqst_errors)
        validate_get_rqst_parameter_email(get_rqst_params, validated_params, rqst_errors)
        validate_get_rqst_parameter_mpn(get_rqst_params, validated_params, rqst_errors)
        validate_get_rqst_parameter_region(get_rqst_params, validated_params, rqst_errors)

        if 'partnerid' in get_rqst_params:
            validated_params['partnerid'] = get_rqst_params['partnerid']
            list_of_ids = re.findall("[@\w. '-_]+", validated_params['partnerid'])
            validated_params['partnerid list'] = list_of_ids
        if 'navid' in get_rqst_params:
            validated_params['navigator id'] = get_rqst_params['navid']

            list_of_nav_ids = re.findall("\d+", validated_params['navigator id'])
            for indx, element in enumerate(list_of_nav_ids):
                list_of_nav_ids[indx] = int(element)
            validated_params['navigator id list'] = list_of_nav_ids

            if not validated_params['navigator id list']:
                rqst_errors.append('Invalid navigator id, navigator ids must be base 10 integers')
        if 'location_id' in get_rqst_params:
            validated_params['location_id'] = get_rqst_params['location_id']

            list_of_ids = re.findall("\d+", validated_params['location_id'])
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            validated_params['location_id list'] = list_of_ids

            if not validated_params['location_id list']:
                rqst_errors.append('Invalid location_id, ids must be base 10 integers')
        if 'is_cps_consumer' in get_rqst_params:
            validated_params['is_cps_consumer'] = get_rqst_params['is_cps_consumer'].lower()
            if validated_params['is_cps_consumer'] not in ('true', 'false'):
                rqst_errors.append("Value for is_cps_consumer is not type boolean")
            else:
                validated_params['is_cps_consumer'] = validated_params['is_cps_consumer'] in ('true')
        if 'page' in get_rqst_params:
            validated_params['page number'] = int(get_rqst_params['page'])
        if "county" in get_rqst_params:
            validated_params['county'] = get_rqst_params['county']
            validated_params['county list'] = re.findall(r"[\w. '-]+", validated_params['county'])
        if "zipcode" in get_rqst_params:
            validated_params['zipcode'] = get_rqst_params['zipcode']
            validated_params['zipcode list'] = re.findall(r"\d+", validated_params['zipcode'])

            if not validated_params['zipcode list']:
                rqst_errors.append('Invalid zipcode, zipcodes must be integers')
        if "time" in get_rqst_params:
            try:
                validated_params['look up date'] = datetime.date.today() - datetime.timedelta(days=int(get_rqst_params['time']))
                validated_params['time'] = get_rqst_params['time']
            except ValueError:
                rqst_errors.append('time parameter must be a valid integer. Metrics returned without time parameter.')
        if "startdate" in get_rqst_params:
            try:
                datetime.datetime.strptime(get_rqst_params["startdate"], '%Y-%m-%d')
                validated_params['start date'] = get_rqst_params["startdate"]
            except ValueError:
                rqst_errors.append('startdate parameter must be a valid date. Metrics returned without startdate parameter.')
        if "enddate" in get_rqst_params:
            try:
                datetime.datetime.strptime(get_rqst_params["enddate"], '%Y-%m-%d')
                validated_params['end date'] = get_rqst_params["enddate"]
            except ValueError:
                rqst_errors.append('enddate parameter must be a valid integer. Metrics returned without enddate parameter.')
        if "groupby" in get_rqst_params:
            validated_params['group by'] = get_rqst_params['groupby']
        if 'nav_location_tags' in get_rqst_params:
            validated_params['nav_location_tags'] = get_rqst_params['nav_location_tags']
            validated_params['nav_location_tags list'] = re.findall(r"[@\w. '-]+", validated_params['nav_location_tags'])
        if 'intent' in get_rqst_params:
            validated_params['intent'] = urllib.parse.unquote(get_rqst_params['intent'])
        if 'name' in get_rqst_params:
            validated_params['name'] = urllib.parse.unquote(get_rqst_params['name'])
        if "state" in get_rqst_params:
            validated_params['state'] = get_rqst_params['state']
            validated_params['state list'] = re.findall(r"[\w. '-]+", validated_params['state'])

            number_of_commas = len(re.findall(r",", validated_params['state']))
            number_of_parameters_there_should_be = number_of_commas + 1
            if number_of_parameters_there_should_be != len(validated_params['state list']):
                rqst_errors.append('List of states is formatted wrong. Values must be ascii strings separated by commas')

            if not validated_params['state list']:
                rqst_errors.append('Invalid state, states must be ascii strings.')
        if 'has_sample_id_card' in get_rqst_params:
            validated_params['has_sample_id_card'] = get_rqst_params['has_sample_id_card'].lower()
            if validated_params['has_sample_id_card'] not in ('true', 'false'):
                rqst_errors.append("Value for has_sample_id_card is not type boolean")
            else:
                validated_params['has_sample_id_card'] = validated_params['has_sample_id_card'] in ('true')
        if 'carrier_id' in get_rqst_params:
            validated_params['carrier id'] = get_rqst_params['carrier_id']

            list_of_carrier_ids = re.findall("\d+", validated_params['carrier id'])
            for indx, element in enumerate(list_of_carrier_ids):
                list_of_carrier_ids[indx] = int(element)
            validated_params['carrier id list'] = list_of_carrier_ids

            if not validated_params['carrier id list']:
                rqst_errors.append('Invalid carrier id, carrier ids must be base 10 integers')
        if "carrier_state" in get_rqst_params:
            validated_params['carrier state'] = get_rqst_params['carrier_state']
            validated_params['carrier state list'] = re.findall(r"[\w. '-]+", validated_params['carrier state'])
        if 'carrier_name' in get_rqst_params:
            validated_params['carrier name'] = urllib.parse.unquote(get_rqst_params['carrier_name'])
        if 'accepted_location_id' in get_rqst_params:
            validated_params['accepted_location_id'] = get_rqst_params['accepted_location_id']

            list_of_accepted_location_ids = re.findall("\d+", validated_params['accepted_location_id'])
            for indx, element in enumerate(list_of_accepted_location_ids):
                list_of_accepted_location_ids[indx] = int(element)
            validated_params['accepted_location_id_list'] = list_of_accepted_location_ids

            if not validated_params['accepted_location_id_list']:
                rqst_errors.append('Invalid accepted_location id, accepted_location ids must be base 10 integers')
        if 'network_name' in get_rqst_params:
            validated_params['network_name'] = urllib.parse.unquote(get_rqst_params['network_name'])
        if 'network_id' in get_rqst_params:
            validated_params['network_id'] = get_rqst_params['network_id']

            list_of_network_ids = re.findall("\d+", validated_params['network_id'])
            for indx, element in enumerate(list_of_network_ids):
                list_of_network_ids[indx] = int(element)
            validated_params['network_id_list'] = list_of_network_ids

            if not validated_params['network_id_list']:
                rqst_errors.append('Invalid network id, network ids must be base 10 integers')
        if 'is_cps_location' in get_rqst_params:
            validated_params['is_cps_location'] = get_rqst_params['is_cps_location'].lower()
            if validated_params['is_cps_location'] not in ('true', 'false'):
                rqst_errors.append("Value for is_cps_location is not type boolean")
            else:
                validated_params['is_cps_location'] = validated_params['is_cps_location'] in ('true')
        if 'question' in get_rqst_params:
            validated_params['question'] = urllib.parse.unquote(get_rqst_params['question'])
        if 'gen_concern_name' in get_rqst_params:
            validated_params['gen_concern_name'] = urllib.parse.unquote(get_rqst_params['gen_concern_name'])
        if 'gen_concern_id_subset' in get_rqst_params:
            validated_params['gen_concern_id_subset'] = get_rqst_params['gen_concern_id_subset']

            list_of_gen_concern_ids = re.findall("\d+", validated_params['gen_concern_id_subset'])
            for indx, element in enumerate(list_of_gen_concern_ids):
                list_of_gen_concern_ids[indx] = int(element)
            validated_params['gen_concern_id_subset_list'] = list_of_gen_concern_ids

            if not validated_params['gen_concern_id_subset_list']:
                rqst_errors.append('Invalid gen_concern id, gen_concern ids must be base 10 integers')
        if 'gen_concern_id' in get_rqst_params:
            validated_params['gen_concern_id'] = get_rqst_params['gen_concern_id']

            list_of_gen_concern_ids = re.findall("\d+", validated_params['gen_concern_id'])
            for indx, element in enumerate(list_of_gen_concern_ids):
                list_of_gen_concern_ids[indx] = int(element)
            validated_params['gen_concern_id_list'] = list_of_gen_concern_ids

            if not validated_params['gen_concern_id_list']:
                rqst_errors.append('Invalid gen_concern id, gen_concern ids must be base 10 integers')
        if 'include_summary_report' in get_rqst_params:
            validated_params['include_summary_report'] = get_rqst_params['include_summary_report'].lower()
            if validated_params['include_summary_report'] not in ('true', 'false'):
                rqst_errors.append("Value for include_summary_report is not type boolean")
            else:
                validated_params['include_summary_report'] = validated_params['include_summary_report'] in ('true')
        if 'include_detailed_report' in get_rqst_params:
            validated_params['include_detailed_report'] = get_rqst_params['include_detailed_report'].lower()
            if validated_params['include_detailed_report'] not in ('true', 'false'):
                rqst_errors.append("Value for include_detailed_report is not type boolean")
            else:
                validated_params['include_detailed_report'] = validated_params['include_detailed_report'] in ('true')
        if 'hospital_name' in get_rqst_params:
            validated_params['hospital_name'] = urllib.parse.unquote(get_rqst_params['hospital_name'])
        if 'family_size' in get_rqst_params:
            validated_params['family_size'] = get_rqst_params['family_size']

            list_of_family_sizes = re.findall("\d+", validated_params['family_size'])
            for indx, element in enumerate(list_of_family_sizes):
                list_of_family_sizes[indx] = int(element)
            validated_params['family_size_list'] = list_of_family_sizes

            if not validated_params['family_size_list']:
                rqst_errors.append('Invalid family_size, family_sizes must be base 10 integers')
        if 'premium_type' in get_rqst_params:
            validated_params['premium_type'] = get_rqst_params['premium_type']
            validated_params['premium_type list'] = re.findall(r"[@\w. '-]+", validated_params['premium_type'])

            if not validated_params['premium_type list']:
                rqst_errors.append('Invalid premium_type.')
            else:
                for premium_type in validated_params['premium_type list']:
                    dummy_plan_object = HealthcarePlan(premium_type=premium_type)
                    if not dummy_plan_object.check_premium_choices():
                        rqst_errors.append('The following is an invalid premium_type : {}'.format(premium_type))

    return validated_params


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
