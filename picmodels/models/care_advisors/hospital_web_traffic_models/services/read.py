import picmodels


def retrieve_hospital_traffic_data_by_id(cls, rqst_web_traffic_calculator_data_id, list_of_ids, rqst_errors):
    web_traffic_calculator_data = picmodels.models.utils.filter_db_queryset_by_id(
        cls.objects.all(),
        rqst_web_traffic_calculator_data_id, list_of_ids
    )

    response_list = create_response_list_from_db_objects(web_traffic_calculator_data)

    def check_response_list_for_requested_data():
        if not response_list:
            rqst_errors.append("No hospital web traffic data instances in db for given ids")
        else:
            if list_of_ids:
                for rqst_id in list_of_ids:
                    tuple_of_bool_if_id_in_data = (instance_data['Database ID'] == rqst_id for instance_data in response_list)
                    if not any(tuple_of_bool_if_id_in_data):
                        rqst_errors.append('Hospital web traffic data instance with id: {} not found in database'.format(rqst_id))

    check_response_list_for_requested_data()

    return response_list


def retrieve_hospital_traffic_data_by_name(cls, rqst_hospital_name, rqst_errors):
    list_of_hospital_names = [rqst_hospital_name]
    web_traffic_calculator_data = filter_hospital_web_traffic_calculator_data_instances_by_hospital_name(
        cls.objects.all(),
        rqst_hospital_name
    )

    response_list = create_response_list_from_db_objects(web_traffic_calculator_data)

    def check_response_list_for_requested_data():
        if not response_list:
            rqst_errors.append("No hospital web traffic data instances in db for given name(s).")
        else:
            for hospital_name in list_of_hospital_names:
                tuple_of_bool_if_hospital_name_in_data = (instance_data['hospital_name'] == hospital_name for instance_data in response_list)
                if not any(tuple_of_bool_if_hospital_name_in_data):
                    rqst_errors.append('Hospital web traffic data instance with name: {} not found in database'.format(hospital_name))

    check_response_list_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def filter_hospital_web_traffic_calculator_data_instances_by_hospital_name(web_traffic_calculator_data_objs, rqst_hospital_name):
    web_traffic_calculator_data_objs = web_traffic_calculator_data_objs.filter(hospital_name=rqst_hospital_name).order_by("hospital_name")

    return web_traffic_calculator_data_objs
