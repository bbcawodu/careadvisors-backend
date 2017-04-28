"""
Defines utility functions and classes for consumer metrics views
"""

import datetime
import json
from django.http import HttpResponse
from ..base import clean_string_value_from_dict_object
from ..base import clean_int_value_from_dict_object
from ..base import clean_list_value_from_dict_object
from ..base import clean_dict_value_from_dict_object
from ..base import parse_and_log_errors
from picmodels.models import MetricsSubmission
from picmodels.models import PlanStat
from picmodels.models import NavMetricsLocation
from picmodels.models import PICStaff
from django.db import models


def add_or_update_metrics_entity(response_raw_data, post_data, post_errors):
    rqst_usr_email = clean_string_value_from_dict_object(post_data, "root", "Email", post_errors)

    consumer_metrics = clean_dict_value_from_dict_object(post_data, "root", "Consumer Metrics", post_errors)
    if consumer_metrics is not None:
        consumer_metrics = post_data["Consumer Metrics"]

        rqst_no_general_assis = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_general_assis",
                                                                 post_errors)
        rqst_no_plan_usage_assis = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_plan_usage_assis",
                                                                    post_errors)
        rqst_no_locating_provider_assis = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_locating_provider_assis",
                                                                           post_errors)
        rqst_no_billing_assis = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_billing_assis",
                                                                 post_errors)
        rqst_no_enroll_apps_started = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_enroll_apps_started",
                                                                       post_errors)
        rqst_no_enroll_qhp = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_enroll_qhp",
                                                              post_errors)
        rqst_no_enroll_abe_chip = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_enroll_abe_chip",
                                                                   post_errors)
        rqst_no_enroll_shop = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_enroll_shop",
                                                               post_errors)
        rqst_no_referrals_agents_brokers = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_agents_brokers",
                                                                            post_errors)
        rqst_no_referrals_ship_medicare = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_ship_medicare",
                                                                           post_errors)
        rqst_no_referrals_other_assis_programs = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_other_assis_programs",
                                                                                  post_errors)
        rqst_no_referrals_issuers = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_issuers",
                                                                     post_errors)
        rqst_no_referrals_doi = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_referrals_doi",
                                                                 post_errors)
        rqst_no_mplace_tax_form_assis = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_mplace_tax_form_assis",
                                                                         post_errors)
        rqst_no_mplace_exempt_assis = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_mplace_exempt_assis",
                                                                       post_errors)
        rqst_no_qhp_abe_appeals = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_qhp_abe_appeals",
                                                                   post_errors)
        rqst_no_data_matching_mplace_issues = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_data_matching_mplace_issues",
                                                                               post_errors)
        rqst_no_sep_eligible = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_sep_eligible",
                                                                post_errors)
        rqst_no_employ_spons_cov_issues = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_employ_spons_cov_issues",
                                                                           post_errors)
        rqst_no_aptc_csr_assis = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_aptc_csr_assis",
                                                                  post_errors)
        rqst_cmplx_cases_mplace_issues = clean_string_value_from_dict_object(consumer_metrics, "Consumer Metrics", "cmplx_cases_mplace_issues", post_errors,
                                                                             empty_string_allowed=True)
        rqst_no_cps_consumers = clean_int_value_from_dict_object(consumer_metrics, "Consumer Metrics", "no_cps_consumers",
                                                                post_errors, no_key_allowed=True)
        if rqst_no_cps_consumers is None:
            rqst_no_cps_consumers = 0

        rqst_metrics_county = clean_string_value_from_dict_object(consumer_metrics, "Consumer Metrics", "County", post_errors)
        rqst_metrics_location = clean_string_value_from_dict_object(consumer_metrics, "Consumer Metrics", "Location", post_errors)

        metrics_date_dict = clean_dict_value_from_dict_object(consumer_metrics, "Consumer Metrics", "Metrics Date", post_errors)
        if metrics_date_dict is not None:
            month = clean_int_value_from_dict_object(metrics_date_dict, "Metrics Date", "Month", post_errors)
            if month < 1 or month > 12:
                post_errors.append("Month must be between 1 and 12 inclusive")

            day = clean_int_value_from_dict_object(metrics_date_dict, "Metrics Date", "Day", post_errors)
            if day < 1 or day > 31:
                post_errors.append("Day must be between 1 and 31 inclusive")

            year = clean_int_value_from_dict_object(metrics_date_dict, "Metrics Date", "Year", post_errors)
            if year < 1 or year > 9999:
                post_errors.append("Year must be between 1 and 9999 inclusive")

            if len(post_errors) == 0:
                metrics_date = datetime.date(year, month, day)

    # if there are no parsing errors, get or create database entries for consumer, location, and point of contact
    # create and save database entry for appointment
    if len(post_errors) == 0:
        # usr_rqst_values = {"first_name": rqst_usr_f_name,
        #                    "last_name": rqst_usr_l_name,
        #                    "type": rqst_usr_type,}
        # user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
        #                                                                       defaults=usr_rqst_values)
        try:
            metrics_instance_message = 'Metrics Entry Updated'
            user_instance = PICStaff.objects.get(email__iexact=rqst_usr_email)

            try:
                metrics_instance = MetricsSubmission.objects.get(staff_member=user_instance, submission_date=metrics_date)
            except models.ObjectDoesNotExist:
                metrics_instance = MetricsSubmission(staff_member=user_instance, submission_date=metrics_date)
                metrics_instance_message = 'Metrics Entry Created'
            except MetricsSubmission.MultipleObjectsReturned:
                post_errors.append("Multiple metrics entries exist for this date")

                response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
                response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
                return response

            metrics_instance.no_general_assis = rqst_no_general_assis
            metrics_instance.no_plan_usage_assis = rqst_no_plan_usage_assis
            metrics_instance.no_locating_provider_assis = rqst_no_locating_provider_assis
            metrics_instance.no_billing_assis = rqst_no_billing_assis
            metrics_instance.no_enroll_apps_started = rqst_no_enroll_apps_started
            metrics_instance.no_enroll_qhp = rqst_no_enroll_qhp
            metrics_instance.no_enroll_abe_chip = rqst_no_enroll_abe_chip
            metrics_instance.no_enroll_shop = rqst_no_enroll_shop
            metrics_instance.no_referrals_agents_brokers = rqst_no_referrals_agents_brokers
            metrics_instance.no_referrals_ship_medicare = rqst_no_referrals_ship_medicare
            metrics_instance.no_referrals_other_assis_programs = rqst_no_referrals_other_assis_programs
            metrics_instance.no_referrals_issuers = rqst_no_referrals_issuers
            metrics_instance.no_referrals_doi = rqst_no_referrals_doi
            metrics_instance.no_mplace_tax_form_assis = rqst_no_mplace_tax_form_assis
            metrics_instance.no_mplace_exempt_assis = rqst_no_mplace_exempt_assis
            metrics_instance.no_qhp_abe_appeals = rqst_no_qhp_abe_appeals
            metrics_instance.no_data_matching_mplace_issues = rqst_no_data_matching_mplace_issues
            metrics_instance.no_sep_eligible = rqst_no_sep_eligible
            metrics_instance.no_employ_spons_cov_issues = rqst_no_employ_spons_cov_issues
            metrics_instance.no_aptc_csr_assis = rqst_no_aptc_csr_assis
            metrics_instance.no_cps_consumers = rqst_no_cps_consumers
            metrics_instance.cmplx_cases_mplace_issues = rqst_cmplx_cases_mplace_issues
            metrics_instance.county = rqst_metrics_county

            try:
                location_instance = NavMetricsLocation.objects.get(name=rqst_metrics_location)
                metrics_instance.location = location_instance
                metrics_instance.zipcode = location_instance.address.zipcode
            except models.ObjectDoesNotExist:
                post_errors.append("Location instance does not exist for given location name: {!s}.".format(rqst_metrics_location))
            except MetricsSubmission.MultipleObjectsReturned:
                post_errors.append("Multiple location instances exist for given location name: {!s}".format(rqst_metrics_location))

            if len(post_errors) == 0:
                response_raw_data["Status"]["Message"] = [metrics_instance_message]
                metrics_instance.save()

                rqst_plan_stats = clean_list_value_from_dict_object(consumer_metrics, "Consumer Metrics", "Plan Stats", post_errors, empty_list_allowed=True)

                if rqst_plan_stats:
                    metrics_instance_plan_stats = PlanStat.objects.filter(metrics_submission=metrics_instance.id)
                    for instance_plan_stat in metrics_instance_plan_stats:
                        instance_plan_stat.delete()

                    for rqst_plan_stat_dict in rqst_plan_stats:
                        planstatobject = PlanStat()
                        planstatobject.plan_name = clean_string_value_from_dict_object(rqst_plan_stat_dict, "Plans Dict", "Issuer Name", post_errors)
                        planstatobject.premium_type = clean_string_value_from_dict_object(rqst_plan_stat_dict, "Plans Dict", "Premium Type", post_errors)
                        planstatobject.metal_level = clean_string_value_from_dict_object(rqst_plan_stat_dict, "Plans Dict", "Metal Level", post_errors)
                        planstatobject.enrollments = clean_int_value_from_dict_object(rqst_plan_stat_dict, "Plans Dict", "Enrollments", post_errors)

                        plan_name_valid = planstatobject.check_plan_choices()
                        premium_type_valid = planstatobject.check_premium_choices()
                        metal_level_valid = planstatobject.check_metal_choices()
                        if not plan_name_valid:
                            post_errors.append("Plan: {!s} is not part of member plans".format(planstatobject.plan_name))
                        if not premium_type_valid:
                            post_errors.append("Premium Type: {!s} is not a valid premium type".format(planstatobject.premium_type))
                        if not metal_level_valid:
                            post_errors.append("Metal: {!s} is not a valid metal level".format(planstatobject.metal_level))

                        if plan_name_valid and premium_type_valid and metal_level_valid:
                            planstatobject.metrics_submission = metrics_instance
                            planstatobject.save()
                    # for plan, enrollments in rqst_plan_stats.items():
                    #     planstatobject = PlanStat()
                    #     planstatobject.plan_name = plan
                    #     if planstatobject.check_plan_choices():
                    #         rqst_plan_enrollments = clean_int_value_from_dict_object(rqst_plan_stats, "Plan Stats", plan, post_errors)
                    #         if rqst_plan_enrollments is not None:
                    #             planstatobject.enrollments = rqst_plan_enrollments
                    #             planstatobject.save()
                    #             metrics_instance.plan_stats.add(planstatobject)
                    #     else:
                    #         post_errors.append("Plan: {!s} is not part of member plans".format(plan))

        except models.ObjectDoesNotExist:
            post_errors.append("Staff database entry does not exist for email: {!s}".format(rqst_usr_email))

    return response_raw_data
