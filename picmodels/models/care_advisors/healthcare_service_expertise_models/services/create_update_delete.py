import json


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    found_rows_w_rqst_name = cls.check_for_rows_with_rqst_name(
        validated_params['name'],
        rqst_errors
    )

    new_row = None
    if not found_rows_w_rqst_name and not rqst_errors:
        new_row = cls()
        new_row.name = validated_params['name']
        new_row.save()

    return new_row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    found_rows_w_rqst_name = cls.check_for_rows_with_rqst_name(
        validated_params['name'],
        rqst_errors,
        rqst_id
    )

    rqst_row = None
    if not found_rows_w_rqst_name and not rqst_errors:
        try:
            rqst_row = cls.objects.get(id=rqst_id)
            rqst_row.name = validated_params['name']
            rqst_row.save()
        except cls.DoesNotExist:
            rqst_errors.append("Row does not exist for database id: {}".format(rqst_id))

    return rqst_row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']

    try:
        row = cls.objects.get(id=rqst_id)
        row.delete()
    except cls.DoesNotExist:
        rqst_errors.append("Row does not exist for database id: {}".format(rqst_id))


def check_for_rows_with_rqst_name(cls, rqst_name, rqst_errors, current_id=None):
    found_row_w_name = False

    rows_w_rqst_name = cls.objects.filter(name__iexact=rqst_name)

    if rows_w_rqst_name:
        found_row_w_name = True

        rows_w_rqst_name_ids = []
        len_of_rows_w_rqst_name = len(rows_w_rqst_name)
        for row in rows_w_rqst_name:
            rows_w_rqst_name_ids.append(row.id)

        if len_of_rows_w_rqst_name > 1:
            rqst_errors.append(
                "Multiple rows with name: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    rqst_name, json.dumps(rows_w_rqst_name_ids)))
        else:
            if not current_id or current_id not in rows_w_rqst_name_ids:
                rqst_errors.append(
                    "Row with name: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        rqst_name, rows_w_rqst_name_ids[0]))
            else:
                found_row_w_name = False

    return found_row_w_name
