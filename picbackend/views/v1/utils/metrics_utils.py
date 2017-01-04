"""
Defines utility functions and classes for consumer metrics views
"""

import datetime
import json
from django.http import HttpResponse
from .base import clean_json_string_input
from .base import clean_json_int_input
from .base import clean_list_input
from .base import clean_dict_input
from .base import parse_and_log_errors
from picmodels.models import MetricsSubmission
from picmodels.models import PlanStat
from picmodels.models import NavMetricsLocation
from picmodels.models import PICStaff
from django.db import models


def add_or_update_metrics_entity(response_raw_data, post_json, post_errors):
    rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)

    consumer_metrics = clean_dict_input(post_json, "root", "Consumer Metrics", post_errors)
    if consumer_metrics is not None:
        consumer_metrics = post_json["Consumer Metrics"]

        rqst_no_general_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_general_assis",
                                                 post_errors)
        rqst_no_plan_usage_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_plan_usage_assis",
                                                 post_errors)
        rqst_no_locating_provider_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_locating_provider_assis",
                                                 post_errors)
        rqst_no_billing_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_billing_assis",
                                                 post_errors)
        rqst_no_enroll_apps_started = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_enroll_apps_started",
                                                 post_errors)
        rqst_no_enroll_qhp = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_enroll_qhp",
                                                 post_errors)
        rqst_no_enroll_abe_chip = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_enroll_abe_chip",
                                                 post_errors)
        rqst_no_enroll_shop = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_enroll_shop",
                                                 post_errors)
        rqst_no_referrals_agents_brokers = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_agents_brokers",
                                                 post_errors)
        rqst_no_referrals_ship_medicare = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_ship_medicare",
                                                 post_errors)
        rqst_no_referrals_other_assis_programs = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_other_assis_programs",
                                                 post_errors)
        rqst_no_referrals_issuers = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_issuers",
                                                 post_errors)
        rqst_no_referrals_doi = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_referrals_doi",
                                                 post_errors)
        rqst_no_mplace_tax_form_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_mplace_tax_form_assis",
                                                 post_errors)
        rqst_no_mplace_exempt_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_mplace_exempt_assis",
                                                 post_errors)
        rqst_no_qhp_abe_appeals = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_qhp_abe_appeals",
                                                 post_errors)
        rqst_no_data_matching_mplace_issues = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_data_matching_mplace_issues",
                                                 post_errors)
        rqst_no_sep_eligible = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_sep_eligible",
                                                 post_errors)
        rqst_no_employ_spons_cov_issues = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_employ_spons_cov_issues",
                                                 post_errors)
        rqst_no_aptc_csr_assis = clean_json_int_input(consumer_metrics, "Consumer Metrics", "no_aptc_csr_assis",
                                                 post_errors)
        rqst_cmplx_cases_mplace_issues = clean_json_string_input(consumer_metrics, "Consumer Metrics", "cmplx_cases_mplace_issues", post_errors,
                                                   empty_string_allowed=True)

        rqst_metrics_county = clean_json_string_input(consumer_metrics, "Consumer Metrics", "County", post_errors)
        rqst_metrics_location = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Location", post_errors)

        metrics_date_dict = clean_dict_input(consumer_metrics, "Consumer Metrics", "Metrics Date", post_errors)
        if metrics_date_dict is not None:
            month = clean_json_int_input(metrics_date_dict, "Metrics Date", "Month", post_errors)
            if month < 1 or month > 12:
                post_errors.append("Month must be between 1 and 12 inclusive")

            day = clean_json_int_input(metrics_date_dict, "Metrics Date", "Day", post_errors)
            if day < 1 or day > 31:
                post_errors.append("Day must be between 1 and 31 inclusive")

            year = clean_json_int_input(metrics_date_dict, "Metrics Date", "Year", post_errors)
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

                rqst_plan_stats = clean_list_input(consumer_metrics, "Consumer Metrics", "Plan Stats", post_errors)
                metrics_instance_plan_stats = PlanStat.objects.filter(metrics_submission=metrics_instance.id)
                for instance_plan_stat in metrics_instance_plan_stats:
                    instance_plan_stat.delete()
                if rqst_plan_stats is not None:
                    for rqst_plan_stat_dict in rqst_plan_stats:
                        planstatobject = PlanStat()
                        planstatobject.plan_name = clean_json_string_input(rqst_plan_stat_dict, "Plans Dict", "Issuer Name", post_errors)
                        planstatobject.premium_type = clean_json_string_input(rqst_plan_stat_dict, "Plans Dict", "Premium Type", post_errors)
                        planstatobject.metal_level = clean_json_string_input(rqst_plan_stat_dict, "Plans Dict", "Metal Level", post_errors)
                        planstatobject.enrollments = clean_json_int_input(rqst_plan_stat_dict, "Plans Dict", "Enrollments", post_errors)

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


