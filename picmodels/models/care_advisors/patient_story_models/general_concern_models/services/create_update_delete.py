import json


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    found_general_concern_objs = cls.check_for_general_concern_objs_with_given_name(
        validated_params['rqst_general_concern_name'],
        rqst_errors
    )

    general_concern_obj = None
    if not found_general_concern_objs and not rqst_errors:
        general_concern_obj = cls()
        general_concern_obj.name = validated_params['rqst_general_concern_name']
        general_concern_obj.save()

    return general_concern_obj


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']
    found_general_concern_objs = cls.check_for_general_concern_objs_with_given_name(
        validated_params['rqst_general_concern_name'],
        rqst_errors,
        rqst_id
    )

    general_concern_obj = None
    if not found_general_concern_objs and not rqst_errors:
        try:
            general_concern_obj = cls.objects.get(id=rqst_id)
            general_concern_obj.name = validated_params['rqst_general_concern_name']
            general_concern_obj.save()
        except cls.DoesNotExist:
            rqst_errors.append("General concern does not exist for database id: {}".format(rqst_id))

    return general_concern_obj


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        general_concern_obj = cls.objects.get(id=rqst_id)
        general_concern_obj.delete()
    except cls.DoesNotExist:
        rqst_errors.append("General concern does not exist for database id: {}".format(rqst_id))


def check_for_general_concern_objs_with_given_name(cls, general_concern_name, rqst_errors, current_id=None):
    found_general_concern_obj = False

    general_concern_objs = cls.objects.filter(name__iexact=general_concern_name)

    if general_concern_objs:
        found_general_concern_obj = True

        general_concern_ids = []
        len_of_general_concerns_qset = len(general_concern_objs)
        for general_concern_obj in general_concern_objs:
            general_concern_ids.append(general_concern_obj.id)

        if len_of_general_concerns_qset > 1:
            rqst_errors.append(
                "Multiple general concerns with name: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    general_concern_name, json.dumps(general_concern_ids)))
        else:
            if not current_id or current_id not in general_concern_ids:
                rqst_errors.append(
                    "General concern with name: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        general_concern_name, general_concern_ids[0]))
            else:
                found_general_concern_obj = False

    return found_general_concern_obj
