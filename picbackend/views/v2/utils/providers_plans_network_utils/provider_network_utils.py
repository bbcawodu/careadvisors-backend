"""
This module defines utility functions and classes for views that handle provider networks contracted with PIC
"""

import json
from picmodels.models import ProviderNetwork
from picbackend.views.v2.utils import clean_string_value_from_dict_object
from picbackend.views.v2.utils import clean_int_value_from_dict_object


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


def retrieve_provider_networks_by_id(response_raw_data, rqst_errors, provider_networks, rqst_provider_network_id, list_of_ids):
    if rqst_provider_network_id == "all":
        all_provider_networks = provider_networks
        provider_networks_dict = {}
        for provider_network in all_provider_networks:
            provider_networks_dict[provider_network.id] = provider_network.return_values_dict()
        provider_networks_list = []
        for provider_network_key, provider_network_entry in provider_networks_dict.items():
            provider_networks_list.append(provider_network_entry)

        response_raw_data["Data"] = provider_networks_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            provider_networks = provider_networks.filter(id__in=list_of_ids)
            if len(provider_networks) > 0:
                provider_networks_dict = {}
                for provider_network in provider_networks:
                    provider_networks_dict[provider_network.id] = provider_network.return_values_dict()
                provider_networks_list = []
                for provider_network_key, provider_network_entry in provider_networks_dict.items():
                    provider_networks_list.append(provider_network_entry)
                response_raw_data["Data"] = provider_networks_list

                for provider_network_id in list_of_ids:
                    if provider_network_id not in provider_networks_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Provider network with id: {!s} not found in database'.format(str(provider_network_id)))
            else:
                rqst_errors.append('No provider networks found for database ID(s): ' + rqst_provider_network_id)
        else:
            rqst_errors.append('No valid provider network IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_provider_networks_by_name(response_raw_data, rqst_errors, provider_networks, rqst_name):
    provider_networks_list = []
    provider_networks = provider_networks.filter(name__iexact=rqst_name)

    if provider_networks:
        for provider_network in provider_networks:
            provider_networks_list.append(provider_network.return_values_dict())
        response_raw_data["Data"] = provider_networks_list
    else:
        rqst_errors.append('No provider networks with name: {!s} not found in database'.format(rqst_name))

    return response_raw_data, rqst_errors
