import picmodels.models

from picmodels.models.care_advisors.healthcare_provider_coverage_network_models.coverage_carrier_models.services.read import filter_carrier_objs_by_state


def retrieve_plan_data_by_id(cls, validated_params, rqst_plan_id, list_of_ids, rqst_errors):
    plan_qset = filter_plan_qset_by_id(cls.objects.all(), rqst_plan_id, list_of_ids, validated_params)
    plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(validated_params, plan_qset)

    response_list = create_response_list_from_db_objects(plan_qset, include_summary_report_fields, include_detailed_report_fields)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No healthcare plan instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in
                                                    response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Healthcare plan instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def retrieve_plan_data_by_name(cls, validated_params, rqst_name, rqst_errors):
    plan_qset = filter_plan_qset_by_name(cls.objects.all(), rqst_name, validated_params)
    plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(validated_params, plan_qset)

    response_list = create_response_list_from_db_objects(plan_qset, include_summary_report_fields, include_detailed_report_fields)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No healthcare plan instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list


def retrieve_plan_data_by_carrier_name(cls, validated_params, rqst_carrier_name, rqst_errors):
    plan_qset = filter_plan_qset_by_carrier_name(cls.objects.all(), rqst_carrier_name, validated_params)
    plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(
        validated_params,
        plan_qset
    )

    response_list = create_response_list_from_db_objects(plan_qset, include_summary_report_fields,
                                                         include_detailed_report_fields)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No healthcare plan instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list


def retrieve_plan_data_by_carrier_id(cls, validated_params, list_of_carrier_ids, rqst_errors):
    response_list = []

    for carrier_id in list_of_carrier_ids:
        response_list_component = []

        try:
            carrier_instance = picmodels.models.HealthcareCarrier.objects.get(id=carrier_id)
            plan_qset = carrier_instance.healthcareplan_set.all()
            plan_qset = prefetch_related_rows(plan_qset, validated_params)
            plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(validated_params, plan_qset)

            response_list_component = create_response_list_from_db_objects(plan_qset, include_summary_report_fields, include_detailed_report_fields)

            def check_response_data_for_requested_data():
                if not response_list_component:
                    rqst_errors.append("No healthcare plan instances in db for healthcare carrier with id: {}".format(carrier_id))

            check_response_data_for_requested_data()
        except picmodels.models.HealthcareCarrier.DoesNotExist:
            rqst_errors.append("No healthcare carrier instance found for id: {}".format(carrier_id))

        def add_response_component_to_response_data():
            response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_plan_data_by_carrier_state(cls, validated_params, list_of_carrier_states, rqst_errors):
    response_list = []

    for carrier_state in list_of_carrier_states:
        response_list_component = []

        carrier_qset = filter_carrier_objs_by_state(picmodels.models.HealthcareCarrier.objects.all(), carrier_state)
        if len(carrier_qset):
            plan_qset = None
            for carrier_instance in carrier_qset:
                if plan_qset:
                    plan_qset = plan_qset | carrier_instance.healthcareplan_set.all()
                else:
                    plan_qset = carrier_instance.healthcareplan_set.all()
            plan_qset = prefetch_related_rows(plan_qset, validated_params)

            plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(
                validated_params, plan_qset)

            response_list_component = create_response_list_from_db_objects(plan_qset, include_summary_report_fields,
                                                                           include_detailed_report_fields)

            def check_response_data_for_requested_data():
                if not response_list_component:
                    rqst_errors.append(
                        "No healthcare plan instances in db for healthcare carriers in state: {}".format(carrier_state))

            check_response_data_for_requested_data()
        else:
            rqst_errors.append("No healthcare carrier instances for state: {}".format(carrier_state))

        def add_response_component_to_response_data():
            response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_plan_data_by_accepted_location_id(cls, validated_params, list_of_accepted_location_ids, rqst_errors):
    response_list = []

    for provider_location_id in list_of_accepted_location_ids:
        response_list_component = []

        try:
            provider_location_instance = picmodels.models.ProviderLocation.objects.get(id=provider_location_id)
            plan_qset = provider_location_instance.accepted_plans.all()
            plan_qset = prefetch_related_rows(plan_qset, validated_params)
            plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(validated_params, plan_qset)

            response_list_component = create_response_list_from_db_objects(plan_qset, include_summary_report_fields,
                                                                           include_detailed_report_fields)

            def check_response_data_for_requested_data():
                if not response_list_component:
                    rqst_errors.append(
                        "No healthcare plan instances in db are accepted for provider location with id: {}".format(provider_location_id))

            check_response_data_for_requested_data()
        except picmodels.models.ProviderLocation.DoesNotExist:
            rqst_errors.append("No provider location instance found for id: {}".format(provider_location_id))

        def add_response_component_to_response_data():
            response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def filter_db_objects_by_secondary_params(validated_params, db_objects):
    if 'include_summary_report' in validated_params:
        include_summary_report_fields = validated_params['include_summary_report']
    else:
        include_summary_report_fields = False
    if 'include_detailed_report' in validated_params:
        include_detailed_report_fields = validated_params['include_detailed_report']
    else:
        include_detailed_report_fields = False

    if 'premium_type' in validated_params:
        matching_db_objects = None
        for rqst_premium_type in validated_params['premium_type_list']:
            if matching_db_objects:
                matching_db_objects = matching_db_objects | db_objects.filter(premium_type__iexact=rqst_premium_type)
            else:
                matching_db_objects = db_objects.filter(premium_type__iexact=rqst_premium_type)
        db_objects = matching_db_objects

    return db_objects, include_summary_report_fields, include_detailed_report_fields


