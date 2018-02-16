"""
Defines utility functions and classes for consumer metrics views
"""

import datetime

from picbackend.views.utils import clean_dict_value_from_dict_object
from picbackend.views.utils import clean_int_value_from_dict_object
from picbackend.views.utils import clean_list_value_from_dict_object
from picbackend.views.utils import clean_string_value_from_dict_object

from picmodels.models import NavMetricsLocation
from picmodels.models import PlanStat


def validate_put_rqst_params(rqst_body, rqst_errors):
    validated_params = {
        'rqst_action': clean_string_value_from_dict_object(rqst_body, "root", "db_action", rqst_errors, no_key_allowed=True)
    }

    rqst_action = validated_params['rqst_action']

    if rqst_action == 'delete':
        validated_params['rqst_id'] = clean_int_value_from_dict_object(rqst_body, "root", "id", rqst_errors)
    else:
        validate_create_or_update_row_params(rqst_body, validated_params, rqst_errors)

    return validated_params


def validate_create_or_update_row_params(rqst_body, validated_params, rqst_errors):
    consumer_metrics = clean_dict_value_from_dict_object(rqst_body, "root", "Consumer Metrics", rqst_errors)
    if not consumer_metrics:
        consumer_metrics = {}

    rqst_no_cps_consumers = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics",
                                                             "no_cps_consumers",
                                                             rqst_errors, no_key_allowed=True)
    if rqst_no_cps_consumers is None:
        rqst_no_cps_consumers = 0

    rqst_metrics_location = clean_string_value_from_dict_object(consumer_metrics, "Consumer Metrics", "Location",
                                                                 rqst_errors)
    location_instance = None
    try:
        location_instance = NavMetricsLocation.objects.get(name=rqst_metrics_location)
    except NavMetricsLocation.DoesNotExist:
        rqst_errors.append("Location instance does not exist for given location name: {!s}.".format(rqst_metrics_location))
    except NavMetricsLocation.MultipleObjectsReturned:
        rqst_errors.append("Multiple location instances exist for given location name: {!s}".format(rqst_metrics_location))

    metrics_date_dict = clean_dict_value_from_dict_object(consumer_metrics, "Consumer Metrics", "Metrics Date",
                                                          rqst_errors)
    metrics_date = None
    if metrics_date_dict is not None:
        month = clean_int_value_from_dict_object(metrics_date_dict, "Metrics Date", "Month", rqst_errors)
        if month:
            if month < 1 or month > 12:
                rqst_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_int_value_from_dict_object(metrics_date_dict, "Metrics Date", "Day", rqst_errors)
        if day:
            if day < 1 or day > 31:
                rqst_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_int_value_from_dict_object(metrics_date_dict, "Metrics Date", "Year", rqst_errors)
        if year:
            if year < 1 or year > 9999:
                rqst_errors.append("Year must be between 1 and 9999 inclusive")

        if not rqst_errors:
            metrics_date = datetime.date(year, month, day)

    rqst_plan_stats = clean_list_value_from_dict_object(consumer_metrics, "Consumer Metrics", "Plan Stats", rqst_errors, empty_list_allowed=True)
    unsaved_plan_stat_objs = []
    if rqst_plan_stats:
        for rqst_plan_stat_dict in rqst_plan_stats:
            planstatobject = PlanStat()
            planstatobject.plan_name = clean_string_value_from_dict_object(rqst_plan_stat_dict, "Plans Dict",
                                                                           "Issuer Name", rqst_errors)
            planstatobject.premium_type = clean_string_value_from_dict_object(rqst_plan_stat_dict, "Plans Dict",
                                                                              "Premium Type", rqst_errors)
            planstatobject.metal_level = clean_string_value_from_dict_object(rqst_plan_stat_dict, "Plans Dict",
                                                                             "Metal Level", rqst_errors)
            planstatobject.enrollments = clean_int_value_from_dict_object(rqst_plan_stat_dict, "Plans Dict",
                                                                          "Enrollments", rqst_errors)

            plan_name_valid = planstatobject.check_plan_choices()
            premium_type_valid = planstatobject.check_premium_choices()
            metal_level_valid = planstatobject.check_metal_choices()
            if not plan_name_valid:
                rqst_errors.append("Plan: {!s} is not part of member plans".format(planstatobject.plan_name))
            if not premium_type_valid:
                rqst_errors.append(
                    "Premium Type: {!s} is not a valid premium type".format(planstatobject.premium_type))
            if not metal_level_valid:
                rqst_errors.append("Metal: {!s} is not a valid metal level".format(planstatobject.metal_level))

            if plan_name_valid and premium_type_valid and metal_level_valid:
                unsaved_plan_stat_objs.append(planstatobject)

    validated_params["rqst_usr_email"] = clean_string_value_from_dict_object(rqst_body, "root", "Email", rqst_errors)
    validated_params["rqst_no_general_assis"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_general_assis",
        rqst_errors
    )
    validated_params["rqst_no_plan_usage_assis"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_plan_usage_assis",
        rqst_errors
    )
    validated_params["rqst_no_locating_provider_assis"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_locating_provider_assis",
        rqst_errors
    )
    validated_params["rqst_no_billing_assis"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_billing_assis",
        rqst_errors
    )
    validated_params["rqst_no_enroll_apps_started"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_enroll_apps_started",
        rqst_errors
    )
    validated_params["rqst_no_enroll_qhp"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_enroll_qhp",
        rqst_errors
    )
    validated_params["rqst_no_enroll_abe_chip"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_enroll_abe_chip",
        rqst_errors
    )
    validated_params["rqst_no_enroll_shop"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_enroll_shop",
        rqst_errors
    )
    validated_params["rqst_no_referrals_agents_brokers"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_referrals_agents_brokers",
        rqst_errors
    )
    validated_params["rqst_no_referrals_ship_medicare"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_referrals_ship_medicare",
        rqst_errors
    )
    validated_params["rqst_no_referrals_other_assis_programs"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_referrals_other_assis_programs",
        rqst_errors
    )
    validated_params["rqst_no_referrals_issuers"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_referrals_issuers",
        rqst_errors
    )
    validated_params["rqst_no_referrals_doi"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_referrals_doi",
        rqst_errors
    )
    validated_params["rqst_no_mplace_tax_form_assis"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_mplace_tax_form_assis",
        rqst_errors
    )
    validated_params["rqst_no_mplace_exempt_assis"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_mplace_exempt_assis",
        rqst_errors
    )
    validated_params["rqst_no_qhp_abe_appeals"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_qhp_abe_appeals",
        rqst_errors
    )
    validated_params["rqst_no_data_matching_mplace_issues"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_data_matching_mplace_issues",
        rqst_errors
    )
    validated_params["rqst_no_sep_eligible"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_sep_eligible",
        rqst_errors
    )
    validated_params["rqst_no_employ_spons_cov_issues"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_employ_spons_cov_issues",
        rqst_errors
    )
    validated_params["rqst_no_aptc_csr_assis"] = clean_int_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "no_aptc_csr_assis",
        rqst_errors
    )
    validated_params["rqst_cmplx_cases_mplace_issues"] = clean_string_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "cmplx_cases_mplace_issues",
        rqst_errors,
        empty_string_allowed=True
    )
    validated_params["rqst_no_cps_consumers"] = rqst_no_cps_consumers
    validated_params["rqst_metrics_county"] = clean_string_value_from_dict_object(
        consumer_metrics,
        "Consumer Metrics",
        "County",
        rqst_errors
    )
    validated_params["location_instance_for_metrics"] = location_instance
    validated_params["unsaved_plan_stat_objs"] = unsaved_plan_stat_objs
    validated_params["metrics_date"] = metrics_date
