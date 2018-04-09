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
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] == "" and empty_string_allowed is False:
        post_errors.append("Value for {!r} in {!r} object is an empty string".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and none_allowed is False:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif (dict_object[dict_key] is None and none_allowed is False) and not isinstance(dict_object[dict_key], str):
        post_errors.append("Value for {!r} in {!r} object is not a string".format(dict_key, dict_name))
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
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and not none_allowed:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif (dict_object[dict_key] is None and none_allowed is False) and not isinstance(dict_object[dict_key], int):
        post_errors.append("Value for {!r} in {!r} object is not an integer".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
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
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and not none_allowed:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif (dict_object[dict_key] is None and none_allowed is False) and not isinstance(dict_object[dict_key], float) and not isinstance(dict_object[dict_key], int):
        post_errors.append("Value for {!r} in {!r} object is not an float".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
    else:
        return float(dict_object[dict_key])


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
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None and none_allowed == False:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif (dict_object[dict_key] is None and none_allowed is False) and not isinstance(dict_object[dict_key], dict):
        post_errors.append("Value for {!r} in {!r} object is not a dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] == {}:
        post_errors.append("Value for {!r} in {!r} object is an empty dictionary".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
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
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], list):
        post_errors.append("Value for {!r} in {!r} object is not a list".format(dict_key, dict_name))
    elif dict_object[dict_key] == []:
        if empty_list_allowed:
            return []
        else:
            post_errors.append("Value for {!r} in {!r} object is an empty list".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
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
            post_errors.append("{!r} key not found in {!r} object".format(dict_key, dict_name))
    elif dict_object[dict_key] is None:
        post_errors.append("Value for {!r} in {!r} object is Null".format(dict_key, dict_name))
    elif not isinstance(dict_object[dict_key], bool):
        post_errors.append("Value for {!r} in {!r} object is not type boolean".format(dict_key, dict_name))
    elif dict_object[dict_key] == '':
        post_errors.append("Value for {!r} in {!r} object is and empty string".format(dict_key, dict_name))
    else:
        return dict_object[dict_key]