def create_response_list_from_db_objects(db_qset, include_summary_report=False, include_detailed_report=False):
    return_list = []

    for db_instance in db_qset:
        return_list.append(db_instance.return_values_dict(include_summary_report=include_summary_report, include_detailed_report=include_detailed_report))

    return return_list


def prefetch_related_rows(db_queryset, validated_params):
    db_queryset = db_queryset.select_related(
        'carrier',
    )

    if 'include_summary_report' in validated_params:
        include_summary_report_fields = validated_params['include_summary_report']
    else:
        include_summary_report_fields = False
    if 'include_detailed_report' in validated_params:
        include_detailed_report_fields = validated_params['include_detailed_report']
    else:
        include_detailed_report_fields = False

    if include_summary_report_fields:
        db_queryset = db_queryset.prefetch_related("primary_care_physician_standard_cost")
    if include_detailed_report_fields:
        db_queryset = db_queryset.prefetch_related(
            "specialist_standard_cost",
            "emergency_room_standard_cost",
            "inpatient_facility_standard_cost",
            "generic_drugs_standard_cost",
            "preferred_brand_drugs_standard_cost",
            "non_preferred_brand_drugs_standard_cost",
            "specialty_drugs_standard_cost"
        )

    return db_queryset


def filter_plan_qset_by_id(db_queryset, rqst_id, list_of_ids, validated_params):
    db_queryset = prefetch_related_rows(db_queryset, validated_params)

    if isinstance(rqst_id, str) and rqst_id.lower() == "all":
        db_queryset = db_queryset.order_by("id")
    else:
        db_queryset = db_queryset.filter(id__in=list_of_ids).order_by("id")

    return db_queryset


def filter_plan_qset_by_name(db_queryset, rqst_name, validated_params):
    db_queryset = prefetch_related_rows(db_queryset, validated_params)

    db_queryset = db_queryset.filter(name__iexact=rqst_name).order_by("name")

    return db_queryset


def filter_plan_qset_by_carrier_name(db_queryset, rqst_carrier_name, validated_params):
    db_queryset = prefetch_related_rows(db_queryset, validated_params)

    db_queryset = db_queryset.filter(carrier__name__iexact=rqst_carrier_name).order_by("id")

    return db_queryset

