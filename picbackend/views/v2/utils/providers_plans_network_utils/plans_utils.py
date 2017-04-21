"""
This module defines utility functions and classes for views that handle accepted plans for provider networks contracted
with PIC
"""

import json
from picmodels.models import HealthcareCarrier
from picmodels.models import HealthcarePlan
from picbackend.views.v2.utils import clean_string_value_from_dict_object
from picbackend.views.v2.utils import clean_int_value_from_dict_object


def add_plan(response_raw_data, rqst_plan_info, post_errors):
    add_plan_params = get_plan_mgmt_put_params(rqst_plan_info, post_errors)

    if len(post_errors) == 0:
        healthcare_carrier_obj = return_healthcare_carrier_obj_with_given_id(add_plan_params['rqst_carrier_id'],
                                                                               post_errors)

        if healthcare_carrier_obj and len(post_errors) == 0:
            found_healthcare_plan_objs = check_for_healthcare_plan_objs_with_given_name_and_carrier(
                add_plan_params['rqst_plan_name'], healthcare_carrier_obj, post_errors)

            if not found_healthcare_plan_objs and len(post_errors) == 0:
                healthcare_plan = HealthcarePlan()
                healthcare_plan.name = add_plan_params['rqst_plan_name']
                healthcare_plan.carrier = healthcare_carrier_obj
                healthcare_plan.metal_level = add_plan_params['rqst_plan_metal_level']
                if not healthcare_plan.check_metal_choices():
                    post_errors.append("Metal: {!s} is not a valid metal level".format(healthcare_plan.metal_level))
                healthcare_plan.premium_type = add_plan_params['rqst_plan_premium_type']
                if not healthcare_plan.check_premium_choices():
                    post_errors.append(
                        "Premium Type: {!s} is not a valid premium type".format(healthcare_plan.premium_type))

                if len(post_errors) == 0:
                    healthcare_plan.save()
                    response_raw_data['Data']["Database ID"] = healthcare_plan.id

    return response_raw_data


def modify_plan(response_raw_data, rqst_plan_info, post_errors):
    modify_plan_params = get_plan_mgmt_put_params(rqst_plan_info, post_errors)
    rqst_plan_id = clean_int_value_from_dict_object(rqst_plan_info, "root", "Database ID", post_errors)

    healthcare_carrier_obj = return_healthcare_carrier_obj_with_given_id(modify_plan_params['rqst_carrier_id'],
                                                                         post_errors)

    if len(post_errors) == 0 and healthcare_carrier_obj:
        found_healthcare_plan_objs = check_for_healthcare_plan_objs_with_given_name_and_carrier(
            modify_plan_params['rqst_plan_name'], healthcare_carrier_obj, post_errors)

        if not found_healthcare_plan_objs:
            try:
                healthcare_plan_obj = HealthcarePlan.objects.get(id=rqst_plan_id)
                healthcare_plan_obj.name = modify_plan_params['rqst_plan_name']
                healthcare_plan_obj.carrier = healthcare_carrier_obj
                healthcare_plan_obj.metal_level = modify_plan_params['rqst_plan_metal_level']
                if not healthcare_plan_obj.check_metal_choices():
                    post_errors.append("Metal: {!s} is not a valid metal level".format(healthcare_plan_obj.metal_level))
                healthcare_plan_obj.premium_type = modify_plan_params['rqst_plan_premium_type']
                if not healthcare_plan_obj.check_premium_choices():
                    post_errors.append(
                        "Premium Type: {!s} is not a valid premium type".format(healthcare_plan_obj.premium_type))

                if len(post_errors) == 0:
                    healthcare_plan_obj.save()
                    response_raw_data['Data']["Database ID"] = healthcare_plan_obj.id
            except HealthcarePlan.DoesNotExist:
                post_errors.append("Healthcare plan does not exist for database id: {}".format(rqst_plan_id))

    return response_raw_data


def return_healthcare_carrier_obj_with_given_id(carrier_id, post_errors):
    try:
        healthcare_carrier_obj = HealthcareCarrier.objects.get(id=carrier_id)
    except HealthcareCarrier.DoesNotExist:
        healthcare_carrier_obj = None
        post_errors.append("No HealthcareCarrier objects found for id: {}".format(carrier_id))

    return healthcare_carrier_obj


