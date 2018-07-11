from django.db.models import Max
from django.apps import apps

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
    sequence_has_this_step = check_sequence_for_current_step(cm_sequence_row, cls, rqst_errors)

    if rqst_errors:
        return None

    found_violating_rows = check_for_rows_with_given_consumer_client_and_sequence(
        cls,
        consumer_row,
        cm_client_row,
        cm_sequence_row,
        rqst_errors
    )
    if found_violating_rows:
        return None

    row.consumer = consumer_row
    row.navigator = navigator_row
    row.cm_client = cm_client_row
    row.cm_sequence = cm_sequence_row

    matching_rows_for_previous_step_found = check_previous_step_in_sequence_for_step_for_consumer(
        row,
        cls,
        rqst_errors
    )
    if rqst_errors:
        return None

    if 'notes' in validated_params:
        row.notes = validated_params['notes']

    if 'datetime_completed' in validated_params:
        row.datetime_completed = validated_params['datetime_completed']

    if 'client_appointment_datetime' in validated_params:
        row.client_appointment_datetime = validated_params['client_appointment_datetime']

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
    else:
        consumer_row = row.consumer
    if "navigator_id" in validated_params:
        navigator_row = get_navigator_row_with_given_id(validated_params["navigator_id"], rqst_errors)
    if "cm_client_id" in validated_params:
        cm_client_row = get_cm_client_row_with_given_id(validated_params["cm_client_id"], rqst_errors)
    else:
        cm_client_row = row.cm_client
    if "cm_sequence_id" in validated_params:
        cm_sequence_row = get_cm_sequence_row_with_given_id(validated_params["cm_sequence_id"], rqst_errors)
        sequence_has_this_step = check_sequence_for_current_step(cm_sequence_row, cls, rqst_errors)
    else:
        cm_sequence_row = row.cm_sequence
    if rqst_errors:
        return None

    found_violating_rows = check_for_rows_with_given_consumer_client_and_sequence(
        cls,
        consumer_row,
        cm_client_row,
        cm_sequence_row,
        rqst_errors,
        row.id
    )
    if found_violating_rows:
        return None

    if 'consumer_row' in locals():
        row.consumer = consumer_row

    if 'navigator_row' in locals():
        row.navigator = navigator_row

    if 'cm_client_row' in locals():
        row.cm_client = cm_client_row

    if 'cm_sequence_row' in locals():
        row.cm_sequence = cm_sequence_row

    matching_rows_for_previous_step_found = check_previous_step_in_sequence_for_step_for_consumer(
        row,
        cls,
        rqst_errors
    )
    if rqst_errors:
        return None

    if 'notes' in validated_params:
        row.notes = validated_params['notes']

    if 'datetime_completed' in validated_params:
        row.datetime_completed = validated_params['datetime_completed']

    if 'client_appointment_datetime' in validated_params:
        row.client_appointment_datetime = validated_params['client_appointment_datetime']

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


def check_for_rows_with_given_consumer_client_and_sequence(cls, consumer_row, client_row, sequence_row, rqst_errors, current_id=None):
    found_matching_rows = False

    matching_rows = cls.objects.filter(
        consumer=consumer_row,
        cm_client=client_row,
        cm_sequence=sequence_row,
    )

    if matching_rows:
        found_matching_rows = True

        row_ids = []
        len_of_row_qset = len(matching_rows)
        for row in matching_rows:
            row_ids.append(row.id)

        if len_of_row_qset > 1:
            rqst_errors.append(
                "Multiple rows with consumer_id: {}, cm_client_id: {}, and cm_sequence_id: {} already exist in db. (Hint - Delete all but one and modify the remaining) id's: {}".format(
                    consumer_row.id if consumer_row else consumer_row,
                    client_row.id if client_row else client_row,
                    sequence_row.id if sequence_row else sequence_row,
                    row_ids
                )
            )
        else:
            if not current_id or current_id not in row_ids:
                rqst_errors.append(
                    "Row with consumer_id: {}, cm_client_id: {}, and cm_sequence_id: {} already exists in db. (Hint - Modify that row) id: {}".format(
                        consumer_row.id if consumer_row else consumer_row,
                        client_row.id if client_row else client_row,
                        sequence_row.id if sequence_row else sequence_row,
                        row_ids[0]
                    )
                )
            else:
                found_matching_rows = False

    return found_matching_rows


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
            row = picmodels.models.CMSequences.objects.get(id=rqst_id)
        except picmodels.models.CMSequences.DoesNotExist:
            row = None
            rqst_errors.append("No CMSequence row found with id: {}".format(rqst_id))

    return row


def check_sequence_for_current_step(sequence_row, current_step_class, rqst_errors):
    sequence_has_steps = False
    steps_for_sequence = sequence_row.steps

    steps_that_match = steps_for_sequence.filter(step_class_name__iexact=current_step_class.__name__)

    if len(steps_that_match):
        sequence_has_steps = True
    else:
        rqst_errors.append(
            "Sequence with id: {} does not contain the step that this endpoint references.".format(
                sequence_row.id,
            )
        )

    return sequence_has_steps


def check_previous_step_in_sequence_for_step_for_consumer(current_step_row, current_step_class, rqst_errors):
    sequence_has_previous_step_row_for_consumer = False
    current_step_number = picmodels.models.StepsForCMSequences.objects.get(step_class_name=current_step_class.__name__).step_number
    if current_step_number == 1:
        return None

    steps_for_sequence = current_step_row.cm_sequence.steps.all()
    if len(steps_for_sequence) == 1:
        return None

    if current_step_number > 0:
        previous_step = steps_for_sequence.filter(step_number=current_step_number-1)
    else:
        step_number_before_complete = steps_for_sequence.aggregate(Max('step_number'))['step_number__max']
        previous_step = steps_for_sequence.filter(step_number=step_number_before_complete)

    if len(previous_step):
        previous_step = previous_step[0]
        previous_step_class = get_step_table_class_with_given_class_name(
            previous_step.step_class_name,
            rqst_errors
        )

        matching_previous_step_rows_for_consumer = previous_step_class.objects.filter(
            consumer=current_step_row.consumer,
            cm_sequence=current_step_row.cm_sequence,
            cm_client=current_step_row.cm_client,
        )

        if len(matching_previous_step_rows_for_consumer):
            sequence_has_previous_step_row_for_consumer = True
        else:
            rqst_errors.append(
                "There is no row in the previous step_number's table for the sequence_id: {}, client_id: {}, and consumer_id: {}.".format(
                    current_step_row.cm_sequence.id,
                    current_step_row.cm_client.id,
                    current_step_row.consumer.id,
                )
            )
    else:
        rqst_errors.append(
            "There is no step that has a step_number 1 less than the step_number of the table that this enpoint references in Sequence with id: {}'s steps.".format(
                current_step_row.cm_sequence.id,
            )
        )

    return sequence_has_previous_step_row_for_consumer


def get_step_table_class_with_given_class_name(step_class_name, rqst_errors):
    step_table_class = None

    if step_class_name:
        app_models = apps.get_app_config('picmodels').get_models()
        # app_models = get_models(apps, include_auto_created=True)

        for model in app_models:
            if model.__name__ == step_class_name:
                step_table_class = model
                break

        if not step_table_class:
            rqst_errors.append("No class found in app for given step_class_name")

    return step_table_class
