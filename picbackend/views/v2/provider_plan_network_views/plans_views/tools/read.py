from picmodels.models import ProviderLocation
from picmodels.models import HealthcareCarrier
from picmodels.models import HealthcarePlan
from picmodels.services import filter_db_queryset_by_id
from picmodels.services.provider_plan_network_services.healthcare_plan_services import filter_plan_qset_by_name
from picmodels.services.provider_plan_network_services.healthcare_plan_services import filter_plan_qset_by_carrier_name
from picmodels.services.provider_plan_network_services.healthcare_carrier_services import filter_carrier_objs_by_state


def retrieve_plan_data_by_id(search_params, rqst_plan_id, list_of_ids, rqst_errors):
    plan_qset = filter_db_queryset_by_id(HealthcarePlan.objects.all(), rqst_plan_id, list_of_ids)
    plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(search_params, plan_qset)

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


def filter_db_objects_by_secondary_params(search_params, db_objects):
    if 'include_summary_report' in search_params:
        include_summary_report_fields = search_params['include_summary_report']
    else:
        include_summary_report_fields = False
    if 'include_detailed_report' in search_params:
        include_detailed_report_fields = search_params['include_detailed_report']
    else:
        include_detailed_report_fields = False
    if 'premium_type' in search_params:
        matching_db_objects = None
        for rqst_premium_type in search_params['premium_type_list']:
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


def retrieve_plan_data_by_name(search_params, rqst_name, rqst_errors):
    plan_qset = filter_plan_qset_by_name(HealthcarePlan.objects.all(), rqst_name)
    plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(search_params, plan_qset)

    response_list = create_response_list_from_db_objects(plan_qset, include_summary_report_fields, include_detailed_report_fields)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No healthcare plan instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list


def retrieve_plan_data_by_carrier_id(search_params, list_of_carrier_ids, rqst_errors):
    response_list = []

    for carrier_id in list_of_carrier_ids:
        response_list_component = []

        try:
            carrier_instance = HealthcareCarrier.objects.get(id=carrier_id)
            plan_qset = carrier_instance.healthcareplan_set.all()
            plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(search_params, plan_qset)

            response_list_component = create_response_list_from_db_objects(plan_qset, include_summary_report_fields, include_detailed_report_fields)

            def check_response_data_for_requested_data():
                if not response_list_component:
                    rqst_errors.append("No healthcare plan instances in db for healthcare carrier with id: {}".format(carrier_id))

            check_response_data_for_requested_data()
        except HealthcareCarrier.DoesNotExist:
            rqst_errors.append("No healthcare carrier instance found for id: {}".format(carrier_id))

        def add_response_component_to_response_data():
            response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_plan_data_by_carrier_state(search_params, list_of_carrier_states, rqst_errors):
    response_list = []

    for carrier_state in list_of_carrier_states:
        response_list_component = []

        carrier_qset = filter_carrier_objs_by_state(HealthcareCarrier.objects.all(), carrier_state)
        if carrier_qset:
            plan_qset = None
            for carrier_instance in carrier_qset:
                if plan_qset:
                    plan_qset = plan_qset | carrier_instance.healthcareplan_set.all()
                else:
                    plan_qset = carrier_instance.healthcareplan_set.all()

            plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(
                search_params, plan_qset)

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


def retrieve_plan_data_by_carrier_name(search_params, rqst_carrier_name, rqst_errors):
    plan_qset = filter_plan_qset_by_carrier_name(HealthcarePlan.objects.all(), rqst_carrier_name)
    plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(
        search_params, plan_qset)

    response_list = create_response_list_from_db_objects(plan_qset, include_summary_report_fields,
                                                         include_detailed_report_fields)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No healthcare plan instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list


def retrieve_plan_data_by_accepted_location_id(search_params, list_of_accepted_location_ids, rqst_errors):
    response_list = []

    for provider_location_id in list_of_accepted_location_ids:
        response_list_component = []

        try:
            provider_location_instance = ProviderLocation.objects.get(id=provider_location_id)
            plan_qset = provider_location_instance.accepted_plans.all()
            plan_qset, include_summary_report_fields, include_detailed_report_fields = filter_db_objects_by_secondary_params(search_params, plan_qset)

            response_list_component = create_response_list_from_db_objects(plan_qset, include_summary_report_fields,
                                                                           include_detailed_report_fields)

            def check_response_data_for_requested_data():
                if not response_list_component:
                    rqst_errors.append(
                        "No healthcare plan instances in db are accepted for provider location with id: {}".format(provider_location_id))

            check_response_data_for_requested_data()
        except ProviderLocation.DoesNotExist:
            rqst_errors.append("No provider location instance found for id: {}".format(provider_location_id))

        def add_response_component_to_response_data():
            response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list
