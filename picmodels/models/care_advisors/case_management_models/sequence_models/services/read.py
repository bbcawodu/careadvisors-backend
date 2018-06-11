from picmodels.models.utils import filter_db_queryset_by_id


def get_serialized_rows_by_id(cls, validated_params,  rqst_errors):
    rqst_id = validated_params['id']
    if rqst_id != 'all':
        list_of_ids = validated_params['id_list']
    else:
        list_of_ids = None

    db_qset = prefetch_related_rows(cls.objects.all())
    db_qset = filter_db_queryset_by_id(db_qset, rqst_id, list_of_ids)

    response_list = create_response_list_from_db_objects(db_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No rows found in database.")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['id'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('db row with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def get_serialized_rows_by_name(cls, validated_params, rqst_errors):
    rqst_name = validated_params['name']

    db_qset = filter_rows_by_name(cls.objects.all(), rqst_name)
    db_qset = prefetch_related_rows(db_qset)

    response_list = create_response_list_from_db_objects(db_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No rows found for given name.")

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def prefetch_related_rows(qset):
    qset = qset.select_related()

    return qset


def filter_rows_by_name(db_qset, rqst_name):
    db_qset = db_qset.filter(name__iexact=rqst_name).order_by("name")

    return db_qset
