import picmodels


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    if 'name' not in validated_params:
        rqst_errors.append("'name' is a required key in the validated_params argument")
        return None

    if cls.check_for_rows_with_given_name(validated_params['name'], rqst_errors):
        return None

    row = cls()
    row.name = validated_params['name']
    row.save()

    if 'add_steps' in validated_params:
        steps_info = validated_params['add_steps']
        cmstepsforsequences_rows = []
        for step_id in steps_info:
            cmstepsforsequences_rows.append(
                get_stepsforcmsequences_row_with_given_id(step_id, rqst_errors)
            )
        if not rqst_errors:
            check_steps_for_given_rows_or_matching_step_number(
                row.steps.all(),
                cmstepsforsequences_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for step_row in cmstepsforsequences_rows:
                    row.steps.add(step_row)
    if rqst_errors:
        row.delete()
        return None

    row.save()

    return row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    if 'id' not in validated_params:
        rqst_errors.append("'id' is a required key in the validated_params argument")
        return None

    rqst_id = validated_params['id']

    try:
        row = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        rqst_errors.append('Row does not exist for the id: {}'.format(rqst_id))
        return None

    if 'add_steps' in validated_params:
        steps_info = validated_params['add_steps']
        cmstepsforsequences_rows = []
        for step_id in steps_info:
            cmstepsforsequences_rows.append(
                get_stepsforcmsequences_row_with_given_id(step_id, rqst_errors)
            )
        if not rqst_errors:
            check_steps_for_given_rows_or_matching_step_number(
                row.steps.all(),
                cmstepsforsequences_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for step_row in cmstepsforsequences_rows:
                    row.steps.add(step_row)
    elif 'remove_steps' in validated_params:
        steps_info = validated_params['remove_steps']
        cmstepsforsequences_rows = []
        for step_id in steps_info:
            cmstepsforsequences_rows.append(
                get_stepsforcmsequences_row_with_given_id(step_id, rqst_errors)
            )
        if not rqst_errors:
            check_steps_for_not_given_rows(
                row.steps.all(),
                cmstepsforsequences_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for step_row in cmstepsforsequences_rows:
                    row.steps.remove(step_row)
    if rqst_errors:
        return None

    if 'name' in validated_params:
        row.name = validated_params['name']

    if cls.check_for_rows_with_given_name(row.name, rqst_errors, rqst_id):
        return None

    row.save()

    return row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    if 'id' not in validated_params:
        rqst_errors.append("'id' is a required key in the validated_params argument")
        return

    rqst_id = validated_params['id']

    try:
        row = cls.objects.get(id=rqst_id)
        row.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Row does not exist for the id: {!s}'.format(str(rqst_id)))


def check_for_rows_with_given_name(cls, name, rqst_errors, current_id=None):
    found_matching_rows = False

    matching_rows = cls.objects.filter(
        name__iexact=name
    )

    if matching_rows:
        found_matching_rows = True

        row_ids = []
        len_of_row_qset = len(matching_rows)
        for row in matching_rows:
            row_ids.append(row.id)

        if len_of_row_qset > 1:
            rqst_errors.append(
                "Multiple rows with name: {} already exist in db. (Hint - Delete all but one and modify the remaining) id's: {}".format(
                    name, row_ids))
        else:
            if not current_id or current_id not in row_ids:
                rqst_errors.append(
                    "Row with name: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        name, row_ids[0]))
            else:
                found_matching_rows = False

    return found_matching_rows


def get_stepsforcmsequences_row_with_given_id(row_id, rqst_errors):
    row = None

    if row_id:
        try:
            row = picmodels.models.StepsForCMSequences.objects.get(id=row_id)
        except picmodels.models.StepsForCMSequences.DoesNotExist:
            row = None
            rqst_errors.append("No StepsForCMSequences row found with id: {}".format(row_id))

    return row


def check_steps_for_given_rows_or_matching_step_number(cur_steps_qset, given_steps_list, row, rqst_errors):
    for cm_step in given_steps_list:
        if rqst_errors:
            break

        if cm_step in cur_steps_qset:
            rqst_errors.append(
                "cm_step with id: {} already exists in row id {}'s steps list (Hint - remove from parameter 'add_steps' list)".format(
                    cm_step.id,
                    row.id,
                )
            )
        else:
            check_steps_for_row_with_given_step_number(cur_steps_qset, cm_step, row, rqst_errors)


def check_steps_for_not_given_rows(cur_steps_qset, given_steps_list, row, rqst_errors):
    for cm_step in given_steps_list:
        if cm_step not in cur_steps_qset:
            rqst_errors.append(
                "cm_step with id: {} does not exists in row id {}'s steps list (Hint - remove from parameter 'remove_stepst' list)".format(
                    cm_step.id,
                    row.id,
                )
            )


def check_steps_for_row_with_given_step_number(cur_steps_qset, given_step_row, row, rqst_errors):
    for cm_step in cur_steps_qset:
        if cm_step.step_number == given_step_row.step_number:
            rqst_errors.append(
                "cm_step with id: {} has a step_number of: {}, which already exists in row id {}'s steps list (Hint - remove from parameter 'add_steps' list)".format(
                    given_step_row.id,
                    given_step_row.step_number,
                    row.id,
                )
            )
            break
