"""
This module defines utility functions and classes for views that handle locations for provider networks that are
contracted with PIC
"""

import json
from picmodels.models import ProviderNetwork
from picmodels.models import ProviderLocation
from picmodels.models import HealthcarePlan
from picbackend.views.v2.utils import clean_string_value_from_dict_object
from picbackend.views.v2.utils import clean_int_value_from_dict_object
from picbackend.views.v2.utils import clean_list_value_from_dict_object


def add_provider_location(response_raw_data, rqst_provider_location_info, post_errors):
    add_provider_location_params = get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors)

    if len(post_errors) == 0:
        provider_network_obj = return_provider_network_obj_with_given_id(add_provider_location_params['rqst_provider_network_id'],
                                                                         post_errors)
        if provider_network_obj and len(post_errors) == 0:
            rqst_provider_location_name = add_provider_location_params['rqst_provider_location_name']
            found_provider_location_objs = check_for_provider_location_objs_with_given_name_and_network(
                rqst_provider_location_name, provider_network_obj, post_errors)

            if not found_provider_location_objs and len(post_errors) == 0:
                provider_location_obj = ProviderLocation()
                provider_location_obj.name = rqst_provider_location_name
                provider_location_obj.provider_network = provider_network_obj
                provider_location_obj.save()
                provider_location_obj.accepted_plans = add_provider_location_params['accepted_plans_objects']
                provider_location_obj.save()
                response_raw_data['Data']["Database ID"] = provider_location_obj.id

    return response_raw_data


def modify_provider_location(response_raw_data, rqst_provider_location_info, post_errors):
    modify_provider_location_params = get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors)

    if len(post_errors) == 0:
        provider_network_obj = return_provider_network_obj_with_given_id(modify_provider_location_params['rqst_provider_network_id'],
                                                                         post_errors)
        if provider_network_obj and len(post_errors) == 0:
            rqst_provider_location_name = modify_provider_location_params['rqst_provider_location_name']
            rqst_provider_location_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                         "Database ID", post_errors)
            found_provider_location_objs = check_for_provider_location_objs_with_given_name_and_network(
                rqst_provider_location_name, provider_network_obj, post_errors, rqst_provider_location_id)

            if not found_provider_location_objs and len(post_errors) == 0:
                try:
                    provider_location_obj = ProviderLocation.objects.get(id=rqst_provider_location_id)
                    provider_location_obj.name = rqst_provider_location_name
                    provider_location_obj.provider_network = provider_network_obj
                    provider_location_obj.accepted_plans.clear()
                    provider_location_obj.accepted_plans = modify_provider_location_params['accepted_plans_objects']
                    provider_location_obj.save()

                    response_raw_data['Data']["Database ID"] = provider_location_obj.id
                except ProviderLocation.DoesNotExist:
                    post_errors.append("Provider Location does not exist for database id: {}".format(rqst_provider_location_id))

    return response_raw_data


def modify_provider_location_add_accepted_plans(response_raw_data, rqst_provider_location_info, post_errors):
    modify_provider_location_params = get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors)
    rqst_provider_location_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                 "Database ID", post_errors)

    try:
        provider_location_obj = ProviderLocation.objects.get(id=rqst_provider_location_id)
        cur_accepted_plans_qset = provider_location_obj.accepted_plans.all()
        for plan in modify_provider_location_params['accepted_plans_objects']:
            if plan in cur_accepted_plans_qset:
                post_errors.append("Plan with the following id already exists in db id {}'s accepted plans list (Hint - remove from parameter 'accepted_plans' list): {})".format(
                    provider_location_obj.id, plan.id
                ))
    except ProviderLocation.DoesNotExist:
        post_errors.append(
            "Provider Location does not exist for database id: {}".format(rqst_provider_location_id))

    if len(post_errors) == 0:
        provider_network_obj = return_provider_network_obj_with_given_id(
            modify_provider_location_params['rqst_provider_network_id'],
            post_errors)
        if provider_network_obj and len(post_errors) == 0:
            rqst_provider_location_name = modify_provider_location_params['rqst_provider_location_name']
            found_provider_location_objs = check_for_provider_location_objs_with_given_name_and_network(
                rqst_provider_location_name, provider_network_obj, post_errors, rqst_provider_location_id)

            if not found_provider_location_objs and len(post_errors) == 0:
                provider_location_obj.name = rqst_provider_location_name
                provider_location_obj.provider_network = provider_network_obj
                for plan in modify_provider_location_params['accepted_plans_objects']:
                    provider_location_obj.accepted_plans.add(plan)

                provider_location_obj.save()

                response_raw_data['Data']["Database ID"] = provider_location_obj.id

    return response_raw_data


