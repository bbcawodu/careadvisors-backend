from picmodels.services import filter_db_queryset_by_id
from picmodels.services.patient_story_models_services.consumer_general_concern_services import filter_general_concern_objs_by_name


def retrieve_general_concerns_by_id(general_concerns, rqst_general_concerns_id, list_of_ids, rqst_errors):
    general_concerns = filter_db_queryset_by_id(general_concerns, rqst_general_concerns_id, list_of_ids)

    response_list = create_response_list_from_db_objects(general_concerns)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No general concern instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in
                                                    response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('General concern instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_general_concerns_by_name(general_concerns, rqst_name, rqst_errors):
    general_concerns = filter_general_concern_objs_by_name(general_concerns, rqst_name)
    if len(general_concerns) > 1:
        rqst_errors.append('Multiple general concerns found in db for name: {!s}'.format(rqst_name))

    response_list = create_response_list_from_db_objects(general_concerns)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No general concern instances in db for given name")

    check_response_data_for_requested_data()

    return response_list
