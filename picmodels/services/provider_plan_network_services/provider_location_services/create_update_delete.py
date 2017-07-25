import json
from picmodels.models import ProviderNetwork
from picmodels.models import ProviderLocation


def add_instance_using_validated_params(add_provider_location_params, post_errors):
    provider_network_obj = return_provider_network_obj_with_given_id(add_provider_location_params['rqst_provider_network_id'],
                                                                     post_errors)

    provider_location_obj = None
    if provider_network_obj and not post_errors:
        rqst_provider_location_name = add_provider_location_params['rqst_provider_location_name']
        found_provider_location_objs = check_for_provider_location_objs_with_given_name_and_network(
            rqst_provider_location_name, provider_network_obj, post_errors)

        if not found_provider_location_objs and not post_errors:
            provider_location_obj = create_new_location_obj(add_provider_location_params,
                                                            rqst_provider_location_name,
                                                            provider_network_obj)

    return provider_location_obj


def return_provider_network_obj_with_given_id(provider_network_id, post_errors):
    try:
        provider_network_obj = ProviderNetwork.objects.get(id=provider_network_id)
    except ProviderNetwork.DoesNotExist:
        provider_network_obj = None
        post_errors.append("No ProviderNetwork objects found for id: {}".format(provider_network_id))

    return provider_network_obj


def check_for_provider_location_objs_with_given_name_and_network(provider_location_name, provider_network_obj, post_errors, current_provider_location_id=None):
    found_provider_location_obj = False

    provider_location_objs = ProviderLocation.objects.filter(name__iexact=provider_location_name,
                                                             provider_network=provider_network_obj)

    if provider_location_objs:
        found_provider_location_obj = True

        provider_location_ids = []
        len_of_provider_location_qset = len(provider_location_objs)
        for provider_location_obj in provider_location_objs:
            provider_location_ids.append(provider_location_obj.id)

        if len_of_provider_location_qset > 1:
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


def create_new_location_obj(provider_location_params, provider_location_name, provider_network_obj):
    provider_location_obj = ProviderLocation()
    provider_location_obj.name = provider_location_name
    provider_location_obj.provider_network = provider_network_obj
    provider_location_obj.save()
    provider_location_obj.accepted_plans = provider_location_params['accepted_plans_objects']
    provider_location_obj.save()

    return provider_location_obj


def modify_instance_using_validated_params(modify_provider_location_params, rqst_provider_location_id, post_errors):
    provider_network_obj = return_provider_network_obj_with_given_id(modify_provider_location_params['rqst_provider_network_id'],
                                                                     post_errors)

    provider_location_obj = None
    if provider_network_obj and not post_errors:
        rqst_provider_location_name = modify_provider_location_params['rqst_provider_location_name']
        found_provider_location_objs = check_for_provider_location_objs_with_given_name_and_network(
            rqst_provider_location_name, provider_network_obj, post_errors, rqst_provider_location_id)

        if not found_provider_location_objs and not post_errors:
            provider_location_obj = modify_location_obj(modify_provider_location_params,
                                                        rqst_provider_location_id,
                                                        rqst_provider_location_name,
                                                        provider_network_obj,
                                                        post_errors)

    return provider_location_obj


def modify_location_obj(provider_location_params, provider_location_id, provider_location_name, provider_network_obj, post_errors):
    try:
        provider_location_obj = ProviderLocation.objects.get(id=provider_location_id)
        provider_location_obj.name = provider_location_name
        provider_location_obj.provider_network = provider_network_obj
        provider_location_obj.accepted_plans.clear()
        provider_location_obj.accepted_plans = provider_location_params['accepted_plans_objects']
        provider_location_obj.save()
    except ProviderLocation.DoesNotExist:
        provider_location_obj = None
        post_errors.append("Provider Location does not exist for database id: {}".format(provider_location_id))

    return provider_location_obj


