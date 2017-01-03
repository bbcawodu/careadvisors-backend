import sys
import urllib
import re
import datetime


def clean_json_string_input(json_dict, dict_name, dict_key, post_errors, empty_string_allowed=False,
                            none_allowed=False):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] == "" and empty_string_allowed is False:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty string".format(dict_key, dict_name))
    elif json_dict[dict_key] is None and none_allowed is False:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    else:
        if json_dict[dict_key] or json_dict[dict_key] == "":
            return str(json_dict[dict_key])
        else:
            return None


def clean_json_int_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    else:
        return int(json_dict[dict_key])


def clean_dict_input(json_dict, dict_name, dict_key, post_errors, none_allowed=False):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None and none_allowed == False:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(json_dict[dict_key], dict):
        post_errors.append("Value for {!r} in {!r} dictionary is not a dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] == {}:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty dictionary".format(dict_key, dict_name))
    else:
        return json_dict[dict_key]
    return None


def clean_list_input(json_dict, dict_name, dict_key, post_errors, empty_list_allowed=False):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(json_dict[dict_key], list):
        post_errors.append("Value for {!r} in {!r} dictionary is not a list".format(dict_key, dict_name))
    elif json_dict[dict_key] == []:
        if empty_list_allowed:
            return []
        else:
            post_errors.append("Value for {!r} in {!r} dictionary is an empty list".format(dict_key, dict_name))
    else:
        return json_dict[dict_key]
    return None


def build_search_params(rqst_params, response_raw_data, rqst_errors):
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
            search_params['look up date'] = datetime.date.today() - datetime.timedelta(days=rqst_params['time'])
            search_params['time'] = rqst_params['time']
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('time parameter must be a valid integer. Metrics returned without time parameter.')
    if "startdate" in rqst_params:
        try:
            datetime.datetime.strptime(rqst_params["startdate"], '%Y-%m-%d')
            search_params['start date'] = rqst_params["startdate"]
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('startdate parameter must be a valid date. Metrics returned without startdate parameter.')
    if "enddate" in rqst_params:
        try:
            datetime.datetime.strptime(rqst_params["enddate"], '%Y-%m-%d')
            search_params['end date'] = rqst_params["enddate"]
        except ValueError:
            response_raw_data['Status']['Error Code'] = 1
            rqst_errors.append('enddate parameter must be a valid integer. Metrics returned without enddate parameter.')
    if "groupby" in rqst_params:
        search_params['group by'] = rqst_params['groupby']

    return search_params


def init_v2_response_data():
    return {'Status': {"Error Code": 0, "Warnings": [], "Version": 2.0, "Missing Parameters": []}}, []


def parse_and_log_errors(response_raw_data, errors_list):
    if len(errors_list) > 0:
        if response_raw_data["Status"]["Error Code"] == 0:
            response_raw_data["Status"]["Error Code"] = 1
        response_raw_data["Status"]["Errors"] = errors_list

        for message in errors_list:
            print(message)
            sys.stdout.flush()

    return response_raw_data
