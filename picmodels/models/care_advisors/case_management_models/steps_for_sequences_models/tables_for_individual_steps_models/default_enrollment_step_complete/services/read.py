import sys


def get_serialized_rows_by_id(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    if rqst_id != 'all':
        list_of_ids = validated_params['id_list']
    else:
        list_of_ids = None

    db_objects = prefetch_related_rows(cls.objects.all())
    db_objects = filter_qset_by_id(db_objects, rqst_id, list_of_ids)
    db_objects = filter_db_objects_by_secondary_params(db_objects, validated_params)

    response_list = create_response_list_from_db_objects(db_objects)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No rows in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['id'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('row with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    sys.stdout.flush()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def filter_db_objects_by_secondary_params(db_objects, validated_get_params):
    if 'consumer_id_list' in validated_get_params:
        list_of_consumer_ids = validated_get_params['consumer_id_list']
        db_objects = db_objects.filter(consumer__in=list_of_consumer_ids)
    if 'nav_id_list' in validated_get_params:
        list_of_nav_ids = validated_get_params['nav_id_list']
        db_objects = db_objects.filter(navigator__in=list_of_nav_ids)
    if 'cm_client_id_list' in validated_get_params:
        if validated_get_params['cm_client_id'] == 'all':
            db_objects = db_objects.filter(cm_client__isnull=False)
        elif validated_get_params['cm_client_id'] == 'none':
            db_objects = db_objects.filter(cm_client__isnull=True)
        else:
            list_of_cm_client_ids = validated_get_params['cm_client_id_list']
            db_objects = db_objects.filter(cm_client__in=list_of_cm_client_ids)
    if 'cm_sequence_id_list' in validated_get_params:
        if validated_get_params['cm_sequence_id'] == 'all':
            db_objects = db_objects.filter(cm_sequence__isnull=False)
        else:
            list_of_cm_sequence_ids = validated_get_params['cm_sequence_id_list']
            db_objects = db_objects.filter(cm_sequence__in=list_of_cm_sequence_ids)

    if 'date_created_start' in validated_get_params:
        date_created_start = validated_get_params['date_created_start']
        db_objects = db_objects.filter(date_created__gte=date_created_start)
    if 'date_created_end' in validated_get_params:
        date_created_end = validated_get_params['date_created_end']
        db_objects = db_objects.filter(date_created__lte=date_created_end)

    if 'date_modified_start' in validated_get_params:
        date_modified_start = validated_get_params['date_modified_start']
        db_objects = db_objects.filter(date_modified__gte=date_modified_start)
    if 'date_modified_end' in validated_get_params:
        date_modified_end = validated_get_params['date_modified_end']
        db_objects = db_objects.filter(date_modified__lte=date_modified_end)

    if 'client_appointment_datetime_start_date' in validated_get_params:
        client_appointment_datetime_start_date = validated_get_params['client_appointment_datetime_start_date']
        db_objects = db_objects.filter(client_appointment_datetime__gte=client_appointment_datetime_start_date)
    if 'client_appointment_datetime_end_date' in validated_get_params:
        client_appointment_datetime_end_date = validated_get_params['client_appointment_datetime_end_date']
        db_objects = db_objects.filter(client_appointment_datetime__lte=client_appointment_datetime_end_date)

    if 'datetime_completed_start_date' in validated_get_params:
        datetime_completed_start_date = validated_get_params['datetime_completed_start_date']
        db_objects = db_objects.filter(datetime_completed__gte=datetime_completed_start_date)
    if 'datetime_completed_end_date' in validated_get_params:
        datetime_completed_end_date = validated_get_params['datetime_completed_end_date']
        db_objects = db_objects.filter(datetime_completed__lte=datetime_completed_end_date)

    return db_objects


def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.select_related(
        'consumer',
        'cm_client',
        'cm_sequence',
        'navigator',
    )

    return db_queryset


def filter_qset_by_id(db_queryset, rqst_id, list_of_ids):
    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset
