from picmodels.models.utils import filter_db_queryset_by_id


def retrieve_general_concerns_by_id(cls, rqst_general_concerns_id, list_of_ids, rqst_errors):
    general_concerns = filter_db_queryset_by_id(cls.objects.all(), rqst_general_concerns_id, list_of_ids)

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


def retrieve_general_concerns_by_name(cls, rqst_name, rqst_errors):
    general_concerns = filter_general_concern_objs_by_name(cls.objects.all(), rqst_name)
    if len(general_concerns) > 1:
        rqst_errors.append('Multiple general concerns found in db for name: {!s}'.format(rqst_name))

    response_list = create_response_list_from_db_objects(general_concerns)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No general concern instances in db for given name")

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def filter_general_concern_objs_by_name(qset, rqst_name):
    qset = qset.filter(name__iexact=rqst_name).order_by("name")

    return qset


def retrieve_related_gen_concern_rows_by_name(cls, gen_concern_names, rqst_errors):
    gen_concern_names = list(set(gen_concern_names))
    gen_concern_rows = []
    gen_concern_errors = []

    if gen_concern_names and not rqst_errors:
        for related_general_concerns_name in gen_concern_names:
            try:
                related_general_concerns_object = cls.objects.get(
                    name__iexact=related_general_concerns_name
                )
                gen_concern_rows.append(related_general_concerns_object)
            except cls.DoesNotExist:
                gen_concern_errors.append(
                    "No related ConsumerGeneralConcern database entry found for name: {}".format(
                        related_general_concerns_name
                    )
                )

    for related_general_concerns_error in gen_concern_errors:
        rqst_errors.append(related_general_concerns_error)

    return gen_concern_rows
