from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_list_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object

from picmodels.models import HealthcarePlan


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {
        'rqst_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors)
    }

    rqst_action = validated_params['rqst_action']

    if rqst_action == 'create':
        validate_create_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'update':
        validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
        validate_update_row_params(rqst_body, validated_params, rqst_errors)
    elif rqst_action == 'delete':
        validated_params['id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)

    return validated_params


def validate_create_row_params(rqst_body, validated_params, rqst_errors):
    rqst_provider_location_name = clean_string_value_from_dict_object(rqst_body, "root", "name", rqst_errors)
    validated_params["name"] = rqst_provider_location_name

    rqst_provider_network_id = clean_int_value_from_dict_object(
        rqst_body,
        "root",
        "provider_network_id",
        rqst_errors
    )
    validated_params["provider_network_id"] = rqst_provider_network_id

    rqst_add_accepted_plans_ids = clean_list_value_from_dict_object(
        rqst_body,
        "root",
        "add_accepted_plans",
        rqst_errors,
        empty_list_allowed=True
    )

    add_accepted_plan_objects = []
    if rqst_add_accepted_plans_ids:
        add_accepted_plan_objects = validate_accepted_plans_params(rqst_add_accepted_plans_ids, rqst_errors)
    validated_params["add_accepted_plans_objects"] = add_accepted_plan_objects


def validate_update_row_params(rqst_body, validated_params, rqst_errors):
    if "name" in rqst_body:
        rqst_provider_location_name = clean_string_value_from_dict_object(rqst_body, "root", "name", rqst_errors)
        validated_params["name"] = rqst_provider_location_name

    if "provider_network_id" in rqst_body:
        rqst_provider_network_id = clean_int_value_from_dict_object(
            rqst_body,
            "root",
            "provider_network_id",
            rqst_errors
        )
        validated_params["provider_network_id"] = rqst_provider_network_id

    if "add_accepted_plans" in rqst_body:
        rqst_add_accepted_plans_ids = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "add_accepted_plans",
            rqst_errors,
        )

        if rqst_add_accepted_plans_ids:
            add_accepted_plan_objects = validate_accepted_plans_params(rqst_add_accepted_plans_ids, rqst_errors)
            validated_params["add_accepted_plans_objects"] = add_accepted_plan_objects
    elif "remove_accepted_plans" in rqst_body:
        rqst_remove_accepted_plans_ids = clean_list_value_from_dict_object(
            rqst_body,
            "root",
            "remove_accepted_plans",
            rqst_errors,
        )

        if rqst_remove_accepted_plans_ids:
            remove_accepted_plan_objects = validate_accepted_plans_params(rqst_remove_accepted_plans_ids, rqst_errors)
            validated_params["remove_accepted_plans_objects"] = remove_accepted_plan_objects


def validate_accepted_plans_params(accepted_plans_ids, rqst_errors):
    for indx, plan_id in enumerate(accepted_plans_ids):
        if not isinstance(plan_id, int):
            rqst_errors.append(
                "All plan ids must be integers, plan id is not an integer for 'accepted_plans' field at index: {}".format(
                    indx
                )
            )

    accepted_plans_ids = list(set(accepted_plans_ids))
    accepted_plans_objects = []
    plans_errors = []

    if accepted_plans_ids and not rqst_errors:
        for accepted_plan_id in accepted_plans_ids:
            try:
                accepted_plan_object = HealthcarePlan.objects.get(id=accepted_plan_id)
                accepted_plans_objects.append(accepted_plan_object)
            except HealthcarePlan.DoesNotExist:
                plans_errors.append(
                    "No HealthcarePlan database entry found for id: {}".format(accepted_plan_id))

    for plan_error in plans_errors:
        rqst_errors.append(plan_error)

    return accepted_plans_objects