def modify_provider_location_remove_accepted_plans(response_raw_data, rqst_provider_location_info, post_errors):
    modify_provider_location_params = get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors)
    rqst_provider_location_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                 "Database ID", post_errors)

    try:
        provider_location_obj = ProviderLocation.objects.get(id=rqst_provider_location_id)
        cur_accepted_plans_qset = provider_location_obj.accepted_plans.all()
        for plan in modify_provider_location_params['accepted_plans_objects']:
            if plan not in cur_accepted_plans_qset:
                post_errors.append(
                    "Plan with the following id does not exist in db id {}'s accepted plans list (Hint - remove from parameter 'accepted_plans' list): {})".format(
                        provider_location_obj.id, plan.id
                    ))
    except ProviderLocation.DoesNotExist:
        post_errors.append(
            "Provider Location does not exist for database id: {}".format(rqst_provider_location_id))

    if len(post_errors) == 0:
        provider_network_obj = return_provider_network_obj_with_given_id(
            modify_provider_location_params['rqst_provider_network_id'],
            post_errors)
        if provider_network_obj and len(post_errors) == 0:
            rqst_provider_location_name = modify_provider_location_params['rqst_provider_location_name']
            found_provider_location_objs = check_for_provider_location_objs_with_given_name_and_network(
                rqst_provider_location_name, provider_network_obj, post_errors, rqst_provider_location_id)

            if not found_provider_location_objs and len(post_errors) == 0:
                provider_location_obj.name = rqst_provider_location_name
                provider_location_obj.provider_network = provider_network_obj
                for plan in modify_provider_location_params['accepted_plans_objects']:
                    provider_location_obj.accepted_plans.remove(plan)

                provider_location_obj.save()

                response_raw_data['Data']["Database ID"] = provider_location_obj.id

    return response_raw_data


def check_for_provider_location_objs_with_given_name_and_network(provider_location_name, provider_network_obj, post_errors, current_provider_location_id=None):
    found_provider_location_obj = False

    provider_location_objs = ProviderLocation.objects.filter(name__iexact=provider_location_name,
                                                             provider_network=provider_network_obj)

    if provider_location_objs:
        found_provider_location_obj = True

        provider_location_ids = []
        for provider_location_obj in provider_location_objs:
            provider_location_ids.append(provider_location_obj.id)

        if provider_location_objs.count() > 1:
            post_errors.append(
                "Multiple provider locations with name: {} and provider network id: {} already exist in db. (Hint - Delete all but one and modify the remaining) id's: {}".format(
                    provider_location_name, provider_network_obj.id, json.dumps(provider_location_ids)))
        else:
            if not current_provider_location_id or current_provider_location_id not in provider_location_ids:
                post_errors.append(
                    "Provider location with name: {} and provider network id: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        provider_location_name, provider_network_obj.id, provider_location_ids[0]))
            else:
                found_provider_location_obj = False

    return found_provider_location_obj


def get_provider_location_mgmt_put_params(rqst_provider_location_info, post_errors):
    rqst_provider_location_name = clean_string_value_from_dict_object(rqst_provider_location_info, "root", "name", post_errors)
    rqst_provider_network_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                "provider_network Database ID", post_errors)
    rqst_accepted_plans_ids = clean_list_value_from_dict_object(rqst_provider_location_info, "root", "accepted_plans",
                                                            post_errors, empty_list_allowed=True)
    for plan_id in rqst_accepted_plans_ids:
        if not isinstance(plan_id, int):
            post_errors.append("All plan ids must be integers, plan id is not an integer for 'accepted_plans' field at index: {}".format(plan_id))
    rqst_accepted_plans_ids = list(set(rqst_accepted_plans_ids))
    accepted_plans_objects = []
    plans_errors = []
    if rqst_accepted_plans_ids:
        for accepted_plan_id in rqst_accepted_plans_ids:
            try:
                accepted_plan_object = HealthcarePlan.objects.get(id=accepted_plan_id)
                accepted_plans_objects.append(accepted_plan_object)
            except HealthcarePlan.DoesNotExist:
                plans_errors.append(
                    "No HealthcarePlan database entry found for id: {}".format(accepted_plan_id))
    for plan_error in plans_errors:
        post_errors.append(plan_error)

    return {"rqst_provider_location_name": rqst_provider_location_name,
            "rqst_provider_network_id": rqst_provider_network_id,
            "accepted_plans_objects": accepted_plans_objects}


def return_provider_network_obj_with_given_id(provider_network_id, post_errors):
    try:
        provider_network_obj = ProviderNetwork.objects.get(id=provider_network_id)
    except ProviderNetwork.DoesNotExist:
        provider_network_obj = None
        post_errors.append("No ProviderNetwork objects found for id: {}".format(provider_network_id))

    return provider_network_obj