def add_accepted_plans_to_instance_using_validated_params(modify_provider_location_params, rqst_provider_location_id, post_errors):
    try:
        provider_location_obj = ProviderLocation.objects.get(id=rqst_provider_location_id)
        cur_accepted_plans_qset = provider_location_obj.accepted_plans.all()
        accepted_plan_instances_from_rqst = modify_provider_location_params['accepted_plans_objects']

        if not accepted_plan_instances_from_rqst:
            post_errors.append("No accepted_plans_objects given in request.")
        else:
            check_accepted_plans_for_given_instances(cur_accepted_plans_qset, accepted_plan_instances_from_rqst,
                                                 provider_location_obj, post_errors)
    except ProviderLocation.DoesNotExist:
        provider_location_obj = None
        post_errors.append(
            "Provider Location does not exist for database id: {}".format(rqst_provider_location_id))

    if not post_errors and provider_location_obj:
        provider_network_obj = return_provider_network_obj_with_given_id(
            modify_provider_location_params['rqst_provider_network_id'],
            post_errors)

        if provider_network_obj and not post_errors:
            rqst_provider_location_name = modify_provider_location_params['rqst_provider_location_name']
            found_provider_location_objs = check_for_provider_location_objs_with_given_name_and_network(
                rqst_provider_location_name, provider_network_obj, post_errors, rqst_provider_location_id)

            if not found_provider_location_objs and not post_errors:
                provider_location_obj.name = rqst_provider_location_name
                provider_location_obj.provider_network = provider_network_obj
                for plan in modify_provider_location_params['accepted_plans_objects']:
                    provider_location_obj.accepted_plans.add(plan)

                provider_location_obj.save()

    return provider_location_obj


def check_accepted_plans_for_given_instances(cur_accepted_plans_qset, given_accepted_plan_instances, provider_location_obj, post_errors):
    for plan in given_accepted_plan_instances:
        if plan in cur_accepted_plans_qset:
            post_errors.append(
                "Plan with the following id already exists in db id {}'s accepted plans list (Hint - remove from parameter 'accepted_plans' list): {})".format(
                    provider_location_obj.id, plan.id
                ))


def remove_accepted_plans_from_instance_using_validated_params(modify_provider_location_params, rqst_provider_location_id, post_errors):
    try:
        provider_location_obj = ProviderLocation.objects.get(id=rqst_provider_location_id)
        cur_accepted_plans_qset = provider_location_obj.accepted_plans.all()
        accepted_plan_instances_from_rqst = modify_provider_location_params['accepted_plans_objects']

        if not accepted_plan_instances_from_rqst:
            post_errors.append("No accepted_plans_objects given in request.")
        else:
            check_accepted_plans_for_not_given_instances(cur_accepted_plans_qset, accepted_plan_instances_from_rqst,
                                                         provider_location_obj, post_errors)
    except ProviderLocation.DoesNotExist:
        provider_location_obj = None
        post_errors.append(
            "Provider Location does not exist for database id: {}".format(rqst_provider_location_id))

    if provider_location_obj and not post_errors:
        provider_network_obj = return_provider_network_obj_with_given_id(
            modify_provider_location_params['rqst_provider_network_id'],
            post_errors)

        if provider_network_obj and not post_errors:
            rqst_provider_location_name = modify_provider_location_params['rqst_provider_location_name']
            found_provider_location_objs = check_for_provider_location_objs_with_given_name_and_network(
                rqst_provider_location_name, provider_network_obj, post_errors, rqst_provider_location_id)

            if not found_provider_location_objs and not post_errors:
                provider_location_obj.name = rqst_provider_location_name
                provider_location_obj.provider_network = provider_network_obj
                for plan in modify_provider_location_params['accepted_plans_objects']:
                    provider_location_obj.accepted_plans.remove(plan)

                provider_location_obj.save()

    return provider_location_obj


def check_accepted_plans_for_not_given_instances(cur_accepted_plans_qset, given_accepted_plan_instances, provider_location_obj, post_errors):
    for plan in given_accepted_plan_instances:
        if plan not in cur_accepted_plans_qset:
            post_errors.append(
                "Plan with the following id does not exist in db id {}'s accepted plans list (Hint - remove from parameter 'accepted_plans' list): {})".format(
                    provider_location_obj.id, plan.id
                ))


def delete_instance_using_validated_params(rqst_provider_location_id, post_errors):
    try:
        provider_location_obj = ProviderLocation.objects.get(id=rqst_provider_location_id)
        provider_location_obj.delete()
    except ProviderLocation.DoesNotExist:
        post_errors.append("Provider location does not exist for database id: {}".format(rqst_provider_location_id))
