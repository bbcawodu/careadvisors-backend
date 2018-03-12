from picmodels.models.utils import filter_db_queryset_by_id


def get_serialized_rows_by_id(cls, rqst_general_concerns_id, list_of_ids, rqst_errors):
    rows = filter_db_queryset_by_id(cls.objects.all(), rqst_general_concerns_id, list_of_ids)

    response_list = create_response_list_from_db_objects(rows)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No rows in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['id'] == db_id for instance_data in
                                                    response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Row instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def get_serialized_rows_by_name(cls, rqst_name, rqst_errors):
    rows = filter_rows_by_name(cls.objects.all(), rqst_name)
    if len(rows) > 1:
        rqst_errors.append('Multiple rows found in db for name: {!s}'.format(rqst_name))

    response_list = create_response_list_from_db_objects(rows)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No rows in db for given name")

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def filter_rows_by_name(qset, rqst_name):
    qset = qset.filter(name__iexact=rqst_name).order_by("name")

    return qset
