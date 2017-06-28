from picmodels.services import filter_db_queryset_by_id
from picmodels.services.provider_plan_network_services.provider_location_services import filter_provider_location_instances_by_name
from picmodels.services.provider_plan_network_services.provider_location_services import filter_provider_location_instances_by_provider_network_name
from picmodels.services.provider_plan_network_services.provider_location_services import filter_provider_location_instances_by_provider_network_id


def retrieve_provider_locations_by_id(provider_location_qset, rqst_provider_location_id, list_of_ids, rqst_errors):
    provider_location_qset = filter_db_queryset_by_id(provider_location_qset, rqst_provider_location_id, list_of_ids)

    response_list = create_response_list_from_db_objects(provider_location_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No provider location instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in
                                                    response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Provider location instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_provider_locations_by_name(provider_location_qset, rqst_name, rqst_errors):
    provider_location_qset = filter_provider_location_instances_by_name(provider_location_qset, rqst_name)

    response_list = create_response_list_from_db_objects(provider_location_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No provider location instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list


def retrieve_provider_locations_by_network_name(provider_location_qset, rqst_network_name, rqst_errors):
    provider_location_qset = filter_provider_location_instances_by_provider_network_name(provider_location_qset, rqst_network_name)

    response_list = create_response_list_from_db_objects(provider_location_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No provider location instances in db for given provider network name")

    check_response_data_for_requested_data()

    return response_list


def retrieve_provider_locations_by_network_id(provider_location_qset, list_of_network_ids, rqst_errors):
    response_list = []

    for network_id in list_of_network_ids:
        filtered_provider_location_qset = filter_provider_location_instances_by_provider_network_id(provider_location_qset, network_id)

        response_list_component = create_response_list_from_db_objects(filtered_provider_location_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append(rqst_errors.append("No provider location instances in network for provider network with id: {}".format(network_id)))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list
