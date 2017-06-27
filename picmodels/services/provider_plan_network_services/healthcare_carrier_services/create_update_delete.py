import json
from picmodels.models import HealthcareCarrier


def add_instance_using_validated_params(add_carrier_params, post_errors):
    found_healthcare_carrier_objs = check_for_healthcare_carrier_objs_with_given_name_and_state(
        add_carrier_params['rqst_carrier_name'], add_carrier_params['rqst_carrier_state'], post_errors)

    healthcare_carrier_obj = None
    if not found_healthcare_carrier_objs and not post_errors:
        healthcare_carrier_obj = create_new_carrier_obj(add_carrier_params, post_errors)

    return healthcare_carrier_obj


def check_for_healthcare_carrier_objs_with_given_name_and_state(carrier_name, carrier_state, post_errors,
                                                                current_carrier_id=None):
    found_healthcare_carrier_obj = False

    healthcare_carrier_objs = HealthcareCarrier.objects.filter(name__iexact=carrier_name,
                                                               state_province__iexact=carrier_state)

    if healthcare_carrier_objs:
        found_healthcare_carrier_obj = True

        carrier_ids = []
        for carrier_obj in healthcare_carrier_objs:
            carrier_ids.append(carrier_obj.id)

        if healthcare_carrier_objs.count() > 1:
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


def create_new_carrier_obj(carrier_params, post_errors):
    healthcare_carrier_obj = HealthcareCarrier()
    healthcare_carrier_obj.name = carrier_params['rqst_carrier_name']
    healthcare_carrier_obj.state_province = carrier_params['rqst_carrier_state']
    if not healthcare_carrier_obj.check_state_choices():
        post_errors.append("State: {!s} is not a valid state abbreviation".format(healthcare_carrier_obj.state_province))

    if not post_errors:
        healthcare_carrier_obj.save()
    else:
        healthcare_carrier_obj = None

    return healthcare_carrier_obj


def modify_instance_using_validated_params(modify_carrier_params, rqst_carrier_id, post_errors):
    found_healthcare_carrier_objs = check_for_healthcare_carrier_objs_with_given_name_and_state(
        modify_carrier_params['rqst_carrier_name'], modify_carrier_params['rqst_carrier_state'], post_errors, rqst_carrier_id)

    healthcare_carrier_obj = None
    if not found_healthcare_carrier_objs and not post_errors:
        healthcare_carrier_obj = modify_carrier_obj(modify_carrier_params, rqst_carrier_id, post_errors)

    return healthcare_carrier_obj


def modify_carrier_obj(carrier_params, rqst_carrier_id, post_errors):
    healthcare_carrier_obj = None
    try:
        healthcare_carrier_obj = HealthcareCarrier.objects.get(id=rqst_carrier_id)
        healthcare_carrier_obj.name = carrier_params['rqst_carrier_name']
        healthcare_carrier_obj.state_province = carrier_params['rqst_carrier_state']
        if not healthcare_carrier_obj.check_state_choices():
            post_errors.append(
                "State: {!s} is not a valid state abbreviation".format(healthcare_carrier_obj.state_province))
    except HealthcareCarrier.DoesNotExist:
        post_errors.append("Healthcare carrier does not exist for database id: {}".format(rqst_carrier_id))

    if not post_errors:
        healthcare_carrier_obj.save()
    else:
        healthcare_carrier_obj = None

    return healthcare_carrier_obj


def delete_instance_using_validated_params(rqst_carrier_id, post_errors):
    try:
        healthcare_carrier_obj = HealthcareCarrier.objects.get(id=rqst_carrier_id)
        healthcare_carrier_obj.delete()
    except HealthcareCarrier.DoesNotExist:
        post_errors.append("Healthcare carrier does not exist for database id: {}".format(rqst_carrier_id))
