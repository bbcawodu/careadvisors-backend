"""
This module defines utility functions and classes for views that handle provider networks contracted with PIC
"""

import json
from picmodels.models import ProviderNetwork
from ....utils import clean_string_value_from_dict_object
from ....utils import clean_int_value_from_dict_object


def add_provider_network(response_raw_data, rqst_provider_network_info, post_errors):
    add_provider_network_params = get_provider_network_mgmt_put_params(rqst_provider_network_info, post_errors)

    if len(post_errors) == 0:
        found_provider_network_objs = check_for_provider_network_objs_with_given_name(
            add_provider_network_params['rqst_provider_network_name'], post_errors)

        if not found_provider_network_objs and len(post_errors) == 0:
            provider_network_obj = ProviderNetwork()
            provider_network_obj.name = add_provider_network_params['rqst_provider_network_name']
            provider_network_obj.save()

            response_raw_data['Data']["Database ID"] = provider_network_obj.id

    return response_raw_data


def modify_provider_network(response_raw_data, rqst_provider_network_info, post_errors):
    modify_provider_network_params = get_provider_network_mgmt_put_params(rqst_provider_network_info, post_errors)
    rqst_provider_network_id = clean_int_value_from_dict_object(rqst_provider_network_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        found_provider_network_objs = check_for_provider_network_objs_with_given_name(
            modify_provider_network_params['rqst_provider_network_name'], post_errors, rqst_provider_network_id)

        if not found_provider_network_objs and len(post_errors) == 0:
            try:
                provider_network_obj = ProviderNetwork.objects.get(id=rqst_provider_network_id)
                provider_network_obj.name = modify_provider_network_params['rqst_provider_network_name']
                provider_network_obj.save()

                response_raw_data['Data']["Database ID"] = provider_network_obj.id
            except ProviderNetwork.DoesNotExist:
                post_errors.append("Provider Network does not exist for database id: {}".format(rqst_provider_network_id))

    return response_raw_data


def check_for_provider_network_objs_with_given_name(provider_network_name, post_errors, current_provider_network_id=None):
    found_provider_network_obj = False

    provider_network_objs = ProviderNetwork.objects.filter(name__iexact=provider_network_name)

    if provider_network_objs:
        found_provider_network_obj = True

        provider_network_ids = []
        for provider_network_obj in provider_network_objs:
            provider_network_ids.append(provider_network_obj.id)

        if provider_network_objs.count() > 1:
            post_errors.append(
                "Multiple provider networks with name: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    provider_network_name, json.dumps(provider_network_ids)))
        else:
            if not current_provider_network_id or current_provider_network_id not in provider_network_ids:
                post_errors.append(
                    "Provider network with name: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        provider_network_name, provider_network_ids[0]))
            else:
                found_provider_network_obj = False

    return found_provider_network_obj


def get_provider_network_mgmt_put_params(rqst_provider_network_info, post_errors):
    rqst_provider_network_name = clean_string_value_from_dict_object(rqst_provider_network_info, "root", "name", post_errors)

    return {"rqst_provider_network_name": rqst_provider_network_name,}


def delete_provider_network(response_raw_data, rqst_provider_network_info, post_errors):
    rqst_provider_network_id = clean_int_value_from_dict_object(rqst_provider_network_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            provider_network_obj = ProviderNetwork.objects.get(id=rqst_provider_network_id)
            provider_network_obj.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except ProviderNetwork.DoesNotExist:
            post_errors.append("Provider network does not exist for database id: {}".format(rqst_provider_network_id))

    return response_raw_data
