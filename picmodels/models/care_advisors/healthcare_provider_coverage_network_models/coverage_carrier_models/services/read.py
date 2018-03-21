from django.conf import settings


def get_serialized_rows_by_id(cls, validated_params, rqst_errors):
    rqst_carrier_id = validated_params['id']
    if rqst_carrier_id != 'all':
        list_of_ids = validated_params['id_list']
    else:
        list_of_ids = None

    carrier_qset = filter_carrier_qset_by_id(cls.objects.all(), rqst_carrier_id, list_of_ids)
    carrier_qset = prefetch_related_rows(carrier_qset)
    carrier_qset = filter_results_by_secondary_params(validated_params, carrier_qset)

    response_list = create_response_list_from_db_objects(carrier_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No carrier instances in db for given ids.")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Carrier instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def get_serialized_rows_by_state(cls, validated_params, rqst_errors):
    list_of_states = validated_params['state_list']
    carrier_qset = cls.objects.all()
    carrier_qset = prefetch_related_rows(carrier_qset)
    response_list = []

    for state in list_of_states:
        filtered_carrier_qset = filter_carrier_objs_by_state(carrier_qset, state)
        filtered_carrier_qset = filter_results_by_secondary_params(validated_params, filtered_carrier_qset)

        response_list_component = create_response_list_from_db_objects(filtered_carrier_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Carriers in the state: {} not found in database'.format(state))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def get_serialized_rows_by_name(cls, validated_params, rqst_errors):
    rqst_name = validated_params['name']

    carrier_qset = filter_carrier_objs_by_name(cls.objects.all(), rqst_name)
    carrier_qset = prefetch_related_rows(carrier_qset)
    carrier_qset = filter_results_by_secondary_params(validated_params, carrier_qset)

    response_list = create_response_list_from_db_objects(carrier_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No carrier instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.prefetch_related('healthcareplan_set')

    return db_queryset


def filter_carrier_qset_by_id(db_queryset, rqst_id, list_of_ids):
    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset


def filter_carrier_objs_by_state(db_queryset, state):
    db_queryset = db_queryset.filter(state_province__iexact=state).order_by("state_province")

    return db_queryset


def filter_carrier_objs_by_name(db_queryset, name):
    db_queryset = db_queryset.filter(name__iexact=name).order_by("name")

    return db_queryset


def filter_results_by_secondary_params(validated_params, rows):
    if 'has_sample_id_card' in validated_params:
        carriers_have_sample_id_cards = validated_params['has_sample_id_card']

        if carriers_have_sample_id_cards:
            rows = rows.exclude(sample_id_card=settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)
        else:
            rows = rows.filter(sample_id_card=settings.DEFAULT_CARRIER_SAMPLE_ID_CARD_URL)

    return rows
