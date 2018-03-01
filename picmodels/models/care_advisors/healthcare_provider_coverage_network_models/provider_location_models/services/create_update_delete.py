import json
import picmodels.models


def create_row_w_validated_params(cls, validated_params, post_errors):
    provider_network_obj = return_provider_network_obj_with_given_id(
        validated_params['rqst_provider_network_id'],
        post_errors
    )

    provider_location_obj = None
    if provider_network_obj and not post_errors:
        rqst_provider_location_name = validated_params['rqst_provider_location_name']
        found_provider_location_objs = cls.check_for_provider_location_objs_with_given_name_and_network(
            rqst_provider_location_name,
            provider_network_obj,
            post_errors
        )

        if not found_provider_location_objs and not post_errors:
            provider_location_obj = cls()
            provider_location_obj.name = rqst_provider_location_name
            provider_location_obj.provider_network = provider_network_obj
            provider_location_obj.save()
            provider_location_obj.accepted_plans = validated_params['add_accepted_plans_objects']
            provider_location_obj.save()

    return provider_location_obj


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        provider_location_obj = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        provider_location_obj = None
        rqst_errors.append("Provider Location does not exist for database id: {}".format(rqst_id))

    if provider_location_obj:
        if 'rqst_provider_network_id' in validated_params:
            provider_network_obj = return_provider_network_obj_with_given_id(
                validated_params['rqst_provider_network_id'],
                rqst_errors
            )
        else:
            provider_network_obj = provider_location_obj.provider_network

        if not rqst_errors:
            if 'rqst_provider_location_name' in validated_params:
                provider_location_name = validated_params['rqst_provider_location_name']
            else:
                provider_location_name = provider_location_obj.name

            found_provider_location_objs = cls.check_for_provider_location_objs_with_given_name_and_network(
                provider_location_name,
                provider_network_obj,
                rqst_errors,
                rqst_id
            )

            if not found_provider_location_objs and not rqst_errors:
                if 'rqst_provider_location_name' in validated_params:
                    provider_location_obj.name = validated_params['rqst_provider_location_name']

                if 'rqst_provider_network_id' in validated_params:
                    provider_location_obj.provider_network = provider_network_obj

                if 'add_accepted_plans_objects' in validated_params:
                    check_accepted_plans_for_given_instances(
                        provider_location_obj.accepted_plans.all(),
                        validated_params['add_accepted_plans_objects'],
                        provider_location_obj,
                        rqst_errors
                    )

                    if not rqst_errors:
                        for plan in validated_params['add_accepted_plans_objects']:
                            provider_location_obj.accepted_plans.add(plan)
                elif 'remove_accepted_plans_objects' in validated_params:
                    check_accepted_plans_for_not_given_instances(
                        provider_location_obj.accepted_plans.all(),
                        validated_params['remove_accepted_plans_objects'],
                        provider_location_obj,
                        rqst_errors
                    )

                    if not rqst_errors:
                        for plan in validated_params['remove_accepted_plans_objects']:
                            provider_location_obj.accepted_plans.remove(plan)

                if not rqst_errors:
                    provider_location_obj.save()

    if rqst_errors:
        provider_location_obj = None

    return provider_location_obj


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        provider_location_obj = cls.objects.get(id=rqst_id)
        provider_location_obj.delete()
    except cls.DoesNotExist:
        rqst_errors.append("Provider location does not exist for database id: {}".format(rqst_id))


def return_provider_network_obj_with_given_id(provider_network_id, post_errors):
    try:
        provider_network_obj = picmodels.models.ProviderNetwork.objects.get(id=provider_network_id)
    except picmodels.models.ProviderNetwork.DoesNotExist:
        provider_network_obj = None
        post_errors.append("No ProviderNetwork objects found for id: {}".format(provider_network_id))

    return provider_network_obj


def check_for_provider_location_objs_with_given_name_and_network(cls, provider_location_name, provider_network_obj, rqst_errors, current_provider_location_id=None):
    found_provider_location_obj = False

    provider_location_objs = cls.objects.filter(
        name__iexact=provider_location_name,
        provider_network=provider_network_obj
    )

    if provider_location_objs:
        found_provider_location_obj = True

        provider_location_ids = []
        len_of_provider_location_qset = len(provider_location_objs)
        for provider_location_obj in provider_location_objs:
            provider_location_ids.append(provider_location_obj.id)

        if len_of_provider_location_qset > 1:
            rqst_errors.append(
                "Multiple provider locations with name: {} and provider network id: {} already exist in db. (Hint - Delete all but one and modify the remaining) id's: {}".format(
                    provider_location_name, provider_network_obj.id, json.dumps(provider_location_ids)))
        else:
            if not current_provider_location_id or current_provider_location_id not in provider_location_ids:
                rqst_errors.append(
                    "Provider location with name: {} and provider network id: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        provider_location_name, provider_network_obj.id, provider_location_ids[0]))
            else:
                found_provider_location_obj = False

    return found_provider_location_obj


def check_accepted_plans_for_given_instances(cur_accepted_plans_qset, given_accepted_plan_instances, provider_location_obj, rqst_errors):
    for plan in given_accepted_plan_instances:
        if plan in cur_accepted_plans_qset:
            rqst_errors.append(
                "Plan with the following id already exists in db id {}'s accepted plans list (Hint - remove from parameter 'add_accepted_plans' list): {})".format(
                    provider_location_obj.id, plan.id
                ))


def check_accepted_plans_for_not_given_instances(cur_accepted_plans_qset, given_accepted_plan_instances, provider_location_obj, rqst_errors):
    for plan in given_accepted_plan_instances:
        if plan not in cur_accepted_plans_qset:
            rqst_errors.append(
                "Plan with the following id does not exist in db id {}'s accepted plans list (Hint - remove from parameter 'remove_accepted_plans' list): {})".format(
                    provider_location_obj.id, plan.id
                ))
