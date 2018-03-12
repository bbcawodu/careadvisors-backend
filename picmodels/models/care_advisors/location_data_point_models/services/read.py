from picmodels.models.utils import filter_db_queryset_by_id


def retrieve_nav_hub_location_data_by_id(cls, validated_params, rqst_nav_hub_location_id, list_of_ids, rqst_errors):
    nav_hub_location_qset = prefetch_related_rows(cls.objects.all())
    nav_hub_location_qset = filter_db_objects_by_secondary_params(nav_hub_location_qset, validated_params)
    nav_hub_location_qset = filter_db_queryset_by_id(nav_hub_location_qset, rqst_nav_hub_location_id, list_of_ids)

    response_list = create_response_list_from_db_objects(nav_hub_location_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No location entries found in database.")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Location entry with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def prefetch_related_rows(qset):
    qset = qset.select_related(
        "address"
    )

    return qset


def filter_db_objects_by_secondary_params(db_objects, validated_params):
    if 'is_cps_location' in validated_params:
        is_cps_location = validated_params['is_cps_location']
        db_objects = db_objects.filter(cps_location=is_cps_location)

    return db_objects
