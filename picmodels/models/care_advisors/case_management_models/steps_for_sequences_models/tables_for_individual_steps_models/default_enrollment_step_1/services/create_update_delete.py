import picmodels


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    if "consumer_id" not in validated_params:
        rqst_errors.append("'consumer_id' is a required key in the validated_params argument")
        return None
    if "navigator_id" not in validated_params:
        rqst_errors.append("'navigator_id' is a required key in the validated_params argument")
        return None
    if "cm_client_id" not in validated_params:
        rqst_errors.append("'cm_client_id' is a required key in the validated_params argument")
        return None
    if "cm_sequence_id" not in validated_params:
        rqst_errors.append("'cm_sequence_id' is a required key in the validated_params argument")
        return None

    row = cls()

    consumer_row = get_consumer_row_with_given_id(validated_params["consumer_id"], rqst_errors)
    navigator_row = get_navigator_row_with_given_id(validated_params["navigator_id"], rqst_errors)
    cm_client_row = get_cm_client_row_with_given_id(validated_params["cm_client_id"], rqst_errors)
    cm_sequence_row = get_cm_sequence_row_with_given_id(validated_params["cm_sequence_id"], rqst_errors)
    if rqst_errors:
        return None

    row.consumer = consumer_row
    row.navigator = navigator_row
    row.cm_client = cm_client_row
    row.cm_sequence = cm_sequence_row

    if 'notes' in validated_params:
        row.notes = validated_params['notes']

    if 'tracking_no' in validated_params:
        row.tracking_no = validated_params['tracking_no']

    if 'user_name' in validated_params:
        row.user_name = validated_params['user_name']

    if 'datetime_completed' in validated_params:
        row.datetime_completed = validated_params['datetime_completed']

    row.save()

    return row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    if "id" in validated_params:
        rqst_id = validated_params['id']
    else:
        rqst_errors.append("'id' is a required key in the validated_params argument")
        return None

    try:
        row = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        rqst_errors.append('Row does not exist for the id: {}'.format(rqst_id))
        return None

    if "consumer_id"  in validated_params:
        consumer_row = get_consumer_row_with_given_id(validated_params["consumer_id"], rqst_errors)
    if "navigator_id" in validated_params:
        navigator_row = get_navigator_row_with_given_id(validated_params["navigator_id"], rqst_errors)
    if "cm_client_id" in validated_params:
        cm_client_row = get_cm_client_row_with_given_id(validated_params["cm_client_id"], rqst_errors)
    if "cm_sequence_id" in validated_params:
        cm_sequence_row = get_cm_sequence_row_with_given_id(validated_params["cm_sequence_id"], rqst_errors)

    if rqst_errors:
        return None

    if 'consumer_row' in locals():
        row.consumer = consumer_row

    if 'navigator_row' in locals():
        row.navigator = navigator_row

    if 'cm_client_row' in locals():
        row.cm_client = cm_client_row

    if 'cm_sequence_row' in locals():
        row.cm_sequence = cm_sequence_row

    if 'notes' in validated_params:
        row.notes = validated_params['notes']

    if 'tracking_no' in validated_params:
        row.tracking_no = validated_params['tracking_no']

    if 'user_name' in validated_params:
        row.user_name = validated_params['user_name']

    if 'datetime_completed' in validated_params:
        row.datetime_completed = validated_params['datetime_completed']

    row.save()

    return row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    if "id" in validated_params:
        rqst_id = validated_params['id']
    else:
        rqst_errors.append("'id' is a required key in the validated_params argument")
        return None

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


def get_cm_client_row_with_given_id(rqst_id, rqst_errors):
    row = None

    if rqst_id:
        try:
            row = picmodels.models.CaseManagementClient.objects.get(id=rqst_id)
        except picmodels.models.CaseManagementClient.DoesNotExist:
            row = None
            rqst_errors.append("No CaseManagementClient row found with id: {}".format(rqst_id))

    return row


def get_cm_sequence_row_with_given_id(rqst_id, rqst_errors):
    row = None

    if rqst_id:
        try:
            row = picmodels.models.CMSequence.objects.get(id=rqst_id)
        except picmodels.models.CMSequence.DoesNotExist:
            row = None
            rqst_errors.append("No CMSequence row found with id: {}".format(rqst_id))

    return row