# defines function to group metrics by given parameter
def group_metrics(metrics_dict, grouping_parameter):
    return_dict = {}
    if grouping_parameter == "County":
        for staff_key, staff_dict in metrics_dict.items():
            for metrics_entry in staff_dict["Metrics Data"]:
                if metrics_entry[grouping_parameter] not in return_dict:
                    return_dict[metrics_entry[grouping_parameter]] = {staff_key: {"Metrics Data": [metrics_entry],
                                                                      "Staff Information": staff_dict["Staff Information"]}}
                else:
                    if staff_key not in return_dict[metrics_entry[grouping_parameter]]:
                        return_dict[metrics_entry[grouping_parameter]][staff_key] = {"Metrics Data": [metrics_entry],
                                                                                     "Staff Information": staff_dict["Staff Information"]}
                    else:
                        return_dict[metrics_entry[grouping_parameter]][staff_key]["Metrics Data"].append(metrics_entry)

    elif grouping_parameter == "Zipcode":
        for staff_key, staff_dict in metrics_dict.items():
            for metrics_entry in staff_dict["Metrics Data"]:
                if metrics_entry[grouping_parameter] not in return_dict:
                    return_dict[metrics_entry[grouping_parameter]] = {staff_key: {"Metrics Data": [metrics_entry],
                                                                      "Staff Information": staff_dict["Staff Information"]}}
                else:
                    if staff_key not in return_dict[metrics_entry[grouping_parameter]]:
                        return_dict[metrics_entry[grouping_parameter]][staff_key] = {"Metrics Data": [metrics_entry],
                                                                                     "Staff Information": staff_dict["Staff Information"]}
                    else:
                        return_dict[metrics_entry[grouping_parameter]][staff_key]["Metrics Data"].append(metrics_entry)
    return return_dict


def retrieve_id_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_id, list_of_ids, fields=None):
    if rqst_staff_id.lower() != "all":
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

    metrics_dict = {}
    if len(metrics_submissions) > 0:
        for metrics_submission in metrics_submissions:
            values_dict = metrics_submission.return_values_dict()
            filtered_values_dict = {}
            if fields:
                for field in fields:
                    filtered_values_dict[field] = values_dict[field]
            else:
                filtered_values_dict = values_dict

            if metrics_submission.staff_member_id not in metrics_dict:
                metrics_dict[metrics_submission.staff_member_id] = {"Metrics Data": [filtered_values_dict]}
                metrics_dict[metrics_submission.staff_member_id]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
            else:
                metrics_dict[metrics_submission.staff_member_id]["Metrics Data"].append(filtered_values_dict)

        if rqst_staff_id.lower() != "all":
            for staff_id in list_of_ids:
                if staff_id not in metrics_dict:
                    if response_raw_data['Status']['Error Code'] != 2:
                        response_raw_data['Status']['Error Code'] = 2
                    rqst_errors.append('Metrics for staff Member with id: {!s} not found in database'.format(str(staff_id)))
                    response_raw_data["Status"]["Missing Parameters"].append(str(staff_id))
    else:
        rqst_errors.append('No metrics entries for staff ID(s): {!s} not found in database'.format(rqst_staff_id))
        response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_id)

    return metrics_dict


def retrieve_f_l_name_metrics(response_raw_data, rqst_errors, metrics_submissions, list_of_first_names, list_of_last_names, rqst_fname, rqst_lname, fields=None):
    metrics_dict = {}
    if len(list_of_first_names) == len(list_of_last_names):
        list_of_ids = []
        for i, first_name in enumerate(list_of_first_names):
            last_name = list_of_last_names[i]
            name_ids = PICStaff.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).values_list('id', flat=True)
            if len(name_ids) > 0:
                list_of_ids.append(name_ids)
            else:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('Metrics for staff member with name: {!s} {!s} not found in database'.format(first_name, last_name))
                response_raw_data["Status"]["Missing Parameters"].append(first_name + last_name)
        list_of_ids = list(set().union(*list_of_ids))
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first names(s): {!s}; and last names(s): {!s} not found in database'.format(rqst_fname, rqst_lname))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_fname + rqst_lname)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                name = '{!s} {!s}'.format(metrics_submission.staff_member.first_name, metrics_submission.staff_member.last_name)
                if name not in metrics_dict:
                    metrics_dict[name] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[name]["Metrics Data"].append(filtered_values_dict)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first names(s): {!s}; and last names(s): {!s} not found in database'.format(rqst_fname, rqst_lname))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_fname + rqst_lname)
    else:
        rqst_errors.append('Length of first name list must be equal to length of last name list')

    return metrics_dict


