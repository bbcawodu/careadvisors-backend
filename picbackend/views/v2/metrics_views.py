"""
Defines views that handle Patient Innovation Center consumer metrics based requests
API Version 2
"""

from django.views.generic import View
from django.utils.decorators import method_decorator
from picmodels.models import MetricsSubmission
from django.views.decorators.csrf import csrf_exempt
from .utils import add_or_update_metrics_instance_using_api_rqst_params
from .utils import group_metrics_by_rqst_param
from .utils import retrieve_id_metrics
from .utils import retrieve_f_l_name_metrics
from .utils import retrieve_first_name_metrics
from .utils import retrieve_last_name_metrics
from .utils import retrieve_email_metrics
from .utils import retrieve_mpn_metrics
from .base import JSONPUTRspMixin
from .base import JSONGETRspMixin


#Need to abstract common variables in get and post class methods into class attributes
class ConsumerMetricsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center metrics instance related requests
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsumerMetricsManagementView, self).dispatch(request, *args, **kwargs)

    def metrics_management_put_logic(self, post_data, response_raw_data, post_errors):
        # Parse BODY data and add or update metrics entry
        response_raw_data = add_or_update_metrics_instance_using_api_rqst_params(response_raw_data, post_data, post_errors)

        return response_raw_data, post_errors

    def metrics_management_get_logic(self, request, search_params, response_raw_data, rqst_errors):
        # Start with this query for all and then evaluate down from request params
        # Queries arent evaluated until you read the data
        metrics_submissions = MetricsSubmission.objects.all()

        metrics_submissions = filter_db_objects_by_secondary_params(search_params, metrics_submissions)

        validated_fields = retrieve_data_fields_to_return(search_params, rqst_errors)

        metrics_dict = filter_db_objects_by_primary_params(response_raw_data, search_params, metrics_submissions,
                                                           validated_fields, rqst_errors)

        # separate_results_into_groups(response_raw_data, search_params, metrics_dict)

        convert_dict_results_into_list_results(metrics_dict, response_raw_data)

        return response_raw_data, rqst_errors

    put_logic_function = metrics_management_put_logic
    get_logic_function = metrics_management_get_logic


def filter_db_objects_by_primary_params(response_raw_data, search_params, db_objects, validated_fields, rqst_errors):
    metrics_dict = {}

    if 'id' in search_params:
        rqst_staff_id = search_params['id']
        if rqst_staff_id != 'all':
            list_of_ids = search_params['id list']
        else:
            list_of_ids = None
        metrics_dict = retrieve_id_metrics(response_raw_data, rqst_errors, db_objects, rqst_staff_id,
                                           list_of_ids, fields=validated_fields)
    elif 'first name' in search_params and 'last name' in search_params:
        rqst_fname = search_params['first name']
        rqst_lname = search_params['last name']
        list_of_first_names = search_params['first name list']
        list_of_last_names = search_params['last name list']
        metrics_dict = retrieve_f_l_name_metrics(response_raw_data, rqst_errors, db_objects,
                                                 list_of_first_names, list_of_last_names, rqst_fname, rqst_lname,
                                                 fields=validated_fields)
    elif 'first name' in search_params:
        rqst_fname = search_params['first name']
        list_of_first_names = search_params['first name list']
        metrics_dict = retrieve_first_name_metrics(response_raw_data, rqst_errors, db_objects, rqst_fname,
                                                   list_of_first_names, fields=validated_fields)
    elif 'last name' in search_params:
        rqst_lname = search_params['last name']
        list_of_last_names = search_params['last name list']
        metrics_dict = retrieve_last_name_metrics(response_raw_data, rqst_errors, db_objects, rqst_lname,
                                                  list_of_last_names, fields=validated_fields)
    elif 'email' in search_params:
        rqst_staff_email = search_params['email']
        list_of_emails = search_params['email list']
        metrics_dict = retrieve_email_metrics(response_raw_data, rqst_errors, db_objects, rqst_staff_email,
                                              list_of_emails, fields=validated_fields)
    elif 'mpn' in search_params:
        rqst_staff_mpn = search_params['mpn']
        list_of_mpns = search_params['mpn list']
        metrics_dict = retrieve_mpn_metrics(response_raw_data, rqst_errors, db_objects, rqst_staff_mpn,
                                            list_of_mpns, fields=validated_fields)

    return metrics_dict


def filter_db_objects_by_secondary_params(search_params, db_objects):
    if 'zipcode list' in search_params:
        list_of_zipcodes = search_params['zipcode list']
        db_objects = db_objects.filter(location__address__zipcode__in=list_of_zipcodes)
    if 'look up date' in search_params:
        look_up_date = search_params['look up date']
        db_objects = db_objects.filter(submission_date__gte=look_up_date)
    if 'start date' in search_params:
        rqst_start_date = search_params['start date']
        db_objects = db_objects.filter(submission_date__gte=rqst_start_date)
    if 'end date' in search_params:
        rqst_end_date = search_params['end date']
        db_objects = db_objects.filter(submission_date__lte=rqst_end_date)
    if 'location' in search_params:
        rqst_location = search_params['location']
        db_objects = db_objects.filter(location__name__iexact=rqst_location)
    if 'location_id list' in search_params:
        list_of_location_ids = search_params['location_id list']
        db_objects = db_objects.filter(location__id__in=list_of_location_ids)

    return db_objects


def retrieve_data_fields_to_return(search_params, rqst_errors):
    validated_fields = []

    accepted_fields = [
                       "Submission Date",
                       "County",
                       "Location",
                       "no_general_assis",
                       "no_plan_usage_assis",
                       "no_locating_provider_assis",
                       "no_billing_assis",
                       "no_enroll_apps_started",
                       "no_enroll_qhp",
                       "no_enroll_abe_chip",
                       "no_enroll_shop",
                       "no_referrals_agents_brokers",
                       "no_referrals_ship_medicare",
                       "no_referrals_other_assis_programs",
                       "no_referrals_issuers",
                       "no_referrals_doi",
                       "no_mplace_tax_form_assis",
                       "no_mplace_exempt_assis",
                       "no_qhp_abe_appeals",
                       "no_data_matching_mplace_issues",
                       "no_sep_eligible",
                       "no_employ_spons_cov_issues",
                       "no_aptc_csr_assis",
                       "no_cps_consumers",
                       "cmplx_cases_mplace_issues",
                       "Plan Stats"
                       ]

    if 'fields list' in search_params:
        list_of_rqst_fields = search_params['fields list']
        while list_of_rqst_fields:
            rqst_field = list_of_rqst_fields.pop()
            if rqst_field in accepted_fields:
                validated_fields.append(rqst_field)
            else:
                rqst_errors.append("{!s} is not a valid metrics field".format(rqst_field))
        if not validated_fields:
            rqst_errors.append("No valid field parameters in request, returning all metrics fields.")

    return validated_fields


def separate_results_into_groups(response_raw_data, search_params, metrics_dict):
    if "group by" in search_params:
        if search_params["group by"] == "zipcode" or search_params["group by"] == "Zipcode":
            metrics_dict = group_metrics_by_rqst_param(metrics_dict, "Zipcode")
            response_raw_data['data_dict'] = metrics_dict


def convert_dict_results_into_list_results(results_dict, response_raw_data):
    results_list = []
    for result_key, result_entry in results_dict.items():
        results_list.append(result_entry)
    response_raw_data["Data"] = results_list
