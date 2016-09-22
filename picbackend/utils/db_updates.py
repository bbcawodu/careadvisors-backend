from django.http import HttpResponse
from django.db import models, IntegrityError
from picmodels.models import PICStaff, MetricsSubmission, PlanStat, PICConsumer, NavMetricsLocation
import datetime, json, sys
from picbackend.utils.base import clean_json_string_input, clean_json_int_input, clean_dict_input, clean_list_input,\
    parse_and_log_errors


def add_staff(response_raw_data, post_json, post_errors):
    rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
    rqst_usr_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
    rqst_usr_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
    rqst_county = clean_json_string_input(post_json, "root", "User County", post_errors)
    rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)

    if len(post_errors) == 0:
        usr_rqst_values = {"first_name": rqst_usr_f_name,
                           "last_name": rqst_usr_l_name,
                           "type": rqst_usr_type,
                           "county": rqst_county,}
        user_instance, user_instance_created = PICStaff.objects.get_or_create(email=rqst_usr_email,
                                                                              defaults=usr_rqst_values)
        if not user_instance_created:
            post_errors.append('Staff database entry already exists for the email: {!s}'.format(rqst_usr_email))
        else:
            response_raw_data['Data'] = {"Database ID": user_instance.id}

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def modify_staff(response_raw_data, post_json, post_errors):
    rqst_usr_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)
    rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)
    rqst_usr_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
    rqst_usr_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
    rqst_county = clean_json_string_input(post_json, "root", "User County", post_errors)
    rqst_usr_type = clean_json_string_input(post_json, "root", "User Type", post_errors)

    if len(post_errors) == 0:
        try:
            staff_instance = PICStaff.objects.get(id=rqst_usr_id)
            staff_instance.first_name = rqst_usr_f_name
            staff_instance.last_name = rqst_usr_l_name
            staff_instance.type = rqst_usr_type
            staff_instance.county = rqst_county
            staff_instance.email = rqst_usr_email
            staff_instance.save()
            response_raw_data['Data'] = {"Database ID": staff_instance.id}
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        except PICStaff.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))
        except IntegrityError:
            post_errors.append('Database entry already exists for the email: {!s}'.format(rqst_usr_email))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def delete_staff(response_raw_data, post_json, post_errors):
    rqst_usr_id = clean_json_int_input(post_json, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            staff_instance = PICStaff.objects.get(id=rqst_usr_id)
            staff_instance.delete()
            response_raw_data['Data'] = {"Database ID": "Deleted"}
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the id: {!s}'.format(str(rqst_usr_id)))
        except PICStaff.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_usr_id)))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def add_consumer(response_raw_data, post_json, post_errors):
    rqst_consumer_email = clean_json_string_input(post_json, "root", "Email", post_errors)
    rqst_consumer_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
    rqst_consumer_m_name = clean_json_string_input(post_json, "root", "Middle Name", post_errors, empty_string_allowed=True)
    rqst_consumer_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
    rqst_consumer_zipcode = clean_json_string_input(post_json, "root", "Zipcode", post_errors)
    rqst_consumer_address = clean_json_string_input(post_json, "root", "Address", post_errors, empty_string_allowed=True)
    rqst_consumer_plan = clean_json_string_input(post_json, "root", "Plan", post_errors, empty_string_allowed=True)
    rqst_consumer_met_nav_at = clean_json_string_input(post_json, "root", "Met Navigator At", post_errors)
    rqst_consumer_household_size = clean_json_int_input(post_json, "root", "Household Size", post_errors)
    rqst_consumer_phone = clean_json_string_input(post_json, "root", "Phone Number", post_errors, empty_string_allowed=True)
    rqst_consumer_pref_lang = clean_json_string_input(post_json, "root", "Preferred Language", post_errors, empty_string_allowed=True)
    rqst_nav_id = clean_json_int_input(post_json, "root", "Navigator Database ID", post_errors)

    if len(post_errors) == 0:
        consumer_rqst_values = {"first_name": rqst_consumer_f_name,
                                "middle_name": rqst_consumer_m_name,
                                "last_name": rqst_consumer_l_name,
                                "phone": rqst_consumer_phone,
                                "zipcode": rqst_consumer_zipcode,
                                "address": rqst_consumer_address,
                                "plan": rqst_consumer_plan,
                                "met_nav_at": rqst_consumer_met_nav_at,
                                "household_size": rqst_consumer_household_size,
                                "preferred_language": rqst_consumer_pref_lang}
        consumer_instance, consumer_instance_created = PICConsumer.objects.get_or_create(email=rqst_consumer_email,
                                                                                         defaults=consumer_rqst_values)
        if not consumer_instance_created:
            post_errors.append('Consumer database entry already exists for the email: {!s}'.format(rqst_consumer_email))
        else:
            try:
                nav_instance = PICStaff.objects.get(id=rqst_nav_id)
                consumer_instance.navigator = nav_instance
                consumer_instance.save()
                response_raw_data['Data'] = {"Database ID": consumer_instance.id}
            except PICStaff.DoesNotExist:
                post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(str(rqst_nav_id)))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def modify_consumer(response_raw_data, post_json, post_errors):
    rqst_consumer_email = clean_json_string_input(post_json, "root", "Email", post_errors)
    rqst_consumer_f_name = clean_json_string_input(post_json, "root", "First Name", post_errors)
    rqst_consumer_m_name = clean_json_string_input(post_json, "root", "Middle Name", post_errors, empty_string_allowed=True)
    rqst_consumer_l_name = clean_json_string_input(post_json, "root", "Last Name", post_errors)
    rqst_consumer_zipcode = clean_json_string_input(post_json, "root", "Zipcode", post_errors)
    rqst_consumer_address = clean_json_string_input(post_json, "root", "Address", post_errors, empty_string_allowed=True)
    rqst_consumer_plan = clean_json_string_input(post_json, "root", "Plan", post_errors, empty_string_allowed=True)
    rqst_consumer_met_nav_at = clean_json_string_input(post_json, "root", "Met Navigator At", post_errors)
    rqst_consumer_household_size = clean_json_int_input(post_json, "root", "Household Size", post_errors)
    rqst_consumer_phone = clean_json_string_input(post_json, "root", "Phone Number", post_errors, empty_string_allowed=True)
    rqst_consumer_pref_lang = clean_json_string_input(post_json, "root", "Preferred Language", post_errors, empty_string_allowed=True)
    rqst_nav_id = clean_json_int_input(post_json, "root", "Navigator Database ID", post_errors)
    rqst_consumer_id = clean_json_int_input(post_json, "root", "Consumer Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
            consumer_instance.first_name = rqst_consumer_f_name
            consumer_instance.middle_name = rqst_consumer_m_name
            consumer_instance.last_name = rqst_consumer_l_name
            consumer_instance.phone = rqst_consumer_phone
            consumer_instance.zipcode = rqst_consumer_zipcode
            consumer_instance.address = rqst_consumer_address
            consumer_instance.plan = rqst_consumer_plan
            consumer_instance.met_nav_at = rqst_consumer_met_nav_at
            consumer_instance.household_size = rqst_consumer_household_size
            consumer_instance.preferred_language = rqst_consumer_pref_lang
            consumer_instance.email = rqst_consumer_email

            nav_instance = PICStaff.objects.get(id=rqst_nav_id)
            consumer_instance.navigator = nav_instance

            consumer_instance.save()
            response_raw_data['Data'] = {"Database ID": consumer_instance.id}
        except PICConsumer.DoesNotExist:
            post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(str(rqst_consumer_id)))
        except PICConsumer.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_consumer_id)))
        except IntegrityError:
            post_errors.append('Database entry already exists for the id: {!s}'.format(str(rqst_consumer_id)))
        except PICStaff.DoesNotExist:
            post_errors.append('Staff database entry does not exist for the navigator id: {!s}'.format(str(rqst_nav_id)))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def delete_consumer(response_raw_data, post_json, post_errors):
    rqst_consumer_id = clean_json_int_input(post_json, "root", "Consumer Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            consumer_instance = PICConsumer.objects.get(id=rqst_consumer_id)
            consumer_instance.delete()
            response_raw_data['Data'] = {"Database ID": "Deleted"}
        except PICConsumer.DoesNotExist:
            post_errors.append('Consumer database entry does not exist for the id: {!s}'.format(str(rqst_consumer_id)))
        except PICConsumer.MultipleObjectsReturned:
            post_errors.append('Multiple database entries exist for the id: {!s}'.format(str(rqst_consumer_id)))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data


def add_or_update_metrics_entity(response_raw_data, post_json, post_errors):
    rqst_usr_email = clean_json_string_input(post_json, "root", "Email", post_errors)

    consumer_metrics = clean_dict_input(post_json, "root", "Consumer Metrics", post_errors)
    if consumer_metrics is not None:
        consumer_metrics = post_json["Consumer Metrics"]

        rqst_cons_rec_edu = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Received Education",
                                                 post_errors)
        rqst_cons_app_maid = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Applied Medicaid",
                                                  post_errors)
        rqst_cons_sel_qhp = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Selected QHP", post_errors)
        rqst_cons_ref_maidorchip = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                        "Referred Medicaid or CHIP", post_errors)
        rqst_cons_filed_exemptions = clean_json_int_input(consumer_metrics, "Consumer Metrics", "Filed Exemptions",
                                                          post_errors)
        rqst_cons_rec_postenr_support = clean_json_int_input(consumer_metrics, "Consumer Metrics",
                                                             "Received Post-Enrollment Support", post_errors)
        rqst_cons_trends = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Trends", post_errors,
                                                   empty_string_allowed=True, none_allowed=True)
        rqst_cons_success_story = clean_json_string_input(consumer_metrics, "Consumer Metrics", "Success Story",
                                                          post_errors)
        rqst_cons_hard_or_diff = clean_json_string_input(consumer_metrics, "Consumer Metrics",
                                                         "Hardship or Difficulty", post_errors)
        rqst_usr_outr_act = clean_json_string_input(consumer_metrics, "Consumer Metrics",
                                                            "Outreach Activities", post_errors,
                                                            empty_string_allowed=True, none_allowed=True)
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
            user_instance = PICStaff.objects.get(email__iexact=rqst_usr_email)

            try:
                metrics_instance = MetricsSubmission.objects.get(staff_member=user_instance, submission_date=metrics_date)
                response_raw_data["Status"]["Message"] = ['Metrics Entry Updated']
            except models.ObjectDoesNotExist:
                metrics_instance = MetricsSubmission(staff_member=user_instance, submission_date=metrics_date)
                response_raw_data["Status"]["Message"] = ['Metrics Entry Created']
            except MetricsSubmission.MultipleObjectsReturned:
                post_errors.append("Multiple metrics entries exist for this date")

                response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
                response = HttpResponse(json.dumps(response_raw_data), content_type="application/json")
                return response

            metrics_instance.received_education = rqst_cons_rec_edu
            metrics_instance.applied_medicaid = rqst_cons_app_maid
            metrics_instance.selected_qhp = rqst_cons_sel_qhp
            metrics_instance.ref_medicaid_or_chip = rqst_cons_ref_maidorchip
            metrics_instance.filed_exemptions = rqst_cons_filed_exemptions
            metrics_instance.rec_postenroll_support = rqst_cons_rec_postenr_support
            metrics_instance.trends = rqst_cons_trends
            metrics_instance.success_story = rqst_cons_success_story
            metrics_instance.hardship_or_difficulty = rqst_cons_hard_or_diff
            metrics_instance.outreach_activity = rqst_usr_outr_act
            metrics_instance.county = rqst_metrics_county

            try:
                location_instance = NavMetricsLocation.objects.get(name=rqst_metrics_location)
                metrics_instance.location = location_instance
                metrics_instance.zipcode = location_instance.zipcode
            except models.ObjectDoesNotExist:
                post_errors.append("Location instance does not exist for given location name: {!s}.".format(rqst_metrics_location))
            except MetricsSubmission.MultipleObjectsReturned:
                post_errors.append("Multiple location instances exist for given location name: {!s}".format(rqst_metrics_location))

            if len(post_errors) == 0:
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
                    #         rqst_plan_enrollments = clean_json_int_input(rqst_plan_stats, "Plan Stats", plan, post_errors)
                    #         if rqst_plan_enrollments is not None:
                    #             planstatobject.enrollments = rqst_plan_enrollments
                    #             planstatobject.save()
                    #             metrics_instance.plan_stats.add(planstatobject)
                    #     else:
                    #         post_errors.append("Plan: {!s} is not part of member plans".format(plan))

        except models.ObjectDoesNotExist:
            post_errors.append("Staff database entry does not exist for email: {!s}".format(rqst_usr_email))

    response_raw_data = parse_and_log_errors(response_raw_data, post_errors)
    return response_raw_data