def delete_provider_location(response_raw_data, rqst_provider_location_info, post_errors):
    rqst_provider_location_id = clean_int_value_from_dict_object(rqst_provider_location_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            provider_location_obj = ProviderLocation.objects.get(id=rqst_provider_location_id)
            provider_location_obj.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except ProviderLocation.DoesNotExist:
            post_errors.append("Provider location does not exist for database id: {}".format(rqst_provider_location_id))

    return response_raw_data


def retrieve_provider_locations_by_id(response_raw_data, rqst_errors, provider_locations, rqst_provider_location_id, list_of_ids):
    if rqst_provider_location_id == "all":
        all_provider_locations = provider_locations
        provider_locations_dict = {}
        for provider_location in provider_locations:
            provider_locations_dict[provider_location.id] = provider_location.return_values_dict()
        provider_locations_list = []
        for provider_location_key, provider_location_entry in provider_locations_dict.items():
            provider_locations_list.append(provider_location_entry)

        response_raw_data["Data"] = provider_locations_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            provider_locations = provider_locations.filter(id__in=list_of_ids)
            if len(provider_locations) > 0:

                provider_locations_dict = {}
                for provider_location in provider_locations:
                    provider_locations_dict[provider_location.id] = provider_location.return_values_dict()
                provider_locations_list = []
                for provider_location_key, provider_location_entry in provider_locations_dict.items():
                    provider_locations_list.append(provider_location_entry)
                response_raw_data["Data"] = provider_locations_list

                for provider_location_id in list_of_ids:
                    if provider_location_id not in provider_locations_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Provider location with id: {!s} not found in database'.format(str(provider_location_id)))
            else:
                rqst_errors.append('No provider locations found for database ID(s): ' + rqst_provider_location_id)
        else:
            rqst_errors.append('No valid provider location IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_provider_locations_by_name(response_raw_data, rqst_errors, provider_locations, rqst_name):
    provider_locations_list = []
    provider_locations = provider_locations.filter(name__iexact=rqst_name)

    if provider_locations:
        for provider_location in provider_locations:
            provider_locations_list.append(provider_location.return_values_dict())
        response_raw_data["Data"] = provider_locations_list
    else:
        rqst_errors.append('No provider locations with name: {!s} not found in database'.format(rqst_name))

    return response_raw_data, rqst_errors


def retrieve_provider_locations_by_network_name(response_raw_data, rqst_errors, provider_locations, rqst_network_name):
    provider_locations_list = []
    provider_locations = provider_locations.filter(provider_network__name__iexact=rqst_network_name)

    if provider_locations:
        for provider_location in provider_locations:
            provider_locations_list.append(provider_location.return_values_dict())
        response_raw_data["Data"] = provider_locations_list
    else:
        rqst_errors.append('No Plans with a carrier with the name: {!s} found in database'.format(rqst_network_name))

    return response_raw_data, rqst_errors


def retrieve_provider_locations_by_network_id(response_raw_data, rqst_errors, provider_locations, rqst_network_id, list_of_network_ids):
    if rqst_network_id == "all":
        all_provider_locations = provider_locations
        provider_locations_dict = {}
        for provider_location in all_provider_locations:
            provider_locations_dict[provider_location.id] = provider_location.return_values_dict()
        provider_locations_list = []
        for provider_location_key, provider_location_entry in provider_locations_dict.items():
            provider_locations_list.append(provider_location_entry)

        response_raw_data["Data"] = provider_locations_list
    elif list_of_network_ids:
        if len(list_of_network_ids) > 0:
            for indx, element in enumerate(list_of_network_ids):
                list_of_network_ids[indx] = int(element)
            provider_locations = provider_locations.filter(provider_network__id__in=list_of_network_ids)
            if len(provider_locations) > 0:

                provider_locations_dict = {}
                for provider_location in provider_locations:
                    if provider_location.provider_network.id not in provider_locations_dict:
                        provider_locations_dict[provider_location.provider_network.id] = [provider_location.return_values_dict()]
                    else:
                        provider_locations_dict[provider_location.provider_network.id].append(provider_location.return_values_dict())
                provider_locations_list = []
                for provider_location_key, provider_location_entry in provider_locations_dict.items():
                    provider_locations_list.append(provider_location_entry)
                response_raw_data["Data"] = provider_locations_list

                for network_id in list_of_network_ids:
                    if network_id not in provider_locations_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Provider location with provider network id: {!s} not found in database'.format(str(network_id)))
            else:
                rqst_errors.append('No provider locations found for provider network database ID(s): ' + rqst_network_id)
        else:
            rqst_errors.append('No valid provider location database IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors
