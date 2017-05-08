"""
Defines utility functions and classes for consumer metrics views
"""

import datetime
from ..base import clean_string_value_from_dict_object
from ..base import clean_int_value_from_dict_object
from ..base import clean_list_value_from_dict_object
from ..base import clean_dict_value_from_dict_object
from picmodels.models import MetricsSubmission
from picmodels.models import PlanStat
from picmodels.models import NavMetricsLocation
from picmodels.models import PICStaff


def add_or_update_metrics_instance_using_api_rqst_params(response_raw_data, post_data, post_errors):
    rqst_metrics_put_params = get_metrics_mgmt_put_params(post_data, post_errors)

    # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
    # create and save database entry for appointment
    if len(post_errors) == 0:
        metrics_instance, metrics_instance_message = create_or_update_metrics_obj(rqst_metrics_put_params, post_errors)

        if len(post_errors) == 0 and metrics_instance and metrics_instance_message:
            response_raw_data["Status"]["Message"] = [metrics_instance_message]

    return response_raw_data


def get_metrics_mgmt_put_params(rqst_data, rqst_errors):
    consumer_metrics = clean_dict_value_from_dict_object(rqst_data, "root", "Consumer Metrics", rqst_errors)
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
        if month < 1 or month > 12:
            rqst_errors.append("Month must be between 1 and 12 inclusive")

        day = clean_int_value_from_dict_object(metrics_date_dict, "Metrics Date", "Day", rqst_errors)
        if day < 1 or day > 31:
            rqst_errors.append("Day must be between 1 and 31 inclusive")

        year = clean_int_value_from_dict_object(metrics_date_dict, "Metrics Date", "Year", rqst_errors)
        if year < 1 or year > 9999:
            rqst_errors.append("Year must be between 1 and 9999 inclusive")

        if len(rqst_errors) == 0:
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

    return {
        "rqst_usr_email": clean_string_value_from_dict_object(rqst_data, "root", "Email", rqst_errors),
        "rqst_no_general_assis": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_general_assis", rqst_errors),
        "rqst_no_plan_usage_assis": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_plan_usage_assis", rqst_errors),
        "rqst_no_locating_provider_assis": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_locating_provider_assis", rqst_errors),
        "rqst_no_billing_assis": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_billing_assis", rqst_errors),
        "rqst_no_enroll_apps_started": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_enroll_apps_started", rqst_errors),
        "rqst_no_enroll_qhp": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_enroll_qhp", rqst_errors),
        "rqst_no_enroll_abe_chip": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_enroll_abe_chip", rqst_errors),
        "rqst_no_enroll_shop": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_enroll_shop", rqst_errors),
        "rqst_no_referrals_agents_brokers": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_agents_brokers", rqst_errors),
        "rqst_no_referrals_ship_medicare": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_ship_medicare", rqst_errors),
        "rqst_no_referrals_other_assis_programs": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_other_assis_programs", rqst_errors),
        "rqst_no_referrals_issuers": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_issuers", rqst_errors),
        "rqst_no_referrals_doi": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_doi", rqst_errors),
        "rqst_no_mplace_tax_form_assis": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_mplace_tax_form_assis", rqst_errors),
        "rqst_no_mplace_exempt_assis": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_mplace_exempt_assis", rqst_errors),
        "rqst_no_qhp_abe_appeals": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_qhp_abe_appeals", rqst_errors),
        "rqst_no_data_matching_mplace_issues": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_data_matching_mplace_issues", rqst_errors),
        "rqst_no_sep_eligible": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_sep_eligible", rqst_errors),
        "rqst_no_employ_spons_cov_issues": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_employ_spons_cov_issues", rqst_errors),
        "rqst_no_aptc_csr_assis": clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_aptc_csr_assis", rqst_errors),
        "rqst_cmplx_cases_mplace_issues": clean_string_value_from_dict_object(consumer_metrics, "Consumer Metrics", "cmplx_cases_mplace_issues", rqst_errors, empty_string_allowed=True),
        "rqst_no_cps_consumers": rqst_no_cps_consumers,
        "rqst_metrics_county": clean_string_value_from_dict_object(consumer_metrics, "Consumer Metrics", "County", rqst_errors),
        "location_instance_for_metrics": location_instance,
        "unsaved_plan_stat_objs": unsaved_plan_stat_objs,
        "metrics_date": metrics_date
    }


