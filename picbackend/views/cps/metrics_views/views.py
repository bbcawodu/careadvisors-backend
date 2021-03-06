from django.views.generic import View
from .tools import validate_metrics_put_rqst_params
from picmodels.models import CPSMetricsSubmission
from picbackend.views.utils import JSONPUTRspMixin
from picbackend.views.utils import JSONGETRspMixin


# Need to abstract common variables in get and post class methods into class attributes
class CPSMetricsManagementView(JSONPUTRspMixin, JSONGETRspMixin, View):
    """
    Defines views that handles Patient Innovation Center metrics instance related requests
    """

    def metrics_management_put_logic(self, rqst_body, response_raw_data, rqst_errors):
        validated_put_rqst_params = validate_metrics_put_rqst_params(rqst_body, rqst_errors)
        rqst_action = validated_put_rqst_params['rqst_action']

        if not rqst_errors:
            metrics_instance = None
            metrics_instance_message = None

            if rqst_action == "create":
                pass
                # metrics_instance, metrics_instance_message = validate_rqst_params_then_add_or_update_metrics_instance(
                #     rqst_body, rqst_errors)
            if rqst_action == "update":
                pass
                # metrics_instance, metrics_instance_message = validate_rqst_params_then_add_or_update_metrics_instance(
                #     rqst_body, rqst_errors)
            elif rqst_action == "delete":
                if rqst_action == "Instance Deletion":
                    # validate_rqst_params_and_delete_instance(rqst_body, rqst_errors)

                    if not rqst_errors:
                        response_raw_data['Data']["db_row"] = "Deleted"
            else:
                rqst_errors.append("No valid 'Database Action' provided.")

            if not rqst_errors:
                if metrics_instance and metrics_instance_message:
                    response_raw_data["Status"]["Message"] = [metrics_instance_message]

    def metrics_management_get_logic(self, request, validated_GET_rqst_params, response_raw_data, rqst_errors):
        validated_fields = retrieve_data_fields_to_return(validated_GET_rqst_params, rqst_errors)

        if not rqst_errors:
            data_list, missing_primary_parameters = retrieve_metrics_data_by_request_params(validated_GET_rqst_params, validated_fields, rqst_errors)
        else:
            data_list = []
            missing_primary_parameters = []

        response_raw_data["Data"] = data_list
        for missing_parameter in missing_primary_parameters:
            response_raw_data["Status"]["Missing Parameters"].append(missing_parameter)

    parse_PUT_request_and_add_response = metrics_management_put_logic

    accepted_GET_request_parameters = [
        "id",
        "staff_id",
        "first_name",
        "last_name",
        "email",
        "zipcode",
        "time_delta_in_days",
        "start_date",
        "end_date",
        "location",
        "location_id",
        "fields"
    ]
    parse_GET_request_and_add_response = metrics_management_get_logic


def retrieve_data_fields_to_return(validated_GET_rqst_params, rqst_errors):
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

    if 'fields list' in validated_GET_rqst_params:
        list_of_rqst_fields = validated_GET_rqst_params['fields list']
        while list_of_rqst_fields:
            rqst_field = list_of_rqst_fields.pop()
            if rqst_field in accepted_fields:
                validated_fields.append(rqst_field)
            else:
                rqst_errors.append("{!s} is not a valid metrics field".format(rqst_field))
        if not validated_fields:
            rqst_errors.append("No valid field parameters in request, returning all metrics fields.")

    return validated_fields


def retrieve_metrics_data_by_request_params(validated_GET_rqst_params, validated_fields, rqst_errors):
    data_list = []
    missing_primary_parameters = []

    if 'id' in validated_GET_rqst_params:
        rqst_id = validated_GET_rqst_params['id']
        if rqst_id != 'all':
            list_of_ids = validated_GET_rqst_params['id_list']
        else:
            list_of_ids = []

        data_list, missing_primary_parameters = CPSMetricsSubmission.retrieve_metrics_data_by_id(rqst_id, list_of_ids, validated_GET_rqst_params, rqst_errors, fields=validated_fields)
    elif 'staff_id' in validated_GET_rqst_params:
        rqst_staff_id = validated_GET_rqst_params['staff_id']
        if rqst_staff_id != 'all':
            list_of_ids = validated_GET_rqst_params['staff_id_list']
        else:
            list_of_ids = []

        data_list, missing_primary_parameters = CPSMetricsSubmission.retrieve_metrics_data_by_staff_id(rqst_staff_id, list_of_ids, validated_GET_rqst_params, rqst_errors, fields=validated_fields)
    elif 'first_name' in validated_GET_rqst_params and 'last_name' in validated_GET_rqst_params:
        list_of_first_names = validated_GET_rqst_params['first_name_list']
        list_of_last_names = validated_GET_rqst_params['last_name_list']

        data_list, missing_primary_parameters = CPSMetricsSubmission.retrieve_metrics_data_by_staff_f_and_l_name(list_of_first_names, list_of_last_names, validated_GET_rqst_params, rqst_errors, fields=validated_fields)
    elif 'first_name' in validated_GET_rqst_params:
        list_of_first_names = validated_GET_rqst_params['first_name_list']

        data_list, missing_primary_parameters = CPSMetricsSubmission.retrieve_metrics_data_by_staff_first_name(list_of_first_names, validated_GET_rqst_params, rqst_errors, fields=validated_fields)
    elif 'last_name' in validated_GET_rqst_params:
        list_of_last_names = validated_GET_rqst_params['last_name_list']

        data_list, missing_primary_parameters = CPSMetricsSubmission.retrieve_metrics_data_by_staff_last_name(list_of_last_names, validated_GET_rqst_params, rqst_errors, fields=validated_fields)
    elif 'email' in validated_GET_rqst_params:
        list_of_emails = validated_GET_rqst_params['email_list']

        data_list, missing_primary_parameters = CPSMetricsSubmission.retrieve_metrics_data_by_staff_email(list_of_emails, validated_GET_rqst_params, rqst_errors, fields=validated_fields)
    else:
        rqst_errors.append('No Valid Parameters')

    return data_list, missing_primary_parameters