def retrieve_first_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_fname, list_of_first_names, fields=None):
    list_of_ids = []
    metrics_dict = {}

    for first_name in list_of_first_names:
        first_name_ids = PICStaff.objects.filter(first_name__iexact=first_name).values_list('id', flat=True)
        if len(first_name_ids) > 0:
            list_of_ids.append(first_name_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Metrics for staff member with first name: {!s} not found in database'.format(first_name))
            response_raw_data["Status"]["Missing Parameters"].append(first_name)
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                if metrics_submission.staff_member.first_name not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.first_name] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[metrics_submission.staff_member.first_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.first_name]["Metrics Data"].append(filtered_values_dict)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_fname))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_fname)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for first name(s): {!s} not found in database'.format(rqst_fname))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_fname)

    return metrics_dict


def retrieve_last_name_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_lname, list_of_last_names, fields=None):
    list_of_ids = []
    metrics_dict = {}

    for last_name in list_of_last_names:
        last_name_ids = PICStaff.objects.filter(last_name__iexact=last_name).values_list('id', flat=True)
        if len(last_name_ids) > 0:
            list_of_ids.append(last_name_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Metrics for staff member with last name: {!s} not found in database'.format(last_name))
            response_raw_data["Status"]["Missing Parameters"].append(last_name)
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                if metrics_submission.staff_member.last_name not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.last_name] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[metrics_submission.staff_member.last_name]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.last_name]["Metrics Data"].append(filtered_values_dict)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_lname))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_lname)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for last name(s): {!s} not found in database'.format(rqst_lname))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_lname)

    return metrics_dict


def retrieve_email_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_email, list_of_emails, fields=None):
    list_of_ids = []
    metrics_dict = {}

    for email in list_of_emails:
        email_ids = PICStaff.objects.filter(email__iexact=email).values_list('id', flat=True)
        if len(email_ids) > 0:
            list_of_ids.append(email_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Staff member with email: {!s} not found in database'.format(email))
            response_raw_data["Status"]["Missing Parameters"].append(email)
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                if metrics_submission.staff_member.email not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(filtered_values_dict)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_staff_email))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_email)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for email(s): {!s} not found in database'.format(rqst_staff_email))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_email)

    return metrics_dict


def retrieve_mpn_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_staff_mpn, list_of_mpns, fields=None):
    list_of_ids = []
    metrics_dict = {}

    for mpn in list_of_mpns:
        mpn_ids = PICStaff.objects.filter(mpn__iexact=mpn).values_list('id', flat=True)
        if len(mpn_ids) > 0:
            list_of_ids.append(mpn_ids)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Staff member with mpn: {!s} not found in database'.format(mpn))
            response_raw_data["Status"]["Missing Parameters"].append(mpn)
    list_of_ids = list(set().union(*list_of_ids))
    if len(list_of_ids) > 0:
        for indx, element in enumerate(list_of_ids):
            list_of_ids[indx] = int(element)
        metrics_submissions = metrics_submissions.filter(staff_member__in=list_of_ids)

        if len(metrics_submissions) > 0:
            for metrics_submission in metrics_submissions:
                values_dict = metrics_submission.return_values_dict()
                filtered_values_dict = {}
                if fields:
                    for field in fields:
                        filtered_values_dict[field] = values_dict[field]
                else:
                    filtered_values_dict = values_dict

                if metrics_submission.staff_member.email not in metrics_dict:
                    metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [filtered_values_dict]}
                    metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
                else:
                    metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(filtered_values_dict)
        else:
            if response_raw_data['Status']['Error Code'] != 2:
                rqst_errors.append('No metrics entries for mpn(s): {!s} not found in database'.format(rqst_staff_mpn))
                response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_mpn)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for mpn(s): {!s} not found in database'.format(rqst_staff_mpn))
            response_raw_data["Status"]["Missing Parameters"].append(rqst_staff_mpn)

    return metrics_dict


def retrieve_location_metrics(response_raw_data, rqst_errors, metrics_submissions, rqst_location, fields=None):
    metrics_submissions = metrics_submissions.filter(location__name__iexact=rqst_location)

    metrics_dict = {}
    if len(metrics_submissions) > 0:
        for metrics_submission in metrics_submissions:
            values_dict = metrics_submission.return_values_dict()
            filtered_values_dict = {}
            if fields:
                for field in fields:
                    filtered_values_dict[field] = values_dict[field]
            else:
                filtered_values_dict = values_dict

            if metrics_submission.staff_member.email not in metrics_dict:
                metrics_dict[metrics_submission.staff_member.email] = {"Metrics Data": [filtered_values_dict]}
                metrics_dict[metrics_submission.staff_member.email]["Staff Information"] = metrics_submission.staff_member.return_values_dict()
            else:
                metrics_dict[metrics_submission.staff_member.email]["Metrics Data"].append(filtered_values_dict)
    else:
        if response_raw_data['Status']['Error Code'] != 2:
            rqst_errors.append('No metrics entries for location(s): {!s} found in database'.format(rqst_location))

    return metrics_dict
