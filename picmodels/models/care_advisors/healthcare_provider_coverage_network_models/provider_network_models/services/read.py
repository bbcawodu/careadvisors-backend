from picmodels.models.utils import filter_db_queryset_by_id


def retrieve_provider_network_data_by_id(cls, rqst_provider_network_id, list_of_ids, rqst_errors):
    provider_network_qset = filter_db_queryset_by_id(cls.objects.all(), rqst_provider_network_id, list_of_ids)

    response_list = create_response_list_from_db_objects(provider_network_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No provider network instances in db for given ids.")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in
                                                    response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Provider network instance with id: {} not found in database.'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def retrieve_provider_network_data_by_name(cls, rqst_name, rqst_errors):
    provider_network_qset = filter_provider_network_instances_by_name(cls.objects.all(), rqst_name)

    response_list = create_response_list_from_db_objects(provider_network_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No provider network instances in db for given name.")

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def filter_provider_network_instances_by_name(provider_network_qset, rqst_name):
    provider_network_qset = provider_network_qset.filter(name__iexact=rqst_name).order_by("name")

    return provider_network_qset