def check_for_healthcare_plan_objs_with_given_name_and_carrier(plan_name, healthcare_carrier_obj, post_errors):
    found_healthcare_plan_obj = False

    healthcare_plan_objs = HealthcarePlan.objects.filter(name__iexact=plan_name, carrier=healthcare_carrier_obj)

    if healthcare_plan_objs:
        found_healthcare_plan_obj = True
        plan_ids = healthcare_plan_objs.values_list('id', flat=True)

        if len(healthcare_plan_objs) > 1:
            post_errors.append(
                "Multiple healthcare plans with name: {} and carrier: {}already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    plan_name, healthcare_carrier_obj.name, json.dumps(plan_ids)))
        else:
            post_errors.append(
                "Healthcare plan with name: {} and carrier: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                    plan_name, healthcare_carrier_obj.name, plan_ids[0]))

    return found_healthcare_plan_obj


def get_plan_mgmt_put_params(rqst_plan_info, post_errors):
    """
    This function parses the BODY of requests for PIC consumer management PUT requests, checks for errors, and returns
    relevant information as a dictionary

    :param rqst_carrier_info: (type: dictionary) Carrier information to be parsed
    :param post_errors: (type: list) list of error messages
    :return: (type: dictionary) dictionary with relevant consumer information
    """

    rqst_plan_name = clean_string_value_from_dict_object(rqst_plan_info, "root", "name", post_errors)
    rqst_carrier_id = clean_int_value_from_dict_object(rqst_plan_info, "root", "Carrier Database ID", post_errors)
    rqst_plan_premium_type = clean_string_value_from_dict_object(rqst_plan_info, "root", "premium_type", post_errors,
                                                                 none_allowed=True, no_key_allowed=True)
    rqst_plan_metal_level = clean_string_value_from_dict_object(rqst_plan_info, "root", "metal_level", post_errors,
                                                                none_allowed=True, no_key_allowed=True)

    return {"rqst_plan_name": rqst_plan_name,
            "rqst_carrier_id": rqst_carrier_id,
            "rqst_plan_premium_type": rqst_plan_premium_type,
            "rqst_plan_metal_level": rqst_plan_metal_level,}


def delete_plan(response_raw_data, rqst_carrier_info, post_errors):
    rqst_plan_id = clean_int_value_from_dict_object(rqst_carrier_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            healthcare_plan_obj = HealthcarePlan.objects.get(id=rqst_plan_id)
            healthcare_plan_obj.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except HealthcarePlan.DoesNotExist:
            post_errors.append("Healthcare plan does not exist for database id: {}".format(rqst_plan_id))

    return response_raw_data


def retrieve_id_plans(response_raw_data, rqst_errors, plans, rqst_plan_id, list_of_ids):
    if rqst_plan_id == "all":
        all_plans = plans
        plan_dict = {}
        for plan in all_plans:
            plan_dict[plan.id] = plan.return_values_dict()
        plan_list = []
        for plan_key, plan_entry in plan_dict.items():
            plan_list.append(plan_entry)

        response_raw_data["Data"] = plan_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            plans = plans.filter(id__in=list_of_ids)
            if len(plans) > 0:

                plan_dict = {}
                for plan in plans:
                    plan_dict[plan.id] = plan.return_values_dict()
                plan_list = []
                for plan_key, plan_entry in plan_dict.items():
                    plan_list.append(plan_entry)
                response_raw_data["Data"] = plan_list

                for plan_id in list_of_ids:
                    if plan_id not in plan_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Plan with id: {!s} not found in database'.format(str(plan_id)))
            else:
                rqst_errors.append('No plans found for database ID(s): ' + rqst_plan_id)
        else:
            rqst_errors.append('No valid plan IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_name_plans(response_raw_data, rqst_errors, plans, rqst_name):
    plans_list = []
    plans = plans.filter(name__iexact=rqst_name)

    if plans:
        for plan in plans:
            plans_list.append(plan.return_values_dict())
        response_raw_data["Data"] = plans_list
    else:
        rqst_errors.append('No plans with name: {!s} not found in database'.format(rqst_name))

    return response_raw_data, rqst_errors


def retrieve_plans_by_carrier_id(response_raw_data, rqst_errors, plans, rqst_carrier_id, list_of_carrier_ids):
    if rqst_carrier_id == "all":
        all_plans = plans
        plan_dict = {}
        for plan in all_plans:
            plan_dict[plan.id] = plan.return_values_dict()
        plan_list = []
        for plan_key, plan_entry in plan_dict.items():
            plan_list.append(plan_entry)

        response_raw_data["Data"] = plan_list
    elif list_of_carrier_ids:
        if len(list_of_carrier_ids) > 0:
            for indx, element in enumerate(list_of_carrier_ids):
                list_of_carrier_ids[indx] = int(element)
            plans = plans.filter(carrier__id__in=list_of_carrier_ids)
            if len(plans) > 0:

                plan_dict = {}
                for plan in plans:
                    if plan.carrier.id not in plan_dict:
                        plan_dict[plan.carrier.id] = [plan.return_values_dict()]
                    else:
                        plan_dict[plan.carrier.id].append(plan.return_values_dict())
                plan_list = []
                for plan_key, plan_entry in plan_dict.items():
                    plan_list.append(plan_entry)
                response_raw_data["Data"] = plan_list

                for carrier_id in list_of_carrier_ids:
                    if carrier_id not in plan_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Plan with carrier id: {!s} not found in database'.format(str(carrier_id)))
            else:
                rqst_errors.append('No plans found for carrier database ID(s): ' + rqst_carrier_id)
        else:
            rqst_errors.append('No valid carrier database IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_plans_by_carrier_state(response_raw_data, rqst_errors, plans, rqst_carrier_state, list_of_carrier_states):
    plans_dict = {}
    plans_object = plans
    for state in list_of_carrier_states:
        plans = plans_object.filter(carrier__state_province__iexact=state)
        for plan in plans:
            if state not in plans_dict:
                plans_dict[state] = [plan.return_values_dict()]
            else:
                plans_dict[state].append(plan.return_values_dict())
    if len(plans_dict) > 0:
        plans_list = []
        for plan_key, plan_entry in plans_dict.items():
            plans_list.append(plan_entry)
        response_raw_data["Data"] = plans_list
        for state in list_of_carrier_states:
            if state not in plans_dict:
                if response_raw_data['Status']['Error Code'] != 2:
                    response_raw_data['Status']['Error Code'] = 2
                rqst_errors.append('No plans with a carrier in state: {!s} found in database'.format(state))
    else:
        rqst_errors.append('No plans with a carrier in state(s): {!s} found in database'.format(rqst_carrier_state))

    return response_raw_data, rqst_errors


def retrieve_plans_by_carrier_name(response_raw_data, rqst_errors, plans, rqst_carrier_name):
    plans_list = []
    plans = plans.filter(carrier__name__iexact=rqst_carrier_name)

    if plans:
        for plans in plans:
            plans_list.append(plans.return_values_dict())
        response_raw_data["Data"] = plans_list
    else:
        rqst_errors.append('No Plans with a carrier with the name: {!s} found in database'.format(rqst_carrier_name))

    return response_raw_data, rqst_errors
