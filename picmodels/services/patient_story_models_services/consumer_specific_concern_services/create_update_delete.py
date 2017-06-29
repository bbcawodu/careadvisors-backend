import json
from picmodels.models import ConsumerSpecificConcern


def add_instance_using_validated_params(add_specific_concern_params, rqst_errors):
    found_specific_concern_objs = check_for_specific_concern_objs_with_given_question(add_specific_concern_params["rqst_specific_concern_question"], rqst_errors)

    specific_concern_obj = None
    if not found_specific_concern_objs and not rqst_errors:
        specific_concern_obj = create_new_specific_concern_obj(add_specific_concern_params)

    return specific_concern_obj


def check_for_specific_concern_objs_with_given_question(specific_concern_question, post_errors, current_specific_concern_id=None):
    found_specific_concern_obj = False

    specific_concern_objs = ConsumerSpecificConcern.objects.filter(question__iexact=specific_concern_question)

    if specific_concern_objs:
        found_specific_concern_obj = True

        specific_concern_ids = []
        for specific_concern_obj in specific_concern_objs:
            specific_concern_ids.append(specific_concern_obj.id)

        if specific_concern_objs.count() > 1:
            post_errors.append(
                "Multiple specific concerns with question: {} already exist in db. (Hint - Delete all but one and modify the remaining) id's: {}".format(
                    specific_concern_question, json.dumps(specific_concern_ids)))
        else:
            if not current_specific_concern_id or current_specific_concern_id not in specific_concern_ids:
                post_errors.append(
                    "Specific concern with question: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        specific_concern_question, specific_concern_ids[0]))
            else:
                found_specific_concern_obj = False

    return found_specific_concern_obj


def create_new_specific_concern_obj(specific_concern_params):
    specific_concern_obj = ConsumerSpecificConcern()
    specific_concern_obj.question = specific_concern_params["rqst_specific_concern_question"]
    specific_concern_obj.research_weight = specific_concern_params["rqst_specific_concern_research_weight"]
    specific_concern_obj.save()
    specific_concern_obj.related_general_concerns = specific_concern_params["related_general_concerns_objects"]
    specific_concern_obj.save()

    return specific_concern_obj


def modify_instance_using_validated_params(modify_specific_concern_params, rqst_specific_concern_id, rqst_errors):
    found_specific_concern_objs = check_for_specific_concern_objs_with_given_question(
        modify_specific_concern_params["rqst_specific_concern_question"], rqst_errors, rqst_specific_concern_id)

    specific_concern_obj = None
    if not found_specific_concern_objs and not rqst_errors:
        specific_concern_obj = modify_specific_concern_obj(modify_specific_concern_params, rqst_specific_concern_id, rqst_errors)

    return specific_concern_obj


def modify_specific_concern_obj(specific_concern_params, specific_concern_id, rqst_errors):
    specific_concern_obj = None
    try:
        specific_concern_obj = ConsumerSpecificConcern.objects.get(id=specific_concern_id)
        specific_concern_obj.question = specific_concern_params["rqst_specific_concern_question"]
        specific_concern_obj.research_weight = specific_concern_params["rqst_specific_concern_research_weight"]
        specific_concern_obj.related_general_concerns.clear()
        specific_concern_obj.related_general_concerns = specific_concern_params["related_general_concerns_objects"]
        specific_concern_obj.save()
    except ConsumerSpecificConcern.DoesNotExist:
        rqst_errors.append("Specific concern does not exist for database id: {}".format(specific_concern_id))

    return specific_concern_obj


def add_general_concern_to_instance_using_validated_params(modify_specific_concern_params, rqst_specific_concern_id, rqst_errors):
    specific_concern_obj = None

    try:
        specific_concern_obj = ConsumerSpecificConcern.objects.get(id=rqst_specific_concern_id)

        if not modify_specific_concern_params['related_general_concerns_objects']:
            rqst_errors.append("No related_general_concerns_objects given in request.")
        else:
            check_related_general_concerns_for_given_instances(specific_concern_obj,
                                                               modify_specific_concern_params['related_general_concerns_objects'],
                                                               rqst_errors)
    except ConsumerSpecificConcern.DoesNotExist:
        rqst_errors.append(
            "Specific concern does not exist for database id: {}".format(rqst_specific_concern_id))

    if not rqst_errors:
        found_specific_concern_objs = check_for_specific_concern_objs_with_given_question(
            modify_specific_concern_params["rqst_specific_concern_question"], rqst_errors, rqst_specific_concern_id)

        if not found_specific_concern_objs and not rqst_errors:
            add_general_concerns_to_instance(specific_concern_obj, modify_specific_concern_params)

    return specific_concern_obj


def check_related_general_concerns_for_given_instances(specific_concern_obj, related_general_concerns_objects, rqst_errors):
    cur_related_general_concerns_qset = specific_concern_obj.related_general_concerns.all()
    for related_general_concerns_object in related_general_concerns_objects:
        if related_general_concerns_object in cur_related_general_concerns_qset:
            rqst_errors.append(
                "Related general concern with the following name already exists in db id {}'s related_general_concerns list (Hint - remove from parameter 'related_general_concerns' list): {})".format(
                    specific_concern_obj.id, related_general_concerns_object.name
                ))


def add_general_concerns_to_instance(specific_concern_obj, modify_specific_concern_params):
    specific_concern_obj.question = modify_specific_concern_params["rqst_specific_concern_question"]
    specific_concern_obj.research_weight = modify_specific_concern_params["rqst_specific_concern_research_weight"]
    for related_general_concerns_object in modify_specific_concern_params['related_general_concerns_objects']:
        specific_concern_obj.related_general_concerns.add(related_general_concerns_object)

    specific_concern_obj.save()


def remove_general_concern_from_instance_using_validated_params(modify_specific_concern_params, rqst_specific_concern_id, rqst_errors):
    specific_concern_obj = None

    try:
        specific_concern_obj = ConsumerSpecificConcern.objects.get(id=rqst_specific_concern_id)
        if not modify_specific_concern_params['related_general_concerns_objects']:
            rqst_errors.append("No related_general_concerns_objects given in request.")
        else:
            check_related_general_concerns_for_not_given_instances(specific_concern_obj,
                                                                   modify_specific_concern_params['related_general_concerns_objects'],
                                                                   rqst_errors)
    except ConsumerSpecificConcern.DoesNotExist:
        rqst_errors.append(
            "Specific concern does not exist for database id: {}".format(rqst_specific_concern_id))

    if not rqst_errors:
        found_specific_concern_objs = check_for_specific_concern_objs_with_given_question(
            modify_specific_concern_params["rqst_specific_concern_question"], rqst_errors, rqst_specific_concern_id)

        if not found_specific_concern_objs and not rqst_errors:
            remove_general_concerns_from_instance(specific_concern_obj, modify_specific_concern_params)

    return specific_concern_obj


def check_related_general_concerns_for_not_given_instances(specific_concern_obj, related_general_concerns_objects, rqst_errors):
    cur_related_general_concerns_qset = specific_concern_obj.related_general_concerns.all()
    for related_general_concerns_object in related_general_concerns_objects:
        if related_general_concerns_object not in cur_related_general_concerns_qset:
            rqst_errors.append(
                "Related general concern with the following name does not exist in db id {}'s related_general_concerns list (Hint - remove from parameter 'related_general_concerns' list): {})".format(
                    specific_concern_obj.id, related_general_concerns_object.name
                ))


def remove_general_concerns_from_instance(specific_concern_obj, modify_specific_concern_params):
    specific_concern_obj.question = modify_specific_concern_params["rqst_specific_concern_question"]
    specific_concern_obj.research_weight = modify_specific_concern_params["rqst_specific_concern_research_weight"]
    for related_general_concerns_object in modify_specific_concern_params['related_general_concerns_objects']:
        specific_concern_obj.related_general_concerns.remove(related_general_concerns_object)

    specific_concern_obj.save()


def delete_instance_using_validated_params(rqst_specific_concern_id, rqst_errors):
    try:
        specific_concern_obj = ConsumerSpecificConcern.objects.get(id=rqst_specific_concern_id)
        specific_concern_obj.delete()
    except ConsumerSpecificConcern.DoesNotExist:
        rqst_errors.append("Specific concern does not exist for database id: {}".format(rqst_specific_concern_id))