def create_or_update_metrics_obj(rqst_metrics_params, rqst_errors):
    metrics_instance = None
    metrics_action_message = None

    rqst_usr_email = rqst_metrics_params['rqst_usr_email']
    metrics_date = rqst_metrics_params['metrics_date']
    location_instance_for_metrics = rqst_metrics_params['location_instance_for_metrics']

    try:
        user_instance = PICStaff.objects.get(email__iexact=rqst_metrics_params['rqst_usr_email'])
    except PICStaff.DoesNotExist:
        rqst_errors.append("Staff database entry does not exist for email: {!s}".format(rqst_usr_email))
    else:
        try:
            metrics_instance = MetricsSubmission.objects.get(staff_member=user_instance, submission_date=metrics_date)
            metrics_action_message = 'Metrics Entry Updated'
        except MetricsSubmission.DoesNotExist:
            metrics_instance = MetricsSubmission(staff_member=user_instance, submission_date=metrics_date)
            metrics_action_message = 'Metrics Entry Created'
        except MetricsSubmission.MultipleObjectsReturned:
            rqst_errors.append("Multiple metrics entries exist for this date")

        if metrics_instance:
            metrics_instance.no_general_assis = rqst_metrics_params['rqst_no_general_assis']
            metrics_instance.no_plan_usage_assis = rqst_metrics_params['rqst_no_plan_usage_assis']
            metrics_instance.no_locating_provider_assis = rqst_metrics_params['rqst_no_locating_provider_assis']
            metrics_instance.no_billing_assis = rqst_metrics_params['rqst_no_billing_assis']
            metrics_instance.no_enroll_apps_started = rqst_metrics_params['rqst_no_enroll_apps_started']
            metrics_instance.no_enroll_qhp = rqst_metrics_params['rqst_no_enroll_qhp']
            metrics_instance.no_enroll_abe_chip = rqst_metrics_params['rqst_no_enroll_abe_chip']
            metrics_instance.no_enroll_shop = rqst_metrics_params['rqst_no_enroll_shop']
            metrics_instance.no_referrals_agents_brokers = rqst_metrics_params['rqst_no_referrals_agents_brokers']
            metrics_instance.no_referrals_ship_medicare = rqst_metrics_params['rqst_no_referrals_ship_medicare']
            metrics_instance.no_referrals_other_assis_programs = rqst_metrics_params['rqst_no_referrals_other_assis_programs']
            metrics_instance.no_referrals_issuers = rqst_metrics_params['rqst_no_referrals_issuers']
            metrics_instance.no_referrals_doi = rqst_metrics_params['rqst_no_referrals_doi']
            metrics_instance.no_mplace_tax_form_assis = rqst_metrics_params['rqst_no_mplace_tax_form_assis']
            metrics_instance.no_mplace_exempt_assis = rqst_metrics_params['rqst_no_mplace_exempt_assis']
            metrics_instance.no_qhp_abe_appeals = rqst_metrics_params['rqst_no_qhp_abe_appeals']
            metrics_instance.no_data_matching_mplace_issues = rqst_metrics_params['rqst_no_data_matching_mplace_issues']
            metrics_instance.no_sep_eligible = rqst_metrics_params['rqst_no_sep_eligible']
            metrics_instance.no_employ_spons_cov_issues = rqst_metrics_params['rqst_no_employ_spons_cov_issues']
            metrics_instance.no_aptc_csr_assis = rqst_metrics_params['rqst_no_aptc_csr_assis']
            metrics_instance.no_cps_consumers = rqst_metrics_params['rqst_no_cps_consumers']
            metrics_instance.cmplx_cases_mplace_issues = rqst_metrics_params['rqst_cmplx_cases_mplace_issues']
            metrics_instance.county = rqst_metrics_params['rqst_metrics_county']
            metrics_instance.location = location_instance_for_metrics
            metrics_instance.zipcode = location_instance_for_metrics.address.zipcode

            if len(rqst_errors) == 0:
                metrics_instance.save()

                metrics_instance_current_plan_stats = metrics_instance.planstat_set.all()
                for current_plan_stat_instance in metrics_instance_current_plan_stats:
                    current_plan_stat_instance.delete()

                unsaved_plan_stat_objs = rqst_metrics_params['unsaved_plan_stat_objs']
                for unsaved_plan_stat_obj in unsaved_plan_stat_objs:
                    unsaved_plan_stat_obj.metrics_submission = metrics_instance
                    unsaved_plan_stat_obj.save()

    return metrics_instance, metrics_action_message
