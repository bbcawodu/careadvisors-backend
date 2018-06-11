def create_row_w_validated_params(cls, validated_params, rqst_errors):
    if 'name' not in validated_params:
        rqst_errors.append("'name' is a required key in the validated_params argument")
        return None

    if not cls.check_for_rows_with_given_name(validated_params['name'], rqst_errors):
        row = cls()
        row.name = validated_params['name']
        row.save()
    else:
        row = None
        rqst_errors.append(
            'Row already exists for the name: {}'.format(
                validated_params['name']
            )
        )

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

    if 'name' in validated_params:
        row.name = validated_params['name']

    if not cls.check_for_rows_with_given_name(row.name, rqst_errors, rqst_id):
        row.save()
    else:
        row = None
        rqst_errors.append(
            'Row already exists for the name: {}'.format(
                validated_params['name']
            )
        )

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
