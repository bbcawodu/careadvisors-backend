import picmodels


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    row = cls()

    consumer_row = get_consumer_row_with_given_id(validated_params["consumer_id"], rqst_errors)
    navigator_row = get_navigator_row_with_given_id(validated_params["navigator_id"], rqst_errors)

    row.status = validated_params['status']
    if not row.check_status_choices():
        rqst_errors.append(
            "status: {!s} is not a valid choice".format(row.status)
        )

    row.contact_type = validated_params['contact_type']
    if not row.check_contact_type_choices():
        rqst_errors.append(
            "contact_type: {!s} is not a valid choice".format(row.status)
        )

    if not rqst_errors:
        row.consumer = consumer_row
        row.navigator = navigator_row

        if 'notes' in validated_params:
            row.notes = validated_params['notes']

        row.save()
    else:
        row = None

    return row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']

    try:
        row = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        row = None
        rqst_errors.append('Row does not exist for the id: {}'.format(rqst_id))

    if row:
        if "consumer_id"  in validated_params:
            consumer_row = get_consumer_row_with_given_id(validated_params["consumer_id"], rqst_errors)
        if "navigator_id" in validated_params:
            navigator_row = get_navigator_row_with_given_id(validated_params["navigator_id"], rqst_errors)

        if "status" in validated_params:
            row.status = validated_params['status']
            if not row.check_status_choices():
                rqst_errors.append(
                    "status: {!s} is not a valid choice".format(row.status)
                )

        if "contact_type" in validated_params:
            row.contact_type = validated_params['contact_type']
            if not row.check_contact_type_choices():
                rqst_errors.append(
                    "contact_type: {!s} is not a valid choice".format(row.status)
                )

        if not rqst_errors:
            if 'consumer_row' in locals():
                row.consumer = consumer_row

            if 'navigator_row' in locals():
                row.navigator = navigator_row

            if 'notes' in validated_params:
                row.notes = validated_params['notes']

            row.save()
        else:
            row = None

    return row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']

    try:
        row = cls.objects.get(id=rqst_id)
        row.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Row does not exist for the id: {!s}'.format(str(rqst_id)))


def get_consumer_row_with_given_id(rqst_id, rqst_errors):
    row = None

    if rqst_id:
        try:
            row = picmodels.models.PICConsumer.objects.get(id=rqst_id)
        except picmodels.models.PICConsumer.DoesNotExist:
            row = None
            rqst_errors.append("No PICConsumer row found with id: {}".format(rqst_id))

    return row


def get_navigator_row_with_given_id(rqst_id, rqst_errors):
    row = None

    if rqst_id:
        try:
            row = picmodels.models.Navigators.objects.get(id=rqst_id)
        except picmodels.models.Navigators.DoesNotExist:
            row = None
            rqst_errors.append("No Navigators row found with id: {}".format(rqst_id))

    return row
