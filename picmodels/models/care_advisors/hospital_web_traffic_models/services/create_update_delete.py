import json


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    traffic_row = None
    hospital_name = validated_params['hospital_name']
    found_web_traffic_calculator_data_objs = cls.check_for_traffic_rows_w_name(hospital_name, rqst_errors)

    if not found_web_traffic_calculator_data_objs and not rqst_errors:
        traffic_row = cls()
        traffic_row.hospital_name = validated_params['hospital_name']
        traffic_row.monthly_visits = validated_params['monthly_visits']

        traffic_row.save()

    return traffic_row


def check_for_traffic_rows_w_name(cls, hospital_name, rqst_errors, current_traffic_row_id=None):
    found_traffic_row_bool = False

    found_traffic_rows = cls.objects.filter(hospital_name__iexact=hospital_name)

    if found_traffic_rows:
        found_traffic_row_bool = True

        found_traffic_ids = []
        found_traffic_qset_len = len(found_traffic_rows)
        for hospital_web_traffic_calculator_data_obj in found_traffic_rows:
            found_traffic_ids.append(hospital_web_traffic_calculator_data_obj.id)

        if found_traffic_qset_len > 1:
            rqst_errors.append(
                "Multiple instances of hospital web traffic calculator data with name: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    hospital_name,
                    json.dumps(found_traffic_ids)
                )
            )
        else:
            if not current_traffic_row_id or current_traffic_row_id not in found_traffic_ids:
                rqst_errors.append(
                    "Hospital web traffic calculator data with name: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        hospital_name,
                        found_traffic_ids[0]
                    )
                )
            else:
                found_traffic_row_bool = False

    return found_traffic_row_bool


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']
    traffic_row = None

    if 'hospital_name' in validated_params:
        found_traffic_rows = cls.check_for_traffic_rows_w_name(
            validated_params['hospital_name'],
            rqst_errors,
            rqst_id
        )
    else:
        found_traffic_rows = False

    if not found_traffic_rows and not rqst_errors:
        try:
            traffic_row = cls.objects.get(id=rqst_id)

            if 'hospital_name' in validated_params:
                traffic_row.hospital_name = validated_params['hospital_name']

            if 'monthly_visits' in validated_params:
                traffic_row.monthly_visits = validated_params['monthly_visits']
        except cls.DoesNotExist:
            rqst_errors.append(
                "Hospital web traffic calculator data instance does not exist for database id: {}".format(rqst_id)
            )
            traffic_row = None

        if not rqst_errors:
            traffic_row.save()

    return traffic_row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        traffic_row = cls.objects.get(id=rqst_id)
        traffic_row.delete()
    except cls.DoesNotExist:
        rqst_errors.append("Hospital web traffic calculator data instance does not exist for database id: {}".format(rqst_id))
