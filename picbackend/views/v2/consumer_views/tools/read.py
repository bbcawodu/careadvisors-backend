"""
Defines utility functions and classes for consumer views
"""


import math
from picmodels.services import filter_db_queryset_by_id
from picmodels.services.staff_consumer_models_services.pic_consumer_services import filter_consumer_objs_by_f_and_l_name
from picmodels.services.staff_consumer_models_services.pic_consumer_services import filter_consumer_objs_by_email
from picmodels.services.staff_consumer_models_services.pic_consumer_services import filter_consumer_objs_by_first_name
from picmodels.services.staff_consumer_models_services.pic_consumer_services import filter_consumer_objs_by_last_name


def retrieve_consumer_data_by_id(consumers, rqst_consumer_id, list_of_ids, rqst_errors):
    consumers = filter_db_queryset_by_id(consumers, rqst_consumer_id, list_of_ids)

    response_list = create_response_list_from_db_objects(consumers)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No consumer instances in db for given ids")
        else:
            if list_of_ids:
                for db_id in list_of_ids:
                    tuple_of_bools_if_id_in_data = (instance_data['Database ID'] == db_id for instance_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Consumer instance with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def create_response_list_from_db_objects(db_objects):
    return_list = []

    for db_instance in db_objects:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_consumer_data_by_f_and_l_name(consumers, rqst_first_name, rqst_last_name, rqst_errors):
    consumers = filter_consumer_objs_by_f_and_l_name(consumers, rqst_first_name, rqst_last_name)

    response_list = create_response_list_from_db_objects(consumers)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No consumers instances in db for given first and last name")

    check_response_data_for_requested_data()

    response_list = [response_list]

    return response_list


def retrieve_consumer_data_by_email(consumers, list_of_emails, rqst_errors):
    response_list = []

    for email in list_of_emails:
        filtered_consumers = filter_consumer_objs_by_email(consumers, email)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with email: {} not found in database'.format(email))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_consumer_data_by_first_name(consumers, list_of_first_names, rqst_errors):
    response_list = []

    for first_name in list_of_first_names:
        filtered_consumers = filter_consumer_objs_by_first_name(consumers, first_name)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with first name: {} not found in database'.format(first_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def retrieve_consumer_data_by_last_name(consumers, list_of_last_names, rqst_errors):
    response_list = []

    for last_name in list_of_last_names:
        filtered_consumers = filter_consumer_objs_by_last_name(consumers, last_name)

        response_list_component = create_response_list_from_db_objects(filtered_consumers)

        def check_response_component_for_requested_data():
            if not response_list_component:
                rqst_errors.append('Consumer with last name: {} not found in database'.format(last_name))

        check_response_component_for_requested_data()

        def add_response_component_to_response_data():
            if response_list_component:
                response_list.append(response_list_component)

        add_response_component_to_response_data()

    return response_list


def paginate_result_list_by_changing_excess_data_to_ids(consumer_list, CONSUMERS_PER_PAGE, rqst_page_no, base_url):
    page_urls = []

    len_of_consumer_list = len(consumer_list)
    if len_of_consumer_list > CONSUMERS_PER_PAGE:
        if rqst_page_no:
            if len_of_consumer_list > ((rqst_page_no - 1) * CONSUMERS_PER_PAGE):
                for i, consumer in enumerate(consumer_list[:(CONSUMERS_PER_PAGE * (rqst_page_no - 1))]):
                    consumer_list[i] = consumer["Database ID"]
            if len_of_consumer_list > (rqst_page_no * CONSUMERS_PER_PAGE):
                for i, consumer in enumerate(consumer_list[(rqst_page_no * CONSUMERS_PER_PAGE):]):
                    consumer_list[(rqst_page_no * CONSUMERS_PER_PAGE)+i] = consumer["Database ID"]
        else:
            total_pages = math.ceil(len_of_consumer_list / CONSUMERS_PER_PAGE)
            for i in range(total_pages):
                page_urls.append(base_url + "&page=" + str(i+1))

            for i, consumer in enumerate(consumer_list[CONSUMERS_PER_PAGE:]):
                consumer_list[CONSUMERS_PER_PAGE+i] = consumer["Database ID"]

    return page_urls
