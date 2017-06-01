import json
from picmodels.models import HospitalWebTrafficData
from ...utils import clean_string_value_from_dict_object
from ...utils import clean_int_value_from_dict_object


def add_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, rqst_hospital_web_traffic_calculator_data_info, post_errors):
    add_hospital_web_traffic_calculator_data_params = get_hospital_web_traffic_calculator_data_mgmt_put_params(rqst_hospital_web_traffic_calculator_data_info, post_errors)

    if len(post_errors) == 0:
        hospital_name = add_hospital_web_traffic_calculator_data_params['hospital_name']

        found_hospital_web_traffic_calculator_data_objs = check_for_hospital_web_traffic_calculator_data_objs_with_given_name(
            hospital_name, post_errors)

        if not found_hospital_web_traffic_calculator_data_objs and len(post_errors) == 0:
            hospital_web_traffic_calculator_data_obj = create_new_hospital_web_traffic_calculator_data_obj(add_hospital_web_traffic_calculator_data_params, post_errors)

            if len(post_errors) == 0:
                response_raw_data['Data']["Database ID"] = hospital_web_traffic_calculator_data_obj.id

    return response_raw_data


def get_hospital_web_traffic_calculator_data_mgmt_put_params(rqst_hospital_web_traffic_calculator_data_info, post_errors):

    return {
        "hospital_name": clean_string_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "hospital_name", post_errors),
        "monthly_visits": clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "monthly_visits", post_errors)
            }


def check_for_hospital_web_traffic_calculator_data_objs_with_given_name(hospital_name, post_errors, current_hospital_web_traffic_calculator_data_id=None):
    found_hospital_web_traffic_calculator_data_obj = False

    hospital_web_traffic_calculator_data_objs = HospitalWebTrafficData.objects.filter(hospital_name__iexact=hospital_name)

    if hospital_web_traffic_calculator_data_objs:
        found_hospital_web_traffic_calculator_data_obj = True

        hospital_web_traffic_calculator_data_ids = []
        for hospital_web_traffic_calculator_data_obj in hospital_web_traffic_calculator_data_objs:
            hospital_web_traffic_calculator_data_ids.append(hospital_web_traffic_calculator_data_obj.id)

        if hospital_web_traffic_calculator_data_objs.count() > 1:
            post_errors.append(
                "Multiple instances of hospital web traffic calculator data with name: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    hospital_name, json.dumps(hospital_web_traffic_calculator_data_ids)))
        else:
            if not current_hospital_web_traffic_calculator_data_id or current_hospital_web_traffic_calculator_data_id not in hospital_web_traffic_calculator_data_ids:
                post_errors.append(
                    "Hospital web traffic calculator data with name: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        hospital_name, hospital_web_traffic_calculator_data_ids[0]))
            else:
                found_hospital_web_traffic_calculator_data_obj = False

    return found_hospital_web_traffic_calculator_data_obj


def create_new_hospital_web_traffic_calculator_data_obj(hospital_web_traffic_calculator_data_params, post_errors):
    hospital_web_traffic_calculator_data_obj = HospitalWebTrafficData()
    hospital_web_traffic_calculator_data_obj.hospital_name = hospital_web_traffic_calculator_data_params['hospital_name']
    hospital_web_traffic_calculator_data_obj.monthly_visits = hospital_web_traffic_calculator_data_params['monthly_visits']

    if len(post_errors) == 0:
        hospital_web_traffic_calculator_data_obj.save()

    return hospital_web_traffic_calculator_data_obj


def modify_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, rqst_hospital_web_traffic_calculator_data_info, post_errors):
    modify_hospital_web_traffic_calculator_data_params = get_hospital_web_traffic_calculator_data_mgmt_put_params(rqst_hospital_web_traffic_calculator_data_info, post_errors)
    rqst_hospital_web_traffic_calculator_data_id = clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        hospital_name = modify_hospital_web_traffic_calculator_data_params['hospital_name']
        found_hospital_web_traffic_calculator_data_objs = check_for_hospital_web_traffic_calculator_data_objs_with_given_name(
            hospital_name, post_errors, rqst_hospital_web_traffic_calculator_data_id)

        if not found_hospital_web_traffic_calculator_data_objs and len(post_errors) == 0:
            hospital_web_traffic_calculator_data_obj = modify_hospital_web_traffic_calculator_data_obj(modify_hospital_web_traffic_calculator_data_params, rqst_hospital_web_traffic_calculator_data_id, post_errors)

            if len(post_errors) == 0:
                response_raw_data['Data']["Database ID"] = hospital_web_traffic_calculator_data_obj.id

    return response_raw_data


def modify_hospital_web_traffic_calculator_data_obj(hospital_web_traffic_calculator_data_params, hospital_web_traffic_calculator_data_id, post_errors):
    hospital_web_traffic_calculator_data_obj = None
    try:
        hospital_web_traffic_calculator_data_obj = HospitalWebTrafficData.objects.get(id=hospital_web_traffic_calculator_data_id)
        hospital_web_traffic_calculator_data_obj.hospital_name = hospital_web_traffic_calculator_data_params['hospital_name']
        hospital_web_traffic_calculator_data_obj.monthly_visits = hospital_web_traffic_calculator_data_params['monthly_visits']
    except HospitalWebTrafficData.DoesNotExist:
        post_errors.append("Hospital web traffic calculator data instance does not exist for database id: {}".format(hospital_web_traffic_calculator_data_id))

    if len(post_errors) == 0:
        hospital_web_traffic_calculator_data_obj.save()

    return hospital_web_traffic_calculator_data_obj


def delete_hospital_web_traffic_calculator_data_instance_using_api_rqst_params(response_raw_data, rqst_hospital_web_traffic_calculator_data_info, post_errors):
    rqst_hospital_web_traffic_calculator_data_id = clean_int_value_from_dict_object(rqst_hospital_web_traffic_calculator_data_info, "root", "Database ID", post_errors)

    if len(post_errors) == 0:
        try:
            hospital_web_traffic_calculator_data_obj = HospitalWebTrafficData.objects.get(id=rqst_hospital_web_traffic_calculator_data_id)
            hospital_web_traffic_calculator_data_obj.delete()
            response_raw_data['Data']["Database ID"] = "Deleted"
        except HospitalWebTrafficData.DoesNotExist:
            post_errors.append("Hospital web traffic calculator data instance does not exist for database id: {}".format(rqst_hospital_web_traffic_calculator_data_id))

    return response_raw_data
