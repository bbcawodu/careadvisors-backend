import sys


def retrieve_consumer_data_by_id(cls, validated_params, rqst_errors):
    rqst_consumer_id = validated_params['id']
    if rqst_consumer_id != 'all':
        list_of_ids = validated_params['id_list']
    else:
        list_of_ids = None

    consumers = filter_consumer_qset_by_id(cls.objects.all(), rqst_consumer_id, list_of_ids)
    consumers = filter_db_objects_by_secondary_params(consumers, validated_params)

    print('Finished db query.')
    sys.stdout.flush()

    response_list = create_response_list_from_db_objects(consumers)

    print('Built response data list.')
    sys.stdout.flush()

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No consumer instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Consumer instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    print('Parsed table data for missing entries.')
    sys.stdout.flush()

    return response_list


def retrieve_consumer_data_by_f_and_l_name(cls, validated_params, rqst_errors):
    rqst_first_name = validated_params['first_name']
    rqst_last_name = validated_params['last_name']

    consumers = filter_consumer_objs_by_f_and_l_name(cls.objects.all(), rqst_first_name, rqst_last_name)
    consumers = filter_db_objects_by_secondary_params(consumers, validated_params)

    response_list = create_response_list_from_db_objects(consumers)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No consumers instances in db for given first and last name")

    check_response_data_for_requested_data()

    response_list = [response_list]

    return response_list


def retrieve_consumer_data_by_email(cls, validated_params, rqst_errors):
    list_of_emails = validated_params['email_list']
    consumers = cls.objects.all()
    consumers = filter_db_objects_by_secondary_params(consumers, validated_params)
    response_list = []

    for email in list_of_emails:
        filtered_consumers = filter_consumer_objs_by_email(consumers, email)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with email: {} not found in database'.format(email))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_consumer_data_by_first_name(cls, validated_params, rqst_errors):
    list_of_first_names = validated_params['first_name_list']
    consumers = cls.objects.all()
    consumers = filter_db_objects_by_secondary_params(consumers, validated_params)
    response_list = []

    for first_name in list_of_first_names:
        filtered_consumers = filter_consumer_objs_by_first_name(consumers, first_name)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with first name: {} not found in database'.format(first_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_consumer_data_by_last_name(cls, validated_params, rqst_errors):
    list_of_last_names = validated_params['last_name_list']
    consumers = cls.objects.all()
    consumers = filter_db_objects_by_secondary_params(consumers, validated_params)
    response_list = []

    for last_name in list_of_last_names:
        filtered_consumers = filter_consumer_objs_by_last_name(consumers, last_name)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with last name: {} not found in database'.format(last_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def filter_db_objects_by_secondary_params(db_objects, validated_GET_rqst_params):
    if 'nav_id_list' in validated_GET_rqst_params:
        list_of_nav_ids = validated_GET_rqst_params['nav_id_list']
        db_objects = db_objects.filter(navigator__in=list_of_nav_ids)
    if 'is_cps_consumer' in validated_GET_rqst_params:
        is_cps_consumer = validated_GET_rqst_params['is_cps_consumer']
        db_objects = db_objects.filter(cps_info__isnull=not is_cps_consumer)
    if 'has_hospital_info' in validated_GET_rqst_params:
        has_hospital_info = validated_GET_rqst_params['has_hospital_info']
        db_objects = db_objects.filter(consumer_hospital_info__isnull=not has_hospital_info)

    return db_objects


def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.select_related(
        'address',
        'navigator',
        # 'primary_guardian',
        'cps_info',
        'cps_info__cps_location',
        'cps_info__cps_location__address',
        'cps_info__primary_dependent',
        "consumer_hospital_info",
    )

    db_queryset = db_queryset.prefetch_related(
        'consumernote_set',
        # 'primary_guardian__picconsumer_set',
        # 'secondary_guardians',
        # 'secondary_guardians__picconsumer_set',
        'cps_info__secondary_dependents',
        "casemanagementstatus_set"
    )

    return db_queryset


def filter_consumer_qset_by_id(db_queryset, rqst_id, list_of_ids):
    db_queryset = prefetch_related_rows(db_queryset)

    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset


def filter_consumer_objs_by_f_and_l_name(db_queryset, rqst_first_name, rqst_last_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name).order_by("last_name", "first_name")

    return db_queryset


def filter_consumer_objs_by_email(db_queryset, rqst_email):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(email__iexact=rqst_email).order_by("email")

    return db_queryset


def filter_consumer_objs_by_first_name(db_queryset, rqst_first_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(first_name__iexact=rqst_first_name).order_by("first_name")

    return db_queryset


def filter_consumer_objs_by_last_name(db_queryset, rqst_last_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(last_name__iexact=rqst_last_name).order_by("last_name")

    return db_queryset
