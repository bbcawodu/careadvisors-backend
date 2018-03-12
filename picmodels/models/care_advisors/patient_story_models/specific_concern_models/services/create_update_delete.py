import json


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    found_specific_concern_rows = cls.check_for_specific_concern_rows_with_given_question(
        validated_params["rqst_specific_concern_question"],
        rqst_errors
    )

    specific_concern_row = None
    if not found_specific_concern_rows and not rqst_errors:
        specific_concern_row = cls()
        specific_concern_row.question = validated_params["rqst_specific_concern_question"]
        specific_concern_row.research_weight = validated_params["rqst_specific_concern_research_weight"]
        specific_concern_row.save()

        if "add_related_general_concerns_objects" in validated_params:
            add_related_general_concerns_to_row(specific_concern_row, validated_params, rqst_errors)

        if not rqst_errors:
            specific_concern_row.save()

    return specific_concern_row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    if "rqst_specific_concern_question" in validated_params:
        found_specific_concern_rows = cls.check_for_specific_concern_rows_with_given_question(
            validated_params["rqst_specific_concern_question"],
            rqst_errors,
            rqst_id
        )
    else:
        found_specific_concern_rows = None

    specific_concern_row = None
    if not found_specific_concern_rows and not rqst_errors:
        try:
            specific_concern_row = cls.objects.get(id=rqst_id)

            if "rqst_specific_concern_question" in validated_params:
                specific_concern_row.question = validated_params["rqst_specific_concern_question"]
            if "rqst_specific_concern_research_weight" in validated_params:
                specific_concern_row.research_weight = validated_params["rqst_specific_concern_research_weight"]

            if "add_related_general_concerns_objects" in validated_params:
                add_related_general_concerns_to_row(specific_concern_row, validated_params, rqst_errors)
            elif "remove_related_general_concerns_objects" in validated_params:
                remove_related_general_concerns_from_row(specific_concern_row, validated_params, rqst_errors)

            if not rqst_errors:
                specific_concern_row.save()
        except cls.DoesNotExist:
            rqst_errors.append("Specific concern does not exist for database id: {}".format(rqst_id))

    return specific_concern_row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        specific_concern_obj = cls.objects.get(id=rqst_id)
        specific_concern_obj.delete()
    except cls.DoesNotExist:
        rqst_errors.append("Specific concern does not exist for database id: {}".format(rqst_id))


def check_for_specific_concern_rows_with_given_question(cls, specific_concern_question, post_errors, current_specific_concern_id=None):
    found_specific_concern_obj = False

    specific_concern_objs = cls.objects.filter(question__iexact=specific_concern_question)

    if specific_concern_objs:
        found_specific_concern_obj = True

        specific_concern_ids = []
        len_of_specific_concerns_qset = len(specific_concern_objs)
        for specific_concern_obj in specific_concern_objs:
            specific_concern_ids.append(specific_concern_obj.id)

        if len_of_specific_concerns_qset > 1:
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


def add_related_general_concerns_to_row(specific_concern_row, validated_params, rqst_errors):
    related_general_concerns_rows = validated_params["add_related_general_concerns_objects"]
    if related_general_concerns_rows:
        check_related_general_concerns_for_given_rows(specific_concern_row, related_general_concerns_rows, rqst_errors)

        for related_general_concerns_row in related_general_concerns_rows:
            specific_concern_row.related_general_concerns.add(related_general_concerns_row)


def remove_related_general_concerns_from_row(specific_concern_row, validated_params, rqst_errors):
    related_general_concerns_rows = validated_params["remove_related_general_concerns_objects"]
    check_related_general_concerns_for_not_given_rows(
        specific_concern_row,
        related_general_concerns_rows,
        rqst_errors
    )

    for related_general_concerns_row in related_general_concerns_rows:
        specific_concern_row.related_general_concerns.remove(related_general_concerns_row)


def check_related_general_concerns_for_given_rows(specific_concern_row, related_general_concerns_rows, rqst_errors):
    cur_related_general_concerns_qset = specific_concern_row.related_general_concerns.all()
    for related_general_concerns_object in related_general_concerns_rows:
        if related_general_concerns_object in cur_related_general_concerns_qset:
            rqst_errors.append(
                "Related general concern with the following name already exists in db id {}'s related_general_concerns list (Hint - remove from parameter 'related_general_concerns' list): {})".format(
                    specific_concern_row.id, related_general_concerns_object.name
                )
            )


def check_related_general_concerns_for_not_given_rows(specific_concern_rows, related_general_concerns_rows, rqst_errors):
    cur_related_general_concerns_qset = specific_concern_rows.related_general_concerns.all()
    for related_general_concerns_object in related_general_concerns_rows:
        if related_general_concerns_object not in cur_related_general_concerns_qset:
            rqst_errors.append(
                "Related general concern with the following name does not exist in db id {}'s related_general_concerns list (Hint - remove from parameter 'related_general_concerns' list): {})".format(
                    specific_concern_rows.id, related_general_concerns_object.name
                )
            )
