import json
from picmodels.models import ConsumerGeneralConcern


def add_instance_using_validated_params(validated_rqst_params, post_errors):
    found_general_concern_objs = check_for_general_concern_objs_with_given_name(validated_rqst_params['rqst_general_concern_name'], post_errors)

    general_concern_obj = None
    if not found_general_concern_objs and not post_errors:
        general_concern_obj = create_general_concern_obj(validated_rqst_params)

    return general_concern_obj


def check_for_general_concern_objs_with_given_name(general_concern_name, post_errors, current_general_concern_id=None):
    found_general_concern_obj = False

    general_concern_objs = ConsumerGeneralConcern.objects.filter(name__iexact=general_concern_name)

    if general_concern_objs:
        found_general_concern_obj = True

        general_concern_ids = []
        len_of_general_concerns_qset = len(general_concern_objs)
        for general_concern_obj in general_concern_objs:
            general_concern_ids.append(general_concern_obj.id)

        if len_of_general_concerns_qset > 1:
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
    general_concern_obj.save()

    return general_concern_obj


def modify_instance_using_validated_params(validated_rqst_params, rqst_general_concern_id, rqst_errors):
    found_general_concern_objs = check_for_general_concern_objs_with_given_name(validated_rqst_params['rqst_general_concern_name'], rqst_errors, rqst_general_concern_id)

    general_concern_obj = None
    if not found_general_concern_objs and not rqst_errors:
        general_concern_obj = modify_general_concern_obj(validated_rqst_params, rqst_general_concern_id, rqst_errors)

    return general_concern_obj


def modify_general_concern_obj(general_concern_params, rqst_general_concern_id, rqst_errors):
    general_concern_obj = None
    try:
        general_concern_obj = ConsumerGeneralConcern.objects.get(id=rqst_general_concern_id)
        general_concern_obj.name = general_concern_params['rqst_general_concern_name']
        general_concern_obj.save()
    except ConsumerGeneralConcern.DoesNotExist:
        rqst_errors.append("General concern does not exist for database id: {}".format(rqst_general_concern_id))

    return general_concern_obj


def delete_instance_using_validated_params(rqst_general_concern_id, rqst_errors):
    try:
        general_concern_obj = ConsumerGeneralConcern.objects.get(id=rqst_general_concern_id)
        general_concern_obj.delete()
    except ConsumerGeneralConcern.DoesNotExist:
        rqst_errors.append("General concern does not exist for database id: {}".format(rqst_general_concern_id))
