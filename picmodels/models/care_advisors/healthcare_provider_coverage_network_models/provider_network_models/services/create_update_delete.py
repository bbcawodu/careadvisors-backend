import json


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    found_provider_network_objs = cls.check_for_provider_network_objs_with_given_name(
        validated_params['rqst_provider_network_name'],
        rqst_errors
    )

    provider_network_obj = None
    if not found_provider_network_objs and not rqst_errors:
        provider_network_obj = cls()
        provider_network_obj.name = validated_params['rqst_provider_network_name']
        provider_network_obj.save()

    return provider_network_obj


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        provider_network_obj = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        rqst_errors.append("Provider Network does not exist for database id: {}".format(rqst_id))
        provider_network_obj = None

    if provider_network_obj:
        if 'rqst_provider_network_name' in validated_params:
            rqst_provider_network_name = validated_params['rqst_provider_network_name']
        else:
            rqst_provider_network_name = provider_network_obj.name

        found_provider_network_objs = cls.check_for_provider_network_objs_with_given_name(
            rqst_provider_network_name,
            rqst_errors,
            rqst_id
        )

        if not found_provider_network_objs and not rqst_errors:
            if 'rqst_provider_network_name' in validated_params:
                provider_network_obj.name = validated_params['rqst_provider_network_name']

            provider_network_obj.save()

    return provider_network_obj


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        provider_network_obj = cls.objects.get(id=rqst_id)
        provider_network_obj.delete()
    except cls.DoesNotExist:
        rqst_errors.append("Provider network does not exist for database id: {}".format(rqst_id))


def check_for_provider_network_objs_with_given_name(cls, provider_network_name, rqst_errors, current_provider_network_id=None):
    found_provider_network_obj = False

    provider_network_objs = cls.objects.filter(name__iexact=provider_network_name)

    if provider_network_objs:
        found_provider_network_obj = True

        provider_network_ids = []
        len_of_provider_network_qset = len(provider_network_objs)
        for provider_network_obj in provider_network_objs:
            provider_network_ids.append(provider_network_obj.id)

        if len_of_provider_network_qset > 1:
            rqst_errors.append(
                "Multiple provider networks with name: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    provider_network_name, json.dumps(provider_network_ids)))
        else:
            if not current_provider_network_id or current_provider_network_id not in provider_network_ids:
                rqst_errors.append(
                    "Provider network with name: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        provider_network_name, provider_network_ids[0]))
            else:
                found_provider_network_obj = False

    return found_provider_network_obj
