import sys


def clean_json_string_input(json_dict, dict_name, dict_key, post_errors, empty_string_allowed=False,
                            none_allowed=False):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] == "" and empty_string_allowed is False:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty string".format(dict_key, dict_name))
    elif json_dict[dict_key] is None and none_allowed is False:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    else:
        return str(json_dict[dict_key])
    return None


def clean_json_int_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    else:
        return int(json_dict[dict_key])
    return None


def clean_dict_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(json_dict[dict_key], dict):
        post_errors.append("Value for {!r} in {!r} dictionary is not a dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] == {}:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty dictionary".format(dict_key, dict_name))
    else:
        return json_dict[dict_key]
    return None


def clean_list_input(json_dict, dict_name, dict_key, post_errors):
    if dict_key not in json_dict:
        post_errors.append("{!r} key not found in {!r} dictionary".format(dict_key, dict_name))
    elif json_dict[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} dictionary is Null".format(dict_key, dict_name))
    elif not isinstance(json_dict[dict_key], list):
        post_errors.append("Value for {!r} in {!r} dictionary is not a list".format(dict_key, dict_name))
    elif json_dict[dict_key] == []:
        post_errors.append("Value for {!r} in {!r} dictionary is an empty list".format(dict_key, dict_name))
    else:
        return json_dict[dict_key]
    return None


def init_response_data():
    return {'Status': {"Error Code": 0, "Version": 1.0}}, []


def parse_and_log_errors(response_raw_data, errors_list):
    if len(errors_list) > 0:
        if response_raw_data["Status"]["Error Code"] == 0:
            response_raw_data["Status"]["Error Code"] = 1
        response_raw_data["Status"]["Errors"] = errors_list

        for message in errors_list:
            print(message)
            sys.stdout.flush()

    return response_raw_data
