"""
Defines utility functions and classes for staff views
"""

from picmodels.models import CareAdvisorCustomer
from picmodels.services import filter_db_queryset_by_id
from picmodels.services.care_advisor_customer_model_services import filter_qset_by_first_name_and_last_name
from picmodels.services.care_advisor_customer_model_services import filter_qset_by_email
from picmodels.services.care_advisor_customer_model_services import filter_qset_by_first_name
from picmodels.services.care_advisor_customer_model_services import filter_qset_by_last_name
from picmodels.services.care_advisor_customer_model_services import filter_qset_by_company_name
from picmodels.services.care_advisor_customer_model_services import filter_qset_by_phone_number


def retrieve_table_data_by_id(rqst_id, list_of_ids, rqst_errors):
    filtered_qset = filter_db_queryset_by_id(CareAdvisorCustomer.objects.all(), rqst_id, list_of_ids)

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


def create_table_data_list_from_qset(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_table_data_by_first_name_and_last_name(rqst_first_name, rqst_last_name, rqst_errors):
    filtered_qset = filter_qset_by_first_name_and_last_name(CareAdvisorCustomer.objects.all(), rqst_first_name, rqst_last_name)

    table_data_list = create_table_data_list_from_qset(filtered_qset)

    def check_response_data_for_requested_data():
        if not table_data_list:
            rqst_errors.append("No rows in care_advisor_customer table were found for given first and last name")

    check_response_data_for_requested_data()

    table_data_list = [table_data_list]

    return table_data_list


def retrieve_table_data_by_email(list_of_emails, rqst_errors):
    table_data_list = []

    for email in list_of_emails:
        filtered_qset = filter_qset_by_email(CareAdvisorCustomer.objects.all(), email)

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


def retrieve_table_data_by_first_name(list_of_first_names, rqst_errors):
    table_data_list = []

    for first_name in list_of_first_names:
        filtered_qset = filter_qset_by_first_name(CareAdvisorCustomer.objects.all(), first_name)

        table_data_list_component = create_table_data_list_from_qset(filtered_qset)

        def check_response_component_for_requested_data():
            if not table_data_list_component:
                rqst_errors.append('No rows in care_advisor_customer table were found first name: {}'.format(first_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if table_data_list_component:
                table_data_list.append(table_data_list_component)

        add_response_component_to_response_data()

    return table_data_list


def retrieve_table_data_by_last_name(list_of_last_names, rqst_errors):
    table_data_list = []

    for last_name in list_of_last_names:
        filtered_qset = filter_qset_by_last_name(CareAdvisorCustomer.objects.all(), last_name)

        table_data_list_component = create_table_data_list_from_qset(filtered_qset)

        def check_response_component_for_requested_data():
            if not table_data_list_component:
                rqst_errors.append('No rows in care_advisor_customer table were found last name: {}'.format(last_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if table_data_list_component:
                table_data_list.append(table_data_list_component)

        add_response_component_to_response_data()

    return table_data_list


def retrieve_table_data_by_company_name(company_name, rqst_errors):
    filtered_qset = filter_qset_by_company_name(CareAdvisorCustomer.objects.all(), company_name)

    table_data_list = create_table_data_list_from_qset(filtered_qset)

    def check_response_component_for_requested_data():
        if not table_data_list:
            rqst_errors.append('No rows in care_advisor_customer table were found company name: {}'.format(company_name))

    check_response_component_for_requested_data()

    return table_data_list


def retrieve_table_data_by_phone_number(list_of_phone_numbers, rqst_errors):
    table_data_list = []

    for phone_number in list_of_phone_numbers:
        filtered_qset = filter_qset_by_phone_number(CareAdvisorCustomer.objects.all(), phone_number)

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
