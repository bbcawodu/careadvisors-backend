from picmodels.models.utils import filter_db_queryset_by_id


def get_serialized_rows_by_id(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    if rqst_id != 'all':
        list_of_ids = validated_params['id_list']
    else:
        list_of_ids = None

    filtered_qset = prefetch_related_rows(cls.objects.all())
    filtered_qset = filter_db_queryset_by_id(filtered_qset, rqst_id, list_of_ids)

    table_data_list = create_table_data_list_from_qset(filtered_qset)

    def check_response_data_for_requested_data():
        if not table_data_list:
            rqst_errors.append("No rows in NavOrgsFromOnlineForm table were found for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['id'] == db_id for instance_data in table_data_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('No row in cNavOrgsFromOnlineForm table was found with id: {}'.format(db_id))

    check_response_data_for_requested_data()

    return table_data_list


def get_serialized_rows_by_email(cls, validated_params, rqst_errors):
    list_of_emails = validated_params['email_list']

    rows_qset = prefetch_related_rows(cls.objects.all())
    table_data_list = []

    for email in list_of_emails:
        filtered_qset = filter_qset_by_email(rows_qset, email)

        table_data_list_component = create_table_data_list_from_qset(filtered_qset)

        def check_response_component_for_requested_data():
            if not table_data_list_component:
                rqst_errors.append('No rows in NavOrgsFromOnlineForm were found for email: {}'.format(email))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if table_data_list_component:
                table_data_list.append(table_data_list_component)

        add_response_component_to_response_data()

    return table_data_list


def get_serialized_rows_by_company_name(cls, validated_params, rqst_errors):
    company_name = validated_params['company_name']

    rows_qset = prefetch_related_rows(cls.objects.all())
    filtered_qset = filter_qset_by_company_name(rows_qset, company_name)

    table_data_list = create_table_data_list_from_qset(filtered_qset)

    def check_response_component_for_requested_data():
        if not table_data_list:
            rqst_errors.append('No rows in NavOrgsFromOnlineForm table were found company name: {}'.format(company_name))

    check_response_component_for_requested_data()

    return table_data_list


def get_serialized_rows_by_phone_number(cls, validated_params, rqst_errors):
    list_of_phone_numbers = validated_params['phone_number_list']

    rows_qset = prefetch_related_rows(cls.objects.all())
    table_data_list = []

    for phone_number in list_of_phone_numbers:
        filtered_qset = filter_qset_by_phone_number(rows_qset, phone_number)

        table_data_list_component = create_table_data_list_from_qset(filtered_qset)

        def check_response_component_for_requested_data():
            if not table_data_list_component:
                rqst_errors.append('No rows in NavOrgsFromOnlineForm table were found phone number: {}'.format(phone_number))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if table_data_list_component:
                table_data_list.append(table_data_list_component)

        add_response_component_to_response_data()

    return table_data_list


def create_table_data_list_from_qset(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def prefetch_related_rows(qset):
    qset = qset.select_related(
        "address",
        'address__country'
    )

    return qset


def filter_qset_by_company_name(qset, rqst_company_name):
    qset = qset.filter(company_name__iexact=rqst_company_name).order_by("company_name")

    return qset


def filter_qset_by_email(qset, rqst_email):
    qset = qset.filter(contact_email__iexact=rqst_email).order_by("contact_email")

    return qset


def filter_qset_by_phone_number(qset, rqst_phone_number):
    qset = qset.filter(contact_phone__iexact=rqst_phone_number).order_by("contact_phone")

    return qset
