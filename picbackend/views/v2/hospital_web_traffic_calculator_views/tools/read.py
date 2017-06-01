def retrieve_hospital_web_traffic_calculator_data_by_id(response_raw_data, rqst_errors, web_traffic_calculator_data, rqst_web_traffic_calculator_data_id, list_of_ids):
    if rqst_web_traffic_calculator_data_id == "all":
        all_web_traffic_calculator_data = web_traffic_calculator_data.all()
        web_traffic_calculator_data_dict = {}
        for web_traffic_calculator_data_instance in all_web_traffic_calculator_data:
            web_traffic_calculator_data_dict[web_traffic_calculator_data_instance.id] = web_traffic_calculator_data_instance.return_values_dict()
        web_traffic_calculator_data_list = []
        for web_traffic_calculator_data_key, web_traffic_calculator_data_entry in web_traffic_calculator_data_dict.items():
            web_traffic_calculator_data_list.append(web_traffic_calculator_data_entry)

        response_raw_data["Data"] = web_traffic_calculator_data_list
    elif list_of_ids:
        if len(list_of_ids) > 0:
            for indx, element in enumerate(list_of_ids):
                list_of_ids[indx] = int(element)
            web_traffic_calculator_data = web_traffic_calculator_data.filter(id__in=list_of_ids)
            if len(web_traffic_calculator_data) > 0:
                web_traffic_calculator_data_dict = {}
                for web_traffic_calculator_data_instance in web_traffic_calculator_data:
                    web_traffic_calculator_data_dict[web_traffic_calculator_data_instance.id] = web_traffic_calculator_data_instance.return_values_dict()
                web_traffic_calculator_data_list = []
                for web_traffic_calculator_data_key, web_traffic_calculator_data_entry in web_traffic_calculator_data_dict.items():
                    web_traffic_calculator_data_list.append(web_traffic_calculator_data_entry)
                response_raw_data["Data"] = web_traffic_calculator_data_list

                for web_traffic_calculator_data_id in list_of_ids:
                    if web_traffic_calculator_data_id not in web_traffic_calculator_data_dict:
                        if response_raw_data['Status']['Error Code'] != 2:
                            response_raw_data['Status']['Error Code'] = 2
                        rqst_errors.append('Hospital web traffic data instance with id: {!s} not found in database'.format(str(web_traffic_calculator_data_id)))
            else:
                rqst_errors.append('No hospital web traffic data instances found for database ID(s): ' + rqst_web_traffic_calculator_data_id)
        else:
            rqst_errors.append('No valid hospital web traffic instance data IDs provided in request (must be integers)')

    return response_raw_data, rqst_errors


def retrieve_web_traffic_calculator_data_by_hospital_name(response_raw_data, rqst_errors, web_traffic_calculator_data, rqst_hospital_name):
    web_traffic_calculator_data_list = []
    web_traffic_calculator_data = web_traffic_calculator_data.filter(hospital_name__iexact=rqst_hospital_name)

    if web_traffic_calculator_data:
        if len(web_traffic_calculator_data) > 1:
            if response_raw_data['Status']['Error Code'] != 2:
                response_raw_data['Status']['Error Code'] = 2
            rqst_errors.append('Multiple hospital web traffic data instances found in db for hospital name: {!s}'.format(rqst_hospital_name))

        for web_traffic_calculator_data_instance in web_traffic_calculator_data:
            web_traffic_calculator_data_list.append(web_traffic_calculator_data_instance.return_values_dict())
        response_raw_data["Data"] = web_traffic_calculator_data_list
    else:
        rqst_errors.append('Hospital web traffic data instance with hospital name: {!s} not found in database'.format(rqst_hospital_name))

    return response_raw_data, rqst_errors
