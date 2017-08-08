import datetime


def filter_metrics_db_instances_by_secondary_params(search_params, metrics_instances):
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
