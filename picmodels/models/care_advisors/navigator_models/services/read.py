def get_serialized_rows_by_id(cls, validated_params, rqst_errors):
    rqst_staff_id = validated_params['id']
    if rqst_staff_id != 'all':
        list_of_ids = validated_params['id_list']
    else:
        list_of_ids = None

    navigator_qset = filter_navigator_qset_by_id(cls.objects.all(), rqst_staff_id, list_of_ids)
    navigator_qset = filter_db_objects_by_secondary_params(navigator_qset, validated_params)

    response_list = create_response_list_from_db_objects(navigator_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No navigator instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['id'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Navigator instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def get_serialized_rows_by_f_and_l_name(cls, validated_params, rqst_errors):
    rqst_first_name = validated_params['first_name']
    rqst_last_name = validated_params['last_name']

    navigator_qset = filter_navigator_objs_by_f_and_l_name(cls.objects.all(), rqst_first_name, rqst_last_name)
    navigator_qset = filter_db_objects_by_secondary_params(navigator_qset, validated_params)

    response_list = create_response_list_from_db_objects(navigator_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No navigator instances in db for given first and last name")

    check_response_data_for_requested_data()

    response_list = [response_list]

    return response_list


def get_serialized_rows_by_email(cls, validated_params, rqst_errors):
    list_of_emails = validated_params['email_list']

    response_list = []

    for email in list_of_emails:
        filtered_navigator_qset = filter_navigator_objs_by_email(cls.objects.all(), email)
        filtered_navigator_qset = filter_db_objects_by_secondary_params(filtered_navigator_qset, validated_params)

        response_list_component = create_response_list_from_db_objects(filtered_navigator_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Navigator instance with email: {} not found in database'.format(email))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def get_serialized_rows_by_first_name(cls, validated_params, rqst_errors):
    list_of_first_names = validated_params['first_name_list']

    response_list = []

    for first_name in list_of_first_names:
        filtered_navigator_qset = filter_navigator_objs_by_first_name(cls.objects.all(), first_name)
        filtered_navigator_qset = filter_db_objects_by_secondary_params(filtered_navigator_qset, validated_params)

        response_list_component = create_response_list_from_db_objects(filtered_navigator_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Navigator instance with first name: {} not found in database'.format(first_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def get_serialized_rows_by_last_name(cls, validated_params, rqst_errors):
    list_of_last_names = validated_params['last_name_list']

    response_list = []

    for last_name in list_of_last_names:
        filtered_navigator_qset = filter_navigator_objs_by_last_name(cls.objects.all(), last_name)
        filtered_navigator_qset = filter_db_objects_by_secondary_params(filtered_navigator_qset, validated_params)

        response_list_component = create_response_list_from_db_objects(filtered_navigator_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Navigator instance with last name: {} not found in database'.format(last_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def get_serialized_rows_by_county(cls, validated_params, rqst_errors):
    list_of_counties = validated_params['county_list']

    response_list = []

    for county in list_of_counties:
        filtered_navigator_qset = filter_navigator_objs_by_county(cls.objects.all(), county)
        filtered_navigator_qset = filter_db_objects_by_secondary_params(filtered_navigator_qset, validated_params)

        response_list_component = create_response_list_from_db_objects(filtered_navigator_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Navigator instances with a default county of: {} not found in database'.format(county))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def get_serialized_rows_by_region(cls, validated_params, rqst_errors):
    list_of_regions = validated_params['region_list']

    response_list = []

    counties_mapped_to_regions = cls.REGIONS
    for region in list_of_regions:
        if region not in counties_mapped_to_regions:
            rqst_errors.append("{} is not a valid region stored in the db.".format(region))
        else:
            counties_in_this_region = counties_mapped_to_regions[region]
            response_list_component = []

            for county in counties_in_this_region:
                def add_staff_data_from_county_to_response_component():
                    filtered_navigator_qset = filter_navigator_objs_by_county(cls.objects.all(), county)
                    filtered_navigator_qset = filter_db_objects_by_secondary_params(filtered_navigator_qset, validated_params)

                    staff_data_for_this_county = create_response_list_from_db_objects(filtered_navigator_qset)
                    for staff_data in staff_data_for_this_county:
                        response_list_component.append(staff_data)

                add_staff_data_from_county_to_response_component()

            def check_response_component_for_requested_data():
                if not response_list_component:
                    rqst_errors.append('Navigator instances with a default county in region: {} not found in database'.format(region))

            check_response_component_for_requested_data()

            def add_response_component_to_response_data():
                if response_list_component:
                    response_list.append(response_list_component)

            add_response_component_to_response_data()

    return response_list


def get_serialized_rows_by_mpn(cls, validated_params, rqst_errors):
    list_of_mpns = validated_params['mpn_list']

    response_list = []

    for mpn in list_of_mpns:
        filtered_navigator_qset = filter_navigator_objs_by_mpn(cls.objects.all(), mpn)
        filtered_navigator_qset = filter_db_objects_by_secondary_params(filtered_navigator_qset, validated_params)

        response_list_component = create_response_list_from_db_objects(filtered_navigator_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Navigator instance with MPN: {} not found in database'.format(mpn))

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


def filter_db_objects_by_secondary_params(db_objects, validated_get_params):
    if 'approved_cm_client_id_list' in validated_get_params:
        list_of_cm_client_ids = validated_get_params['approved_cm_client_id_list']
        db_objects = db_objects.filter(approved_cm_clients__in=list_of_cm_client_ids)

    return db_objects


def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.select_related(
        'address',
        'address__country',
    )

    db_queryset = db_queryset.prefetch_related(
        "approved_clients_for_case_management",
        'picconsumer_set',
        'base_locations',
        'base_locations__address',
        'base_locations__address__country',
        'credentialsmodel_set',
        "healthcare_locations_worked",
        "healthcare_service_expertises",
        "insurance_carrier_specialties",
        "resume_set",
        "resume_set__education_set",
        "resume_set__job_set",
    )

    return db_queryset


def filter_navigator_qset_by_id(db_queryset, rqst_id, list_of_ids):
    db_queryset = prefetch_related_rows(db_queryset)

    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset


def filter_navigator_objs_by_f_and_l_name(db_queryset, rqst_first_name, rqst_last_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(first_name__iexact=rqst_first_name, last_name__iexact=rqst_last_name).order_by(
        "last_name", "first_name")

    return db_queryset


def filter_navigator_objs_by_first_name(db_queryset, rqst_first_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(first_name__iexact=rqst_first_name).order_by("first_name")

    return db_queryset


def filter_navigator_objs_by_last_name(db_queryset, rqst_last_name):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(last_name__iexact=rqst_last_name).order_by("last_name")

    return db_queryset


def filter_navigator_objs_by_email(db_queryset, rqst_email):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(email__iexact=rqst_email).order_by("email")

    return db_queryset


def filter_navigator_objs_by_county(db_queryset, rqst_county):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(county__iexact=rqst_county).order_by("county")

    return db_queryset


def filter_navigator_objs_by_mpn(db_queryset, rqst_mpn):
    db_queryset = prefetch_related_rows(db_queryset)

    db_queryset = db_queryset.filter(mpn__iexact=rqst_mpn).order_by("mpn")

    return db_queryset
