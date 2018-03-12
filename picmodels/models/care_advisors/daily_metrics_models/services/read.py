import datetime

import picmodels.models
from picmodels.models.utils import filter_db_queryset_by_id
from picmodels.models.care_advisors.navigator_models.services.read import filter_navigator_objs_by_f_and_l_name
from picmodels.models.care_advisors.navigator_models.services.read import filter_navigator_objs_by_first_name
from picmodels.models.care_advisors.navigator_models.services.read import filter_navigator_objs_by_last_name
from picmodels.models.care_advisors.navigator_models.services.read import filter_navigator_objs_by_email
from picmodels.models.care_advisors.navigator_models.services.read import filter_navigator_objs_by_mpn


def retrieve_metrics_data_by_staff_id(cls, rqst_staff_id, list_of_ids, search_params, rqst_errors, fields=None):
    staff_instances = filter_db_queryset_by_id(picmodels.models.Navigators.objects.all(), rqst_staff_id, list_of_ids)

    response_list = create_metrics_response_list_from_filtered_staff_objects_and_secondary_params(staff_instances, search_params, fields)

    def check_response_data_for_requested_data():
        missing_parameter_list = []

        if not response_list:
            rqst_errors.append("No metrics entries found in database for given staff id(s).")

            if rqst_staff_id == 'all':
                missing_parameter_list = ['all']
            else:
                missing_parameter_list = list_of_ids
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (metrics_data_entry["Staff Information"]['id'] == db_id for metrics_data_entry in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Metrics for staff Member with id: {} not found in database'.format(db_id))
                        missing_parameter_list.append(db_id)

        return missing_parameter_list

    missing_primary_parameters = check_response_data_for_requested_data()

    return response_list, missing_primary_parameters


def retrieve_metrics_data_by_staff_f_and_l_name(cls, list_of_first_names, list_of_last_names, search_params, rqst_errors, fields=None):
    response_list = []
    missing_primary_parameters = []

    if len(list_of_first_names) == len(list_of_last_names):
        for i in range(len(list_of_first_names)):
            first_name = list_of_first_names[i]
            last_name = list_of_last_names[i]

            staff_instances = filter_navigator_objs_by_f_and_l_name(picmodels.models.Navigators.objects.all(), first_name, last_name)

            response_list_component = create_metrics_response_list_from_filtered_staff_objects_and_secondary_params(staff_instances, search_params, fields)

            def check_response_data_for_requested_data():
                if not response_list_component:
                    rqst_errors.append("No metrics entries found in database for {} {}".format(first_name, last_name))
                    missing_primary_parameters.append("{} {}".format(first_name, last_name))

            check_response_data_for_requested_data()

            def add_response_component_to_response_data():
                if response_list_component:
                    response_list.append(response_list_component)

            add_response_component_to_response_data()
    else:
        rqst_errors.append('Length of first name list must be equal to length of last name list')

    return response_list, missing_primary_parameters


def retrieve_metrics_data_by_staff_first_name(cls, list_of_first_names, search_params, rqst_errors, fields=None):
    response_list = []
    missing_primary_parameters = []

    for first_name in list_of_first_names:
        staff_instances = filter_navigator_objs_by_first_name(picmodels.models.Navigators.objects.all(), first_name)

        response_list_component = create_metrics_response_list_from_filtered_staff_objects_and_secondary_params(staff_instances,
                                                                                                                search_params,
                                                                                                                fields)

        def check_response_data_for_requested_data():
            if not response_list_component:
                rqst_errors.append("No metrics entries found in database for {}".format(first_name))
                missing_primary_parameters.append(first_name)

        check_response_data_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list, missing_primary_parameters


def retrieve_metrics_data_by_staff_last_name(cls, list_of_last_names, search_params, rqst_errors, fields=None):
    response_list = []
    missing_primary_parameters = []

    for last_name in list_of_last_names:
        staff_instances = filter_navigator_objs_by_last_name(picmodels.models.Navigators.objects.all(), last_name)

        response_list_component = create_metrics_response_list_from_filtered_staff_objects_and_secondary_params(staff_instances, search_params, fields)

        def check_response_data_for_requested_data():
            if not response_list_component:
                rqst_errors.append("No metrics entries found in database for {}".format(last_name))
                missing_primary_parameters.append(last_name)

        check_response_data_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list, missing_primary_parameters


def retrieve_metrics_data_by_staff_email(cls, list_of_emails, search_params, rqst_errors, fields=None):
    response_list = []
    missing_primary_parameters = []

    for email in list_of_emails:
        staff_instances = filter_navigator_objs_by_email(picmodels.models.Navigators.objects.all(), email)

        response_list_component = create_metrics_response_list_from_filtered_staff_objects_and_secondary_params(staff_instances, search_params, fields)

        def check_response_data_for_requested_data():
            if not response_list_component:
                rqst_errors.append("No metrics entries found in database for {}".format(email))
                missing_primary_parameters.append(email)

        check_response_data_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list, missing_primary_parameters


def retrieve_metrics_data_by_staff_mpn(cls, list_of_staff_mpns, search_params, rqst_errors, fields=None):
    response_list = []
    missing_primary_parameters = []

    for staff_mpn in list_of_staff_mpns:
        staff_instances = filter_navigator_objs_by_mpn(picmodels.models.Navigators.objects.all(), staff_mpn)

        response_list_component = create_metrics_response_list_from_filtered_staff_objects_and_secondary_params(
            staff_instances, search_params, fields)

        def check_response_data_for_requested_data():
            if not response_list_component:
                rqst_errors.append("No metrics entries found in database for {}".format(staff_mpn))
                missing_primary_parameters.append(staff_mpn)

        check_response_data_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list, missing_primary_parameters


def create_metrics_response_list_from_filtered_staff_objects_and_secondary_params(staff_objects, search_params, requested_fields):
    response_list = []

    for staff_instance in staff_objects:
        response_list_entry = {"Staff Information": staff_instance.return_values_dict()}

        metrics_db_objects_for_this_staff_instance = staff_instance.metricssubmission_set.all()
        filtered_metrics_instances = filter_metrics_db_instances_by_secondary_params(search_params, metrics_db_objects_for_this_staff_instance)

        metrics_data_list = []
        for metrics_instance in filtered_metrics_instances:
            metrics_data_entry = create_metrics_data_response_entry_including_requested_fields(metrics_instance, requested_fields)
            metrics_data_list.append(metrics_data_entry)

        if metrics_data_list:
            response_list_entry["Metrics Data"] = metrics_data_list

            response_list.append(response_list_entry)

    return response_list


def create_metrics_data_response_entry_including_requested_fields(metrics_instance, requested_fields):
    complete_metrics_data_entry = metrics_instance.return_values_dict()

    filtered_metrics_data_entry = {}
    if requested_fields:
        for field in requested_fields:
            filtered_metrics_data_entry[field] = complete_metrics_data_entry[field]
    else:
        filtered_metrics_data_entry = complete_metrics_data_entry

    return filtered_metrics_data_entry


def prefetch_related_rows(db_queryset):
    db_queryset = db_queryset.select_related(
        'staff_member',
        'location',
        'location__address',
    )

    db_queryset = db_queryset.prefetch_related(
        'planstat_set',
    )

    return db_queryset


def filter_metrics_db_instances_by_secondary_params(search_params, metrics_instances):
    metrics_instances = prefetch_related_rows(metrics_instances)

    if 'zipcode_list' in search_params:
        list_of_zipcodes = search_params['zipcode_list']
        metrics_instances = metrics_instances.filter(location__address__zipcode__in=list_of_zipcodes)
    if 'time_delta_in_days' in search_params:
        time_delta_in_days = search_params['time_delta_in_days']
        begin_date = datetime.date.today() - time_delta_in_days

        metrics_instances = metrics_instances.filter(submission_date__gte=begin_date)
    if 'start_date' in search_params:
        rqst_start_date = search_params['start_date']
        metrics_instances = metrics_instances.filter(submission_date__gte=rqst_start_date)
    if 'end_date' in search_params:
        rqst_end_date = search_params['end_date']
        metrics_instances = metrics_instances.filter(submission_date__lte=rqst_end_date)
    if 'location' in search_params:
        rqst_location = search_params['location']
        metrics_instances = metrics_instances.filter(location__name__iexact=rqst_location)
    if 'location_id_list' in search_params:
        list_of_location_ids = search_params['location_id_list']
        metrics_instances = metrics_instances.filter(location__id__in=list_of_location_ids)

    return metrics_instances.order_by("submission_date")
