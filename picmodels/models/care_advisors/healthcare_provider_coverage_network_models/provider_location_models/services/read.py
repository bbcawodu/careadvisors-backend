from picmodels.models.utils import filter_db_queryset_by_id


def get_serialized_rows_by_id(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    if rqst_id != 'all':
        list_of_ids = validated_params['id_list']
    else:
        list_of_ids = None

    provider_location_qset = filter_db_queryset_by_id(cls.objects.all(), rqst_id, list_of_ids)
    provider_location_qset = prefetch_related_rows(provider_location_qset)

    response_list = create_response_list_from_db_objects(provider_location_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No provider location instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in
                                                    response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Provider location instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def get_serialized_rows_by_name(cls, validated_params, rqst_errors):
    rqst_name = validated_params['name']

    provider_location_qset = filter_provider_location_instances_by_name(cls.objects.all(), rqst_name)
    provider_location_qset = prefetch_related_rows(provider_location_qset)

    response_list = create_response_list_from_db_objects(provider_location_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No provider location instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list


def get_serialized_rows_by_network_name(cls, validated_params, rqst_errors):
    rqst_network_name = validated_params['network_name']

    provider_location_qset = filter_provider_location_instances_by_provider_network_name(
        cls.objects.all(),
        rqst_network_name
    )
    provider_location_qset = prefetch_related_rows(provider_location_qset)

    response_list = create_response_list_from_db_objects(provider_location_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No provider location instances in db for given provider network name")

    check_response_data_for_requested_data()

    return response_list


def get_serialized_rows_by_network_id(cls, validated_params, rqst_errors):
    list_of_network_ids = validated_params['network_id_list']

    response_list = []

    provider_location_qset = cls.objects.all()
    for network_id in list_of_network_ids:
        filtered_provider_location_qset = filter_provider_location_instances_by_provider_network_id(
            provider_location_qset,
            network_id
        )
        filtered_provider_location_qset = prefetch_related_rows(filtered_provider_location_qset)

        response_list_component = create_response_list_from_db_objects(filtered_provider_location_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append(
                    "No provider location instances in network for provider network with id: {}".format(network_id)
                )

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def get_serialized_rows_by_state(cls, validated_params, rqst_errors):
    list_of_states = validated_params['state_list']
    db_qset = cls.objects.all()
    response_list = []

    for state in list_of_states:
        filtered_db_qset = filter_provider_location_instances_by_state(db_qset, state)
        filtered_db_qset = prefetch_related_rows(filtered_db_qset)

        response_list_component = create_response_list_from_db_objects(filtered_db_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Hospital locations in the state: {} not found in database'.format(state))

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


def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.select_related(
        'provider_network'
    )

    db_queryset = db_queryset.prefetch_related(
        'accepted_plans'
    )

    return db_queryset


def filter_provider_location_instances_by_name(provider_location_qset, rqst_name):
    provider_location_qset = provider_location_qset.filter(name__iexact=rqst_name).order_by("name")

    return provider_location_qset


def filter_provider_location_instances_by_provider_network_name(provider_location_qset, rqst_provider_network_name):
    provider_location_qset = provider_location_qset.filter(
        provider_network__name__iexact=rqst_provider_network_name
    ).order_by("id")

    return provider_location_qset


def filter_provider_location_instances_by_provider_network_id(provider_location_qset, rqst_provider_network_id):
    provider_location_qset = provider_location_qset.filter(provider_network__id=rqst_provider_network_id).order_by("id")

    return provider_location_qset


def filter_provider_location_instances_by_state(provider_location_qset, state):
    provider_location_qset = provider_location_qset.filter(state_province__iexact=state).order_by("name")

    return provider_location_qset
