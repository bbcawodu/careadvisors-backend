import json


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    found_healthcare_carrier_objs = cls.check_for_healthcare_carrier_objs_with_given_name_and_state(
        validated_params['rqst_carrier_name'],
        validated_params['rqst_carrier_state'],
        rqst_errors
    )

    healthcare_carrier_obj = None
    if not found_healthcare_carrier_objs and not rqst_errors:
        healthcare_carrier_obj = cls()
        healthcare_carrier_obj.name = validated_params['rqst_carrier_name']
        healthcare_carrier_obj.state_province = validated_params['rqst_carrier_state']

        if not healthcare_carrier_obj.check_state_choices():
            rqst_errors.append(
                "State: {!s} is not a valid state abbreviation".format(healthcare_carrier_obj.state_province))

        if not rqst_errors:
            healthcare_carrier_obj.save()

    return healthcare_carrier_obj


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    healthcare_carrier_obj = None
    try:
        healthcare_carrier_obj = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        rqst_errors.append("Healthcare carrier does not exist for database id: {}".format(rqst_id))

    found_healthcare_carrier_objs = True
    if healthcare_carrier_obj:
        if 'rqst_carrier_name' not in validated_params:
            carrier_name = healthcare_carrier_obj.name
        else:
            carrier_name = validated_params['rqst_carrier_name']

        if 'rqst_carrier_state' not in validated_params:
            carrier_state = healthcare_carrier_obj.state_province
        else:
            carrier_state = validated_params['rqst_carrier_state']

        found_healthcare_carrier_objs = cls.check_for_healthcare_carrier_objs_with_given_name_and_state(
            carrier_name,
            carrier_state,
            rqst_errors,
            rqst_id
        )

    if not found_healthcare_carrier_objs and not rqst_errors:
        if 'rqst_carrier_name' in validated_params:
            healthcare_carrier_obj.name = validated_params['rqst_carrier_name']

        if 'rqst_carrier_state' in validated_params:
            healthcare_carrier_obj.state_province = validated_params['rqst_carrier_state']

        if not healthcare_carrier_obj.check_state_choices():
            rqst_errors.append(
                "State: {!s} is not a valid state abbreviation".format(healthcare_carrier_obj.state_province))

        if not rqst_errors:
            healthcare_carrier_obj.save()

    if rqst_errors:
        healthcare_carrier_obj = None

    return healthcare_carrier_obj


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        healthcare_carrier_obj = cls.objects.get(id=rqst_id)
        healthcare_carrier_obj.delete()
    except cls.DoesNotExist:
        rqst_errors.append("Healthcare carrier does not exist for database id: {}".format(rqst_id))


def check_for_healthcare_carrier_objs_with_given_name_and_state(
        cls,
        carrier_name,
        carrier_state,
        post_errors,
        current_carrier_id=None):
    found_healthcare_carrier_obj = False

    healthcare_carrier_objs = cls.objects.filter(name__iexact=carrier_name,state_province__iexact=carrier_state)

    if healthcare_carrier_objs:
        found_healthcare_carrier_obj = True

        carrier_ids = []
        len_of_carrier_qset = len(healthcare_carrier_objs)
        for carrier_obj in healthcare_carrier_objs:
            carrier_ids.append(carrier_obj.id)

        if len_of_carrier_qset > 1:
            post_errors.append(
                "Multiple healthcare carriers with name: {} and state: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    carrier_name, carrier_state, json.dumps(carrier_ids)))
        else:
            if not current_carrier_id or current_carrier_id not in carrier_ids:
                post_errors.append(
                    "Healthcare carrier with name: {} and state: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        carrier_name, carrier_state, carrier_ids[0]))
            else:
                found_healthcare_carrier_obj = False

    return found_healthcare_carrier_obj
