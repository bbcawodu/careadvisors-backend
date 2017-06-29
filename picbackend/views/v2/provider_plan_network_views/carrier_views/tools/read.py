from picmodels.services import filter_db_queryset_by_id
from picmodels.services.provider_plan_network_services.healthcare_carrier_services import filter_carrier_objs_by_state
from picmodels.services.provider_plan_network_services.healthcare_carrier_services import filter_carrier_objs_by_name


def retrieve_carrier_data_by_id(carrier_qset, rqst_carrier_id, list_of_ids, rqst_errors):
    carrier_qset = filter_db_queryset_by_id(carrier_qset, rqst_carrier_id, list_of_ids)

    response_list = create_response_list_from_db_objects(carrier_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No carrier instances in db for given ids.")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Carrier instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_carrier_data_by_state(carrier_qset, list_of_states, rqst_errors):
    response_list = []

    for state in list_of_states:
        filtered_carrier_qset = filter_carrier_objs_by_state(carrier_qset, state)

        response_list_component = create_response_list_from_db_objects(filtered_carrier_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Carriers in the state: {} not found in database'.format(state))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_carrier_data_by_name(carrier_qset, rqst_name, rqst_errors):
    carrier_qset = filter_carrier_objs_by_name(carrier_qset, rqst_name)

    response_list = create_response_list_from_db_objects(carrier_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No carrier instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list
