"""
This module defines utility functions and classes for views that handle carriers for provider networks contracted with
PIC
"""

import json
from picmodels.models import ConsumerGeneralConcern
from ....utils import clean_string_value_from_dict_object
from ....utils import clean_int_value_from_dict_object


def add_general_concern_using_api_rqst_params(response_raw_data, rqst_gen_concern_info, post_errors):
    add_general_concern_params = get_general_concern_mgmt_put_params(rqst_gen_concern_info, post_errors)

    if len(post_errors) == 0:
        found_general_concern_objs = check_for_general_concern_objs_with_given_name(
            add_general_concern_params['rqst_general_concern_name'], post_errors)

        if not found_general_concern_objs and len(post_errors) == 0:
            general_concern_obj = create_general_concern_obj(add_general_concern_params)

            if len(post_errors) == 0:
                general_concern_obj.save()
                response_raw_data['Data']["Database ID"] = general_concern_obj.id

    return response_raw_data


def get_general_concern_mgmt_put_params(rqst_carrier_info, rqst_errors):

    return {"rqst_general_concern_name": clean_string_value_from_dict_object(rqst_carrier_info, "root", "name", rqst_errors),
            }


def check_for_general_concern_objs_with_given_name(general_concern_name, post_errors, current_general_concern_id=None):
    found_general_concern_obj = False

    general_concern_objs = ConsumerGeneralConcern.objects.filter(name__iexact=general_concern_name)

    if general_concern_objs:
        found_general_concern_obj = True

        general_concern_ids = []
        for general_concern_obj in general_concern_objs:
            general_concern_ids.append(general_concern_obj.id)

        if general_concern_objs.count() > 1:
            post_errors.append(
                "Multiple general concerns with name: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    general_concern_name, json.dumps(general_concern_ids)))
        else:
            if not current_general_concern_id or current_general_concern_id not in general_concern_ids:
                post_errors.append(
                    "General concern with name: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        general_concern_name, general_concern_ids[0]))
            else:
                found_general_concern_obj = False

    return found_general_concern_obj


def create_general_concern_obj(general_concern_params):
    general_concern_obj = ConsumerGeneralConcern()
    general_concern_obj.name = general_concern_params['rqst_general_concern_name']

    return general_concern_obj


def modify_general_concern_using_api_rqst_params(response_raw_data, rqst_general_concern_info, rqst_errors):
    modify_general_concern_params = get_general_concern_mgmt_put_params(rqst_general_concern_info, rqst_errors)
    rqst_general_concern_id = clean_int_value_from_dict_object(rqst_general_concern_info, "root", "Database ID", rqst_errors)

    if len(rqst_errors) == 0:
        found_general_concern_objs = check_for_general_concern_objs_with_given_name(
            modify_general_concern_params['rqst_general_concern_name'], rqst_errors, rqst_general_concern_id)

        if not found_general_concern_objs and len(rqst_errors) == 0:
            general_concern_obj = modify_general_concern_obj(modify_general_concern_params, rqst_general_concern_id, rqst_errors)

            if len(rqst_errors) == 0:
                general_concern_obj.save()
                response_raw_data['Data']["Database ID"] = general_concern_obj.id

    return response_raw_data


def modify_general_concern_obj(general_concern_params, rqst_general_concern_id, rqst_errors):
    general_concern_obj = None
    try:
        general_concern_obj = ConsumerGeneralConcern.objects.get(id=rqst_general_concern_id)
        general_concern_obj.name = general_concern_params['rqst_general_concern_name']
    except ConsumerGeneralConcern.DoesNotExist:
        rqst_errors.append("General concern does not exist for database id: {}".format(rqst_general_concern_id))

    return general_concern_obj


def delete_general_concern_using_api_rqst_params(response_raw_data, rqst_general_concern_info, rqst_errors):
    rqst_general_concern_id = clean_int_value_from_dict_object(rqst_general_concern_info, "root", "Database ID", rqst_errors)

    if len(rqst_errors) == 0:
        try:
            general_concern_obj = ConsumerGeneralConcern.objects.get(id=rqst_general_concern_id)
            general_concern_obj.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except ConsumerGeneralConcern.DoesNotExist:
            rqst_errors.append("General concern does not exist for database id: {}".format(rqst_general_concern_id))

    return response_raw_data
