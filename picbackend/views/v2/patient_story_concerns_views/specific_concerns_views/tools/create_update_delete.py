"""
This module defines utility functions and classes for views that handle locations for provider networks that are
contracted with PIC
"""

import json
from picmodels.models import ConsumerSpecificConcern
from picmodels.models import ConsumerGeneralConcern
from ....utils import clean_string_value_from_dict_object
from ....utils import clean_int_value_from_dict_object
from ....utils import clean_list_value_from_dict_object


RESEARCH_WEIGHT_DEFAULT = 50


def add_specific_concern_using_api_rqst_params(response_raw_data, rqst_specific_concern_info, rqst_errors):
    add_specific_concern_params = get_specific_concern_mgmt_put_params(rqst_specific_concern_info, rqst_errors)

    if len(rqst_errors) == 0:
        found_specific_concern_objs = check_for_specific_concern_objs_with_given_question(
            add_specific_concern_params["rqst_specific_concern_question"], rqst_errors)

        if not found_specific_concern_objs and len(rqst_errors) == 0:
            specific_concern_obj = create_new_specific_concern_obj(add_specific_concern_params)
            response_raw_data['Data']["Database ID"] = specific_concern_obj.id

    return response_raw_data


def get_specific_concern_mgmt_put_params(rqst_provider_location_info, post_errors):
    rqst_specific_concern_research_weight = clean_int_value_from_dict_object(rqst_provider_location_info, "root",
                                                                             "research_weight", post_errors,
                                                                             no_key_allowed=True)
    if not rqst_specific_concern_research_weight:
        rqst_specific_concern_research_weight = RESEARCH_WEIGHT_DEFAULT
    elif rqst_specific_concern_research_weight > 100:
        post_errors.append("Value for 'research_weight' must be less than 100. Given value is: {}".format(rqst_specific_concern_research_weight))

    rqst_related_general_concerns_names = clean_list_value_from_dict_object(rqst_provider_location_info, "root",
                                                                            "related_general_concerns", post_errors,
                                                                            empty_list_allowed=True)
    for indx, general_concern_name in enumerate(rqst_related_general_concerns_names):
        if not isinstance(general_concern_name, str):
            post_errors.append("All related general concerns must be strings, related general concern is not an string for 'related_general_concerns' field at index: {}".format(indx))
    rqst_related_general_concerns_names = list(set(rqst_related_general_concerns_names))
    related_general_concerns_objects = []
    related_general_concerns_errors = []
    if rqst_related_general_concerns_names and len(post_errors) == 0:
        for related_general_concerns_name in rqst_related_general_concerns_names:
            try:
                related_general_concerns_object = ConsumerGeneralConcern.objects.get(name__iexact=related_general_concerns_name)
                related_general_concerns_objects.append(related_general_concerns_object)
            except ConsumerGeneralConcern.DoesNotExist:
                related_general_concerns_errors.append(
                    "No related ConsumerGeneralConcern database entry found for name: {}".format(related_general_concerns_name))
    for related_general_concerns_error in related_general_concerns_errors:
        post_errors.append(related_general_concerns_error)

    return {"rqst_specific_concern_question": clean_string_value_from_dict_object(rqst_provider_location_info, "root", "question", post_errors),
            "rqst_specific_concern_research_weight": rqst_specific_concern_research_weight,
            "related_general_concerns_objects": related_general_concerns_objects}


def check_for_specific_concern_objs_with_given_question(specific_concern_question, post_errors, current_specific_concern_id=None):
    found_specific_concern_obj = False

    specific_concern_objs = ConsumerSpecificConcern.objects.filter(question__iexact=specific_concern_question)

    if specific_concern_objs:
        found_specific_concern_obj = True

        specific_concern_ids = []
        for specific_concern_obj in specific_concern_objs:
            specific_concern_ids.append(specific_concern_obj.id)

        if specific_concern_objs.count() > 1:
            post_errors.append(
                "Multiple specific concerns with question: {} already exist in db. (Hint - Delete all but one and modify the remaining) id's: {}".format(
                    specific_concern_question, json.dumps(specific_concern_ids)))
        else:
            if not current_specific_concern_id or current_specific_concern_id not in specific_concern_ids:
                post_errors.append(
                    "Specific concern with question: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        specific_concern_question, specific_concern_ids[0]))
            else:
                found_specific_concern_obj = False

    return found_specific_concern_obj


def create_new_specific_concern_obj(specific_concern_params):
    specific_concern_obj = ConsumerSpecificConcern()
    specific_concern_obj.question = specific_concern_params["rqst_specific_concern_question"]
    specific_concern_obj.research_weight = specific_concern_params["rqst_specific_concern_research_weight"]
    specific_concern_obj.save()
    specific_concern_obj.related_general_concerns = specific_concern_params["related_general_concerns_objects"]
    specific_concern_obj.save()

    return specific_concern_obj


def modify_specific_concern_using_api_rqst_params(response_raw_data, rqst_specific_concern_info, rqst_errors):
    modify_specific_concern_params = get_specific_concern_mgmt_put_params(rqst_specific_concern_info, rqst_errors)

    if len(rqst_errors) == 0:
        rqst_specific_concern_id = clean_int_value_from_dict_object(rqst_specific_concern_info, "root",
                                                                     "Database ID", rqst_errors)
        found_specific_concern_objs = check_for_specific_concern_objs_with_given_question(
            modify_specific_concern_params["rqst_specific_concern_question"], rqst_errors, rqst_specific_concern_id)

        if not found_specific_concern_objs and len(rqst_errors) == 0:
            try:
                specific_concern_obj = modify_specific_concern_obj(modify_specific_concern_params,
                                                                   rqst_specific_concern_id)

                response_raw_data['Data']["Database ID"] = specific_concern_obj.id
            except ConsumerSpecificConcern.DoesNotExist:
                rqst_errors.append("Specific concern does not exist for database id: {}".format(rqst_specific_concern_id))

    return response_raw_data


def modify_specific_concern_obj(specific_concern_params, specific_concern_id):
    specific_concern_obj = ConsumerSpecificConcern.objects.get(id=specific_concern_id)
    specific_concern_obj.question = specific_concern_params["rqst_specific_concern_question"]
    specific_concern_obj.research_weight = specific_concern_params["rqst_specific_concern_research_weight"]
    specific_concern_obj.related_general_concerns.clear()
    specific_concern_obj.related_general_concerns = specific_concern_params["related_general_concerns_objects"]
    specific_concern_obj.save()

    return specific_concern_obj


def modify_specific_concern_add_general_concern_using_api_rqst_params(response_raw_data, rqst_specific_concern_info, rqst_errors):
    modify_specific_concern_params = get_specific_concern_mgmt_put_params(rqst_specific_concern_info, rqst_errors)
    rqst_specific_concern_id = clean_int_value_from_dict_object(rqst_specific_concern_info, "root",
                                                                 "Database ID", rqst_errors)

    if len(rqst_errors) == 0:
        try:
            specific_concern_obj = ConsumerSpecificConcern.objects.get(id=rqst_specific_concern_id)
            cur_related_general_concerns_qset = specific_concern_obj.related_general_concerns.all()
            for related_general_concerns_object in modify_specific_concern_params['related_general_concerns_objects']:
                if related_general_concerns_object in cur_related_general_concerns_qset:
                    rqst_errors.append("Related general concern with the following name already exists in db id {}'s related_general_concerns list (Hint - remove from parameter 'related_general_concerns' list): {})".format(
                        specific_concern_obj.id, related_general_concerns_object.name
                    ))
        except ConsumerSpecificConcern.DoesNotExist:
            rqst_errors.append(
                "Specific concern does not exist for database id: {}".format(rqst_specific_concern_id))

        if len(rqst_errors) == 0:
            found_specific_concern_objs = check_for_specific_concern_objs_with_given_question(
                modify_specific_concern_params["rqst_specific_concern_question"], rqst_errors, rqst_specific_concern_id)

            if not found_specific_concern_objs and len(rqst_errors) == 0:
                specific_concern_obj.question = modify_specific_concern_params["rqst_specific_concern_question"]
                specific_concern_obj.research_weight = modify_specific_concern_params["rqst_specific_concern_research_weight"]
                for related_general_concerns_object in modify_specific_concern_params['related_general_concerns_objects']:
                    specific_concern_obj.related_general_concerns.add(related_general_concerns_object)

                specific_concern_obj.save()

                response_raw_data['Data']["Database ID"] = specific_concern_obj.id

    return response_raw_data


def modify_specific_concern_remove_general_concern_using_api_rqst_params(response_raw_data, rqst_specific_concern_info, rqst_errors):
    modify_specific_concern_params = get_specific_concern_mgmt_put_params(rqst_specific_concern_info, rqst_errors)
    rqst_specific_concern_id = clean_int_value_from_dict_object(rqst_specific_concern_info, "root",
                                                                "Database ID", rqst_errors)

    if len(rqst_errors) == 0:
        try:
            specific_concern_obj = ConsumerSpecificConcern.objects.get(id=rqst_specific_concern_id)
            cur_related_general_concerns_qset = specific_concern_obj.related_general_concerns.all()
            for related_general_concerns_object in modify_specific_concern_params['related_general_concerns_objects']:
                if related_general_concerns_object not in cur_related_general_concerns_qset:
                    rqst_errors.append(
                        "Related general concern with the following name does not exist in db id {}'s related_general_concerns list (Hint - remove from parameter 'related_general_concerns' list): {})".format(
                            specific_concern_obj.id, related_general_concerns_object.name
                        ))
        except ConsumerSpecificConcern.DoesNotExist:
            rqst_errors.append(
                "Specific concern does not exist for database id: {}".format(rqst_specific_concern_id))

        if len(rqst_errors) == 0:
            found_specific_concern_objs = check_for_specific_concern_objs_with_given_question(
                modify_specific_concern_params["rqst_specific_concern_question"], rqst_errors, rqst_specific_concern_id)

            if not found_specific_concern_objs and len(rqst_errors) == 0:
                specific_concern_obj.question = modify_specific_concern_params["rqst_specific_concern_question"]
                specific_concern_obj.research_weight = modify_specific_concern_params["rqst_specific_concern_research_weight"]
                for related_general_concerns_object in modify_specific_concern_params['related_general_concerns_objects']:
                    specific_concern_obj.related_general_concerns.remove(related_general_concerns_object)

                specific_concern_obj.save()

                response_raw_data['Data']["Database ID"] = specific_concern_obj.id

    return response_raw_data


def delete_specific_concern_using_api_rqst_params(response_raw_data, rqst_specific_concern_info, rqst_errors):
    rqst_specific_concern_id = clean_int_value_from_dict_object(rqst_specific_concern_info, "root", "Database ID", rqst_errors)

    if len(rqst_errors) == 0:
        try:
            specific_concern_obj = ConsumerSpecificConcern.objects.get(id=rqst_specific_concern_id)
            specific_concern_obj.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except ConsumerSpecificConcern.DoesNotExist:
            rqst_errors.append("Specific concern does not exist for database id: {}".format(rqst_specific_concern_id))

    return response_raw_data
