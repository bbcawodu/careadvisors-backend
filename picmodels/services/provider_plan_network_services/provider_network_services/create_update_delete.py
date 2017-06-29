import json
from picmodels.models import ProviderNetwork


def add_instance_using_validated_params(add_provider_network_params, post_errors):
    found_provider_network_objs = check_for_provider_network_objs_with_given_name(
        add_provider_network_params['rqst_provider_network_name'], post_errors)

    provider_network_obj = None
    if not found_provider_network_objs and not post_errors:
        provider_network_obj = ProviderNetwork()
        provider_network_obj.name = add_provider_network_params['rqst_provider_network_name']
        provider_network_obj.save()

    return provider_network_obj


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


def modify_instance_using_validated_params(modify_provider_network_params, rqst_provider_network_id, post_errors):
    found_provider_network_objs = check_for_provider_network_objs_with_given_name(
        modify_provider_network_params['rqst_provider_network_name'], post_errors, rqst_provider_network_id)

    provider_network_obj = None
    if not found_provider_network_objs and not post_errors:
        try:
            provider_network_obj = ProviderNetwork.objects.get(id=rqst_provider_network_id)
            provider_network_obj.name = modify_provider_network_params['rqst_provider_network_name']
            provider_network_obj.save()
        except ProviderNetwork.DoesNotExist:
            post_errors.append("Provider Network does not exist for database id: {}".format(rqst_provider_network_id))

    return provider_network_obj


def delete_instance_using_validated_params(rqst_provider_network_id, post_errors):
    try:
        provider_network_obj = ProviderNetwork.objects.get(id=rqst_provider_network_id)
        provider_network_obj.delete()
    except ProviderNetwork.DoesNotExist:
        post_errors.append("Provider network does not exist for database id: {}".format(rqst_provider_network_id))
