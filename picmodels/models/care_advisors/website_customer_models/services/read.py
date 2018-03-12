from picmodels.models.utils import filter_db_queryset_by_id


def retrieve_table_data_by_id(cls, rqst_id, list_of_ids, rqst_errors):
    filtered_qset = filter_db_queryset_by_id(cls.objects.all(), rqst_id, list_of_ids)

    table_data_list = create_table_data_list_from_qset(filtered_qset)

    def check_response_data_for_requested_data():
        if not table_data_list:
            rqst_errors.append("No rows in care_advisor_customer table were found for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['id'] == db_id for instance_data in table_data_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('No row in care_advisor_customer table was found with id: {}'.format(db_id))

    check_response_data_for_requested_data()

    return table_data_list


def retrieve_table_data_by_email(cls, list_of_emails, rqst_errors):
    table_data_list = []

    for email in list_of_emails:
        filtered_qset = filter_qset_by_email(cls.objects.all(), email)

        table_data_list_component = create_table_data_list_from_qset(filtered_qset)

        def check_response_component_for_requested_data():
            if not table_data_list_component:
                rqst_errors.append('No rows in care_advisor_customer table were found for email: {}'.format(email))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if table_data_list_component:
                table_data_list.append(table_data_list_component)

        add_response_component_to_response_data()

    return table_data_list


def retrieve_table_data_by_full_name(cls, full_name, rqst_errors):
    filtered_qset = filter_qset_by_full_name(cls.objects.all(), full_name)

    table_data_list = create_table_data_list_from_qset(filtered_qset)

    def check_response_component_for_requested_data():
        if not table_data_list:
            rqst_errors.append('No rows in care_advisor_customer table were found for full name: {}'.format(full_name))

    check_response_component_for_requested_data()

    return table_data_list


def retrieve_table_data_by_company_name(cls, company_name, rqst_errors):
    filtered_qset = filter_qset_by_company_name(cls.objects.all(), company_name)

    table_data_list = create_table_data_list_from_qset(filtered_qset)

    def check_response_component_for_requested_data():
        if not table_data_list:
            rqst_errors.append('No rows in care_advisor_customer table were found company name: {}'.format(company_name))

    check_response_component_for_requested_data()

    return table_data_list


def retrieve_table_data_by_phone_number(cls, list_of_phone_numbers, rqst_errors):
    table_data_list = []

    for phone_number in list_of_phone_numbers:
        filtered_qset = filter_qset_by_phone_number(cls.objects.all(), phone_number)

        table_data_list_component = create_table_data_list_from_qset(filtered_qset)

        def check_response_component_for_requested_data():
            if not table_data_list_component:
                rqst_errors.append('No rows in care_advisor_customer table were found phone number: {}'.format(phone_number))

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


def filter_qset_by_full_name(qset, rqst_full_name):
    qset = qset.filter(full_name__iexact=rqst_full_name).order_by("full_name")

    return qset


def filter_qset_by_company_name(qset, rqst_company_name):
    qset = qset.filter(company_name__iexact=rqst_company_name).order_by("company_name")

    return qset


def filter_qset_by_email(qset, rqst_email):
    qset = qset.filter(email__iexact=rqst_email).order_by("email")

    return qset


def filter_qset_by_phone_number(qset, rqst_phone_number):
    qset = qset.filter(phone_number__iexact=rqst_phone_number).order_by("phone_number")

    return qset
