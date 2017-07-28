"""
Defines utility functions and classes for staff views
"""

from picmodels.models import CareAdvisorCustomer
from picmodels.services import filter_db_queryset_by_id
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_f_and_l_name
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_first_name
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_last_name
from picmodels.services.staff_consumer_models_services.pic_staff_services import filter_staff_objs_by_email


def retrieve_table_data_by_id(rqst_id, list_of_ids, rqst_errors):
    care_advisor_customer_qset = filter_db_queryset_by_id(CareAdvisorCustomer.objects.all(), rqst_id, list_of_ids)

    table_data_list = create_response_list_from_db_objects(care_advisor_customer_qset)

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


def retrieve_staff_data_by_f_and_l_name(rqst_first_name, rqst_last_name, rqst_errors):
    staff_qset = filter_staff_objs_by_f_and_l_name(CareAdvisorCustomer.objects.all(), rqst_first_name, rqst_last_name)

    response_list = create_response_list_from_db_objects(staff_qset)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No staff instances in db for given first and last name")

    check_response_data_for_requested_data()

    response_list = [response_list]

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_staff_data_by_email(list_of_emails, rqst_errors):
    response_list = []

    for email in list_of_emails:
        filtered_staff_qset = filter_staff_objs_by_email(CareAdvisorCustomer.objects.all(), email)

        response_list_component = create_response_list_from_db_objects(filtered_staff_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Staff instance with email: {} not found in database'.format(email))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_staff_data_by_first_name(list_of_first_names, rqst_errors):
    response_list = []

    for first_name in list_of_first_names:
        filtered_staff_qset = filter_staff_objs_by_first_name(CareAdvisorCustomer.objects.all(), first_name)

        response_list_component = create_response_list_from_db_objects(filtered_staff_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Staff instance with first name: {} not found in database'.format(first_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_staff_data_by_last_name(list_of_last_names, rqst_errors):
    response_list = []

    for last_name in list_of_last_names:
        filtered_staff_qset = filter_staff_objs_by_last_name(CareAdvisorCustomer.objects.all(), last_name)

        response_list_component = create_response_list_from_db_objects(filtered_staff_qset)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Staff instance with last name: {} not found in database'.format(last_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list
